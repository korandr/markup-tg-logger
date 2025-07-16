from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from socket import socket
from socketserver import BaseServer
from typing import Any
from urllib.parse import urlparse


HOST = 'localhost'
PORT = 8080
SAVE_JSON_ENDPOINT = '/save-json'
BAD_REQUEST_ENDPOINT = '/bad-reqest'

_ENCODING = 'utf-8'
_CONTENT_TYPE_HEADER = 'Content-type'
_CONTENT_TYPE_JSON = 'application/json'
_RetAddress = Any # from socket
_AfInetAddress = tuple[str | bytes | bytearray, int] # from socketserver
_RequestType = socket | tuple[bytes, socket]


class JsonHub:
    """Exchanger for saving JSON when testing JSON API."""

    def __init__(self) -> None:
        self._data: dict[str, Any] | None = None

    def set_received_json(self, data: dict[str, Any]) -> None:
        """Store the JSON received by the server inside a class."""

        self._data = data

    def get_last_received_json(self, auto_reset: bool = True) -> dict[str, Any] | None:
        """Get the last saved JSON.
        
        Args:
            auto_reset: If `True`, the data will be flushed after receiving.
        """

        data = self._data
        if auto_reset:
            self._data = None

        return data

    def reset_saved_json(self) -> None:
        """Manually reset saved data."""

        self._data = None


class MockTelegramHandler(BaseHTTPRequestHandler):
    """HTTP handler for processing test POST requests.
    
    Endpoints:
        - `SAVE_JSON_ENDPOINT`: Accepts a POST request and stores the submitted JSON,
           which can then be retrieved through the installed `JsonHub` instance. Response: 200.
        - `BAD_REQUEST_ENDPOINT`: Always returns 400 Bad Request.
    """

    def __init__(
        self,
        request: _RequestType,
        client_address: _RetAddress,
        server: BaseServer,
        json_hub: JsonHub,
    ) -> None:
        self._json_hub = json_hub
        super().__init__(request, client_address, server)

    def do_POST(self) -> None:
        """Process HTTP POST request and generate response."""

        path = urlparse(self.path).path

        if path == SAVE_JSON_ENDPOINT:
            self._save_json()
        elif path == BAD_REQUEST_ENDPOINT:
            self._bad_request()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode(_ENCODING))

    def _save_json(self) -> None:
        """Save JSON data from the request to `JsonHub` and generate a response."""

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            json_data = json.loads(post_data.decode(_ENCODING))
            self._json_hub.set_received_json(json_data)
            self.send_response(200)
            self.send_header(_CONTENT_TYPE_HEADER, _CONTENT_TYPE_JSON)
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode(_ENCODING))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header(_CONTENT_TYPE_HEADER, _CONTENT_TYPE_JSON)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode(_ENCODING))

    def _bad_request(self) -> None:
        """Generate HTTP BadRequest response."""

        self.send_response(400)
        self.send_header(_CONTENT_TYPE_HEADER, _CONTENT_TYPE_JSON)
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Bad Request'}).encode(_ENCODING))


class MockTelegramServer(HTTPServer):
    """Simulated Telegram server for testing based on `http.server`."""

    def __init__(
        self,
        server_address: _AfInetAddress,
        RequestHandlerClass: type[MockTelegramHandler],
        json_hub: JsonHub,
        bind_and_activate: bool = True,
    ) -> None:
        """
        Args:
            server_address: Server address in the format `(host, port)`.
            RequestHandlerClass: The handler class that will be created on each request.
            json_hub: A `JsonHub` instance to store the request data.
            bind_and_activate: Starting the server.
        """

        make_handler_func = lambda request, address, server: RequestHandlerClass(
            request, address, server, json_hub
        )

        super().__init__(server_address, make_handler_func, bind_and_activate)
        self._json_hub = json_hub

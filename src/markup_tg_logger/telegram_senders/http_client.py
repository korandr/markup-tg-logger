from http.client import HTTPConnection, HTTPSConnection
import json
from typing import Any, override
from urllib.parse import urlparse

from ..config import MAX_MESSAGE_LENGTH, TELEGRAM_SEND_MESSAGE_URL
from ..interfaces import ITelegramSender
from ..exceptions import SenderError, TelegramApiError


class HttpClientTelegramSender(ITelegramSender):
    """Implementation of Telegram Bot API method `sendMessage` using `http.client`.
    
    Docs:
        https://core.telegram.org/bots/api#sendmessage
    """

    _MAX_MESSAGE_LENGTH: int = MAX_MESSAGE_LENGTH
    _STATUS_CODE_OK = 200
    _CONTENT_TYPE_HEADER = 'Content-Type'
    _CONTENT_TYPE_JSON = 'application/json'
    _ENCODING = 'utf-8'

    def __init__(self, url: str = TELEGRAM_SEND_MESSAGE_URL) -> None:
        """
        Args:
            url: Telegram Bot API URL for the `sendMessage` method. Contains one required parameter
                `{bot_token}`. Use default value. Overridden for tests only.
        """

        self._url = url

    @override
    def send(
        self,
        bot_token: str,
        chat_id: int | str,
        text: str,
        parse_mode: str = '',
        disable_notification: bool = False,
        **params: dict[str, Any]
    ) -> None:
        if len(text) > self._MAX_MESSAGE_LENGTH:
            raise ValueError('Text exceeds message character limit')
        
        url = self._url.format(bot_token=bot_token)
        parsed_url = urlparse(url)
        protocol = parsed_url.scheme
        host = parsed_url.netloc
        endpoint = parsed_url.path

        payload: dict[str, Any] = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
        }
        payload.update(params)

        headers = {
            self._CONTENT_TYPE_HEADER: self._CONTENT_TYPE_JSON,
        }

        connection = self._make_connection(host=host, protocol=protocol)
        try:
            connection.request(
                method = 'POST',
                url = endpoint,
                body = json.dumps(payload),
                headers = headers,
            )
            response = connection.getresponse()

        except Exception as e:
            raise SenderError(f'Error sending HTTP request: {e}')
        finally:
            connection.close()

        response_data = response.read().decode(self._ENCODING)
        if response.status != self._STATUS_CODE_OK:
            if response.getheader(self._CONTENT_TYPE_HEADER) == self._CONTENT_TYPE_JSON:
                json_data = json.loads(response_data)
                raise TelegramApiError(f'Error interacting with Telegram Bot API: {json_data}')
            else:
                raise SenderError(f'Error sending HTTP request. Status Code: {response.status}')
            
    def _make_connection(self, host: str, protocol: str) -> HTTPConnection | HTTPSConnection:
        """Create a connection instance depending on the protocol."""

        protocol_to_connection_class: dict[str, type[HTTPConnection | HTTPSConnection]] = {
            'http': HTTPConnection,
            'https': HTTPSConnection,
        }

        if not protocol in protocol_to_connection_class:
            raise SenderError(f'Unsupported protocol: "{host}"')
        
        return protocol_to_connection_class[protocol](host)

from collections.abc import Generator
import pytest
import threading

from .test_utils.telegram_server import JsonHub, HOST, PORT, MockTelegramHandler, MockTelegramServer


@pytest.fixture(scope='module')
def telegram_server_json_hub() -> Generator[JsonHub, None, None]:
    """Starts the test server in a separate thread."""

    json_hub = JsonHub()
    print('Mock Telegram Server Started')
    server = MockTelegramServer((HOST, PORT), MockTelegramHandler, json_hub)
    
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    yield json_hub

    server.shutdown()
    server.server_close()
    thread.join()

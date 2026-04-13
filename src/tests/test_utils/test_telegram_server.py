import pytest
import requests

from .telegram_server import (
    BAD_REQUEST_ENDPOINT,
    BOT_TOKEN,
    HOST,
    JsonHub,
    PORT, 
    SAVE_JSON_ENDPOINT,
)


@pytest.mark.utils
def test_mock_telegram_server(telegram_server_json_hub: JsonHub) -> None:
    telegram_server_json_hub.reset_saved_json()
    JSON = {'test': 'data'}

    requests.post(url=f'http://{HOST}:{PORT}/bot{BOT_TOKEN}/{SAVE_JSON_ENDPOINT}', json=JSON)

    assert telegram_server_json_hub.get_last_received_json() == JSON

@pytest.mark.utils
def test_mock_telegram_server_bad_request() -> None:
    response = requests.post(
        url = f'http://{HOST}:{PORT}/bot{BOT_TOKEN}/{BAD_REQUEST_ENDPOINT}',
        json = {},
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Bad Request'

@pytest.mark.utils
def test_mock_telegram_server_invalid_json() -> None:
    response = requests.post(url=f'http://{HOST}:{PORT}/bot{BOT_TOKEN}/{SAVE_JSON_ENDPOINT}')

    assert response.status_code == 400
    assert response.json()['error'] == 'Invalid JSON'

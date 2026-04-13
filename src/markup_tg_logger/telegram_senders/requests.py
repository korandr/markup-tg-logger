from typing import Any, override

import requests

from ..config import MAX_MESSAGE_LENGTH, TELEGRAM_BASE_URL, TELEGRAM_METHOD, TELEGRAM_FULL_URL
from ..interfaces import ITelegramSender
from ..exceptions import SenderError, TelegramApiError


class RequestsTelegramSender(ITelegramSender):
    """Implementation of Telegram Bot API method `sendMessage` on the `requests` library.
    
    Docs:
        https://core.telegram.org/bots/api#sendmessage
    """

    _MAX_MESSAGE_LENGTH: int = MAX_MESSAGE_LENGTH
    _STATUS_CODE_OK = 200
    _CONTENT_TYPE_HEADER = 'Content-Type'
    _CONTENT_TYPE_JSON = 'application/json'

    def __init__(
        self,
        *,
        base_url: str = TELEGRAM_BASE_URL,
        method: str = TELEGRAM_METHOD,
    ) -> None:
        """
        Args:
            base_url: Telegram Bot API base URL. You can specify simple proxy here.
            method: The Telegram Bot API method that will be used to send the message.
        """

        self._base_url = base_url
        self._method = method

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
            raise SenderError('Text exceeds message character limit')
        
        url = TELEGRAM_FULL_URL.format(
            bot_token = bot_token,
            base_url = self._base_url,
            method = self._method,
        )

        payload: dict[str, Any] = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
        }
        payload.update(params)

        try:
            response = requests.post(url, json=payload)
        except Exception as e:
            raise SenderError(f'Error sending HTTP request: {e}')
        
        if response.status_code != self._STATUS_CODE_OK:
            if response.headers.get(self._CONTENT_TYPE_HEADER) == self._CONTENT_TYPE_JSON:
                json_data = response.json()
                raise TelegramApiError(f'Error interacting with Telegram Bot API: {json_data}')
            else:
                raise SenderError(f'Error sending HTTP request. Status Code: {response.status_code}')
        

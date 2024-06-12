from typing import Dict, Any

import requests

from ..config import MAX_MESSAGE_LENGTH, URL


# https://core.telegram.org/bots/api#sendmessage

class TelegramSender:
    def __init__(self):
        self._MAX_MESSAGE_LENGTH = MAX_MESSAGE_LENGTH
        self._URL = URL

    def send(self, bot_token: str, chat_id: int | str, text: str, parse_mode: str = '', disable_notification: bool = False, **params: Dict[str, Any]) -> None:
        if len(text) > self._MAX_MESSAGE_LENGTH: raise ValueError('Text exceeds message character limit')
        
        url = self._URL.format(bot_token=bot_token)

        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
        }
        payload.update(params)

        response = requests.post(url, json=payload)
        if response.status_code != 200 and response.headers.get('Content-Type') == 'application/json':
            json_data = response.json()
            print(json_data)
        response.raise_for_status()


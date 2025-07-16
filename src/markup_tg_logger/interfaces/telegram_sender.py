from abc import ABC, abstractmethod
from typing import Any


class ITelegramSender(ABC):
    """Interface for Telegram Bot API implementations of the `sendMessage` method.
    
    Docs:
        https://core.telegram.org/bots/api#sendmessage
    """

    @abstractmethod
    def send(
        self,
        bot_token: str,
        chat_id: int | str,
        text: str,
        parse_mode: str = '',
        disable_notification: bool = False,
        **params: Any
    ) -> None:
        """Send message via Telegram Bot API.
        
        Args:
            bot_token: Telegram bot API token.
            chat_id: Unique identifier for the target chat or username of the target channel (in
                the format `@channelusername`).
            text: Text of the message to be sent, 1-4096 characters after entities parsing.
            parse_mode: Mode for parsing entities in the message text.
            disable_notifications: Sends the message silently. Users will receive a notification
                with no sound.
            **params: Other parameters of the Telegram API method.

        Raises:
            SenderError: Error interacting with Telegram API.

        Docs:
            https://core.telegram.org/bots/api#sendmessage
        """
        pass

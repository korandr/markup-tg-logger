# markup-tg-logger
Flexible integration of Python's standard logging module and Telegram Bot API for logging to
Telegram chats or channels with built-in HTML support.

### Features
- Sending messages to multiple chats from a single handler.
- Ability to format log messages, `fmt` strings, stack and traceback output, or the final output.
- Full built-in HTML support. Extensible for Markdown and MarkdownV2 usage.
- Splitting long log entries into multiple messages that don't exceed Telegram's character limit
while maintaining valid markup during splitting.
- Configurable escaping of markup special characters at different formatting stages.
- Configurable notification disabling based on log level or other parameters.
- Choice of HTTP client library for Telegram Bot API interaction: `http.client` or `requests`.
  Option to install the library without dependencies.
- The library is fully documented in docstrings.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
    - [Minimal Example](#minimal-example)
    - [Using HTML Markup](#using-html-markup)
        - [Escaping](#escaping)
        - [Templates](#templates)
        - [Level Names](#level-names)
        - [Binding with Handler](#binding-with-handler)
    - [Notification Settings](#notification-settings)
    - [Splitting Long Texts](#splitting-long-texts)
    - [API Adapters](#api-adapters)
    - [Code of the given examples](#code-of-the-given-examples)
- [Documentation](#documentation)
    - [Structure](#structure)
    - [Markdown Support](#markdown-support)
- [Testing](#testing)
- [Useful Links](#useful-links)
- [Feedback](#feedback)

## Installation

Requires Python version 3.12+, 3.13 recommended.

Installation without dependencies:

```bash
pip install markup-tg-logger
```

Installation with `requests` library:

```bash
pip install markup-tg-logger[requests]
```

Import:

```python
import markup_tg_logger
```

## Quick Start

Basic knowledge of Python's standard `logging` library is recommended to work with this library.  
[Python logging Docs](https://docs.python.org/3/library/logging.html#module-logging)

### Minimal Example

`TelegramHandler` sends messages to a chat or channel via a Telegram bot. At minimum, you only
need to provide the bot token and the chat ID where logs will be sent.

```python
import logging

from markup_tg_logger import TelegramHandler


handler = TelegramHandler(
    bot_token = 'bot_token',
    chat_id = 12345,
)
handler.setLevel(logging.INFO)

logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('This message sended via markup-tg-logger')
```

You can also specify multiple recipients in `chat_id`, for example: `chat_id = {12345, '@logchannel'}`.

For private messages, `chat_id` is the same as `user_id`, which can be obtained through the Bot API.
For instance, you can use one of the currently available bots at the time of writing:   
[Show Json Bot](https://t.me/ShowJsonBot).

### Using HTML Markup

To control markup, configure and set the appropriate formatter in the handler. For most tasks,
`HtmlFormatter` is sufficient. In the following example, HTML is used in the `fmt` string.

```python
from markup_tg_logger import HtmlFormatter

FMT = (
    '<b>{levelname}</b>\n\n'
    '<u>{asctime}</u>\n\n'
    '<i>{message}</i>\n\n'
    '(Line: {lineno} [<code>{pathname}</code>])'
)

formatter = HtmlFormatter(
    fmt = FMT,
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{',
)
```

For more details about HTML in Telegram, read
[Bot API documentation](https://core.telegram.org/bots/api#html-style).

#### Escaping

By default, message text is escaped. If you want to use markup directly when calling the logger
(`logger.info('<code>example</code>')`), set the `escape_message=False` parameter in the
constructor of `HtmlFormatter`.

It's recommended to keep `escape_stack_info` and `escape_exception` parameters enabled, as stack
and traceback outputs typically contain `<` and `>` characters by default.

#### Templates

You can also wrap stack and/or traceback outputs in HTML templates. For this, specify
`stack_info_template` and `exception_template` parameters with a string like `<tag>{text}</tag>`.

Commonly used templates include:
- Monospace font: `<code>{text}</code>`
- Syntax-highlighted code block: `<pre><code class="language-python">{text}</code></pre>`

For convenience, you can import ready-made templates for Python and Bash code blocks:

```python
from markup_tg_logger.defaults import HTML_PYTHON_TEMPLATE, HTML_BASH_TEMPLATE
```

Alternatively, you can wrap the entire logger output in an HTML template using the `result_template`
parameter. In this case, the formatter will fully format the text (similar to standard
`logging.Formatter`), including stack and traceback outputs, and then insert the formatted text
into the specified template. It's recommended to enable `escape_result` and disable other `escape_*`
flags in this scenario.

#### Level Names

Telegram allows using emojis in messages, so by default level names are replaced with colored
emojis for better visual distinction between messages.

⬛️ - DEBUG   
⬜️ - INFO   
🟨 - WARNING   
🟥 - ERROR   
🟪 - CRITICAL   

You can override level names using the `level_names` parameter:

```python
formatter = HtmlFormatter(
    ...
    level_names = {logging.DEBUG: '⬛⬛️⬛️', logging.INFO: '⬜️⬜️⬜️'}
)
```

Levels not explicitly specified in the dictionary will keep their default names from the original
library. To reset all names to default, specify `level_names = {}`.

#### Binding with Handler

After configuring the formatter, set it to the `TelegramHandler` instance:

```python
...
handler.setFormatter(formatter)
```

### Notification Settings

You can enable or disable message notifications when creating the handler. This parameter is taken
directly from the Telegram Bot API. Notifications are enabled by default.

```python
handler = TelegramHandler(
    bot_token = 'bot_token',
    chat_id = 12345,
    disable_notification = True,
)
```

For more flexible configuration, you can pass an implementation of the `INotifier` interface to
`disable_notification` to control notifications. The library includes a ready-made `LevelNotifier`
class for enabling notifications when certain log levels are reached.

```python
from markup_tg_logger import LevelNotifier

handler = TelegramHandler(
    ...
    disable_notification = LevelNotifier(logging.ERROR),
)
```

### Splitting Long Texts

Telegram supports messages up to 4096 characters. Log entries may exceed this limit, especially
with long tracebacks. By default, `TelegramHandler` is configured to automatically split long texts
into multiple messages while preserving markup in each message.

To override this behavior, pass a reconfigured splitter factory to `message_splitter_factory`.

```python
from markup_tg_logger import MessageSplitterFactory
from markup_tg_logger.interfaces import IMessageSplitter

class CustomHtmlSplitter(IMessageSplitter):
    ...

handler = TelegramHandler(
    ...
    message_splitter_factory = MessageSplitterFactory({'HTML': CustomHtmlSplitter})
)
```

### API Adapters

You can choose an HTTP client for interacting with Telegram Bot API to better integrate with your
project's dependencies, or implement your own `ITelegramSender`.

Currently, the library includes implementations using:
- Python's standard `http.client`
- The popular third-party `requests` library

If the `requests` library is installed, `TelegramHandler` will use it by default automatically.

For more control, you can pass a sender instance to the `sender` parameter
when creating `TelegramHandler`.

```python
from markup_tg_logger import TelegramHandler
from markup_tg_logger.telegram_senders.http_client import HttpClientTelegramSender


handler = TelegramHandler(
    ...
    sender = HttpClientTelegramSender(),
)
```

### Code of the given examples

[Code for the examples shown](https://github.com/korandr/markup-tg-logger/tree/main/src/examples)

To run, set `BOT_TOKEN` and `CHAT_ID` environment variables.

## Documentation

The library is fully documented in docstrings.

### Structure

`markup_tg_logger/`
- `formatters/` - Classes based on `logging.Formatter`.
- `interfaces/` - Library interfaces for implementing custom classes.
- `message_splitters/` - Classes that split text with markup into messages
that do not exceeda given length.
- `notifiers/` - Classes that decide whether to turn on notifications in Telegram
depending on the `LogRecord` parameters.
- `telegram_senders/` - Classes that interact with the Telegram API.
Adapters for different HTTP libraries.
- `config.py` - Immutable data for the library.
- `defaults.py` - Some pre-configured values for class constructor parameters.
- `exceptions.py` - All library exceptions.
- `handler.py` - The central library class based on `logging.Handler`.
- `types.py` - Custom data types.

### Markdown Support

The library provides a built-in implementation for working with HTML only, but also provides an
interface-based API for implementing other markup languages.

For full Markdown support, `MarkdownMessageSplitter` should be implemented based on
`IMessageSplitter` to split messages while preserving markup.

```python
from markup_tg_logger import (
    TelegramHandler, EscapeMarkupFormatter,
    MessageSplitterFactory, BaseMessageSplitter, HtmlMessageSplitter,
)
from markup_tg_logger.interfaces import IMessageSplitter
from markup_tg_logger.types import ParseMode


class MarkdownMessageSplitter(IMessageSplitter):
    @property
    def parse_mode(self) -> ParseMode:
        return 'Markdown'
    
    def split(self, text: str) -> list[str]:
        ...

message_splitter_factory = MessageSplitterFactory(
    parse_mode_to_splitter = {
        '': BaseMessageSplitter(),
        'HTML': HtmlMessageSplitter(),
        'Markdown': MarkdownMessageSplitter(),
    }
)

formatter = EscapeMarkupFormatter(
    ...
    parse_mode = 'Markdown',
)

handler = TelegramHandler(
    ...
    message_splitter_factory = message_splitter_factory,
)
handler.setFormatter(formatter)
```

The `BaseMarkupFormatter` and `EscapeMarkupFormatter` classes are markup language independent
and can be used for Markdown without modification.

If you know for sure that your messages will not exceed the Telegram character limit, you can
immediately use Markdown in combination with `BaseMessageSplitter`.

```python
message_splitter_factory = MessageSplitterFactory(
    parse_mode_to_splitter = {
        '': BaseMessageSplitter(),
        'HTML': HtmlMessageSplitter(),
        'Markdown': BaseMessageSplitter(),
    }
)
```

## Testing

Installing dependencies for tests:

```bash
pip install -r requirements.txt
```

Running tests from the repository root:

```bash
pytest
```

## Useful Links

- [Python logging Docs](https://docs.python.org/3/library/logging.html#module-logging)
- [Telegram - Create Bot](https://core.telegram.org/bots/features#botfather)
- [Telegram Bot API - sendMessage](https://core.telegram.org/bots/api#sendmessage)
- [Telegram Bot API - HTML](https://core.telegram.org/bots/api#html-style)
- [Show Json Bot - Get user_id](https://t.me/ShowJsonBot)

## Feedback
Developer: Andrey Korovyansky | [andrey.korovyansky@gmail.com](mailto:andrey.korovyansky@gmail.com)

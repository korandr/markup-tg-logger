# markup-tg-logger
An extension to Python's standard logging module for logging to a Telegram chat or channel with built-in HTML support and the ability to add MarkdownV2.

[Read this in Russian](https://github.com/korandr/markup-tg-logger/blob/main/README.ru.md)

### Features
- Plain mode without markup.
- HTML formatting of the fmt string.
- Large text is automatically split into multiple messages according to the Telegram limit. Formatting is preserved.
- Disable escaping of special characters.
- Pre-configured formatters for markup in a code block of the entire message or only the call stack on error.
- Flexible modification of pre-configured behavior by creating child classes."

## Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Useful links](#useful-links)
- [Feedback](#feedback)

## Installation

Python version 3.9 or higher is required.

Installation from the PyPI repository:

```bash
pip install markup-tg-logger
```

Installation from a GitHub repository (requires pip version 20 and above).

```bash
pip install git+https://github.com/korandr/markup-tg-logger.git
```

Package import:

```python
import markup_tg_logger
```

## Quick Start

### HTML template

Example of setting up a Telegram logger with HTML formatting of the fmt template:

```python
import logging
from markup_tg_logger import HtmlTelegramFormatter, BaseTelegramHandler


BOT_TOKEN = 'bot_token_here'
CHAT_ID = 'user_id_or_channel_username'

FORMAT = '''<b>{levelname}</b>

<u>{asctime}</u>

<i>{message}</i>

<pre><code class="language-bash">(Line: {lineno} [{pathname}])</code></pre>
'''

formatter = HtmlTelegramFormatter(
    fmt = FORMAT,
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{',
)

handler = BaseTelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger('markup_tg_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('Hello HTML world! \n Any special characters: ><& <3')
```

When using `HtmlTelegramFormatter`, you can specify any HTML tags [supported by the Telegram API]((https://core.telegram.org/bots/api#html-style)) in the `fmt` string.       
At the same time, all characters `<`, `>` and `&` in the `message` string will be escaped and will not affect the markup. If you whant to change this behavior, you need to specify the `is_escape_markup=False` parameter in the constructor of the `HtmlTelegramFormatter` class.

The `HtmlTelegramFormatter` class allows you to customize the formatting of regular messages only. Traceback output will not be formatted. 

### Formatted traceback output

Example of setting up a Telegram logger with HTML formatting of the fmt template and formatted traceback output:

```python
import logging
from markup_tg_logger import HtmlTracebackTelegramFormatter, BaseTelegramHandler


BOT_TOKEN = 'bot_token_here'
CHAT_ID = 'user_id_or_channel_username'

formatter = HtmlTracebackTelegramFormatter(
    fmt = '<b>{levelname}</b>\n{asctime}\n\n{message}',
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{',
)

handler = BaseTelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)

handler.setLevel(logging.ERROR)
handler.setFormatter(formatter)

logger = logging.getLogger('markup_tg_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

try:
    raise ValueError('Error <description>')
except Exception as e:
    logger.exception(e)
```

The `HtmlTracebackTelegramFormatter` class works similarly to `HtmlTelegramFormatter`, but additionally formats the traceback string into a code block (`<pre><code class="language-python">...`)   

Please note that in this example, the logging level `ERROR` is also specified.   

You can also use the `CodeTelegramFormatter` class, which formats the entire logger output into a code block.   

### Notification control

Example of setting up a simple Telegram logger without markup and with notification control

```python
import time
import logging
from markup_tg_logger import BaseTelegramFormatter, BaseTelegramHandler, LevelNotifier


BOT_TOKEN = 'bot_token_here'
CHAT_ID = 'user_id_or_channel_username'

formatter = BaseTelegramFormatter(
    fmt = '{levelname}\n{asctime}\n\n{message}',
    datefmt = '%d-%m-%Y %H:%M:%S',
    style = '{'
)

handler = BaseTelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
    disable_notification = LevelNotifier(logging.ERROR)
)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger('markup_tg_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('Message without notification')
time.sleep(5)
logger.critical('Important notification message')
```

The `disable_notification` argument can accept either a `bool` value (according to the Telegram Bot API) or an `INotifier` interface object.   
In this case, a `LevelNotifier` object with the level `ERROR` is passed, so notifications will only be sent for the `ERROR` level and above.    


[See the code from the examples](https://github.com/korandr/markup-tg-logger/tree/main/src/examples)

## Documentation

[Here](https://github.com/korandr/markup-tg-logger/wiki) you can find the documentation for the library.

## Useful links

- [Python logging Docs](https://docs.python.org/3/library/logging.html#module-logging)
- [Python logging Docs - Handler](https://docs.python.org/3/library/logging.html#handler-objects)
- [Python logging Docs - Formatter](https://docs.python.org/3/library/logging.html#formatter-objects)
- [Telegram - Create Bot](https://core.telegram.org/bots/features#botfather)
- [Telegram Bot API - HTML](https://docs.python.org/3/library/logging.html#module-logging)
- [Telegram Bot API - sendMessage](https://core.telegram.org/bots/api#sendmessage)
- [Show Json Bot - Get user_id](https://t.me/ShowJsonBot)


## Feedback
Developer: Andrey Korovyanskiy | [andrey.korovyansky@gmail.com](mailto:andrey.korovyansky@gmail.com) 

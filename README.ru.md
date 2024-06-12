# markup-tg-logger
Расширение стандартного модуля python logging для логгирования в чат или канал Telegram со встроенной поддержкой HTML и возможностью замены на MarkdownV2.

### Особенности
- Простой режим без разметки.
- HTML разметка строки fmt.
- Большой текст автоматически разделяется на несколько сообщений в соответствии с лимитом Telegram. Разметка при этом сохраняется. 
- Отключаемое экранирование служебных символов.
- Преднастроенные форматтеры для разметки в блок кода всего сообщения или только стэка вызовов при ошибке.
- Гибкое изменение преднастроенного поведения за счёт создания дочерних классов.

## Содержание
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Документация](#документация)
- [Полезные ссылки](#полезные-ссылки)
- [Обратная связь](#обратная-связь)

## Установка

Требуется python версии 3.9 и выше.

Из репозитория PyPI:

```bash
pip install markup-tg-logger
```

Установка из github-репозитория (необходим pip версии 20 и выше)

```bash
pip install git+https://github.com/korandr/markup-tg-logger.git
```

Импорт

```python
import markup_tg_logger
```

## Быстрый старт

### HTML шаблон

Пример настройки Telegram логгера с HTML разметкой fmt-шаблона

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

При использовании `HtmlTelegramFormatter` в строке `fmt` можно указывать любые HTML теги, [которые поддерживает Telegram API](https://core.telegram.org/bots/api#html-style).    
При этом все символы `<`, `>` и `&` в строке `message` будут экранированы и не повлияют на разметку. Чтобы изменить это поведение, необходимо указать в конструкторе класса `HtmlTelegramFormatter` параметр `is_escape_markup=False`.

Класс `HtmlTelegramFormatter` позволяет настраивать только форматирование обычных сообщений. Traceback вывод форматироваться не будет.  

### Форматирование Traceback

Пример настройки Telegram логгера с HTML разметкой fmt-шаблона и форматированным Traceback выводом.

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

Класс `HtmlTracebackTelegramFormatter` работает аналогично `HtmlTelegramFormatter`, но дополнительно форматирует Traceback строку в блок с кодом (`<pre><code class="language-python">...`)

Обратите внимание, что в данном примере также задан уровень логгирования `ERROR`.

Также можно использовать класс `CodeTelegramFormatter`, который форматирует в блок с кодом не только traceback вывод, но и вообще весь вывод логгера.

### Настройка уведомлений

Пример настройки простого Telegram логгера без разметки с управлением уведомлениями

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

В качестве аргумента `disable_notification` можно передать значение `bool` (согласно Telegram Bot API) или объект интерфейса `INotifier`.   
В данном случае передан объект `LevelNotifier` с уровнем `ERROR`, поэтому уведомления будут приходить только при уровне `ERROR` и выше.    


[Код приведённых примеров](https://github.com/korandr/markup-tg-logger/tree/main/src/examples)

## Документация

[Здесь](https://github.com/korandr/markup-tg-logger/wiki) можно ознакомиться с документацией к бибиотеке.

## Полезные ссылки

- [Python logging Docs](https://docs.python.org/3/library/logging.html#module-logging)
- [Python logging Docs - Handler](https://docs.python.org/3/library/logging.html#handler-objects)
- [Python logging Docs - Formatter](https://docs.python.org/3/library/logging.html#formatter-objects)
- [Telegram - Create Bot](https://core.telegram.org/bots/features#botfather)
- [Telegram Bot API - HTML](https://docs.python.org/3/library/logging.html#module-logging)
- [Telegram Bot API - sendMessage](https://core.telegram.org/bots/api#sendmessage)
- [Show Json Bot - Get user_id](https://t.me/ShowJsonBot)


## Обратная связь
Разработчик: Андрей Коровянский | [andrey.korovyansky@gmail.com](mailto:andrey.korovyansky@gmail.com) 

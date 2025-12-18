# markup-tg-logger сhangelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]

### Added
- Full configuration support via
  [`logging.config.dictConfig`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig).
  All arguments of the `TelegramHandler` class constructor now support serializable values ​​from the
  configuration dictionary. Class imports are resolved from string paths using the standard
  logging import resolver.
- Now several ids can be passed to the `chat_id` argument of the `TelegramHandler` constructor
  not only as a set, but also as a list. The passed list will be converted into a set to avoid
  duplication of messages to one recipient.
- Added an [example](https://github.com/korandr/markup-tg-logger/tree/main/src/examples/config_example.py)
  of configuring a logger from a dictionary. More detailed examples of configuration have been
  added to `README.md`.

### Changed
- Improved handling of malformed HTML code when splitting text into messages using
  `HtmlMessageSplitter`. Now throws explicit, informative exceptions when encountering issues
  like improper escaping. Error messages include the problematic character, its position,
  surrounding context, and the full text for easier debugging.

## Fixed
- Fixed HTML attribute parsing to support valueless attributes. Currently, Telegram supports only
  one such attribute, `expandable` in the `blockquote` tag. Tags containing such attributes
  previously caused a `HtmlMessageSplitter` failure.


## [1.0.0] - 2025-07-16
- [Github](https://github.com/korandr/markup-tg-logger/releases/tag/v1.0.0)
- [PyPI](https://pypi.org/project/markup-tg-logger/1.0.0/)

Changelog is maintained from stable version 1.0.0.
Previous beta versions (0.1.x) contained experimental features and are not recommended for use.

### Key Features

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

# markup-tg-logger сhangelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

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

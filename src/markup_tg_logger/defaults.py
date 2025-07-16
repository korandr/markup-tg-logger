import logging


HTML_PYTHON_TEMPLATE = '<pre><code class="language-python">{text}</code></pre>'
HTML_BASH_TEMPLATE = '<pre><code class="language-bash">{text}</code></pre>'

DEFAULT_LEVEL_NAMES: dict[int, str] = {
        logging.DEBUG:    '⬛️ DEBUG ⬛️',
        logging.INFO:     '⬜️ INFO ⬜️',
        logging.WARNING:  '🟨 WARNING 🟨',
        logging.ERROR:    '🟥 ERROR 🟥',
        logging.CRITICAL: '🟪 CRITICAL 🟪',
    }

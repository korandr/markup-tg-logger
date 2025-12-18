from logging.config import BaseConfigurator 
from typing import Any, TypeVar

from .exceptions import MarkupTgLoggerException


_T = TypeVar('_T')

_configurator = BaseConfigurator({})

def resolve_object_from_config(value: dict[str, Any], expected_type: type[_T]) -> _T:
    """Import and create an object described in a dictionary in the user-defined object format.

    Docs:
        https://docs.python.org/3/library/logging.config.html#user-defined-objects

    The dictionary must contain the `'()'` key with the import path for the requested class as a
    string. The remaining dictionary keys will be passed to the constructor of the specified class.
    The standard logging `'.'` special key is not supported, define a custom factory if needed.
    
    For example: `{'()': 'markup_tg_logger.LevelNotifier', 'level': 'ERROR'}`.

    Args:
        value: Configuration dictionary.
        expected_type: Type of the object to import and create.

    Raises:
        MarkupTgLoggerException: The dictionary does not contain the `'()'` key or created
            object is not an instance of `expected_type`.
    """

    if not '()' in value:
        raise MarkupTgLoggerException('The configuration dictionary must contain the `"()"` key.')

    class_path: str = value.pop('()')
    cls = _configurator.resolve(class_path)
    obj = cls(**value)

    if not isinstance(obj, expected_type):
        raise MarkupTgLoggerException(
            f'Expected {expected_type.__name__}, but got {cls.__name__}. '
            f'Check the valid types for specfied argument.'
        )
    
    return obj

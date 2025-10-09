"""
Internationalization (i18n) Module
Handles multi-language support and translations
"""

from .translator import (
    Translator,
    get_translator,
    set_language,
    translate,
    t,
)

__all__ = [
    "Translator",
    "get_translator",
    "set_language",
    "translate",
    "t",
]

"""
Internationalization (i18n) System for Encrypt-D
Provides multi-language support for the user interface
"""

import json
import locale
from pathlib import Path
from typing import Dict, Optional


class Translator:
    """Manages translations and language switching"""

    def __init__(self, default_language: str = "en"):
        """
        Initialize the translator

        Args:
            default_language: Default language code (en, es)
        """
        # The translation files are in the same directory as this file
        self.i18n_dir = Path(__file__).parent
        self.i18n_dir.mkdir(exist_ok=True)

        self.default_language = default_language
        self.current_language = default_language
        self.translations: Dict[str, Dict] = {}

        # Load available languages
        self._load_all_languages()

        # Auto-detect system language
        self._detect_system_language()

    def _load_all_languages(self):
        """Load all available translation files"""
        for lang_file in self.i18n_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load language file {lang_file}: {e}")

    def _detect_system_language(self):
        """Detect and set system language if available"""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                lang_code = system_locale.split("_")[0].lower()
                if lang_code in self.translations:
                    self.current_language = lang_code
        except Exception as e:
            print(f"Warning: Language detection failed: {e}")

    def set_language(self, language_code: str) -> bool:
        """
        Set the current language

        Args:
            language_code: Language code to set (e.g., 'en', 'es')

        Returns:
            True if successful, False if language not available
        """
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False

    def get(self, key: str, **kwargs) -> str:
        """
        Get translated string by key

        Args:
            key: Translation key (e.g., 'app.title', 'error.invalid_password')
            **kwargs: Format arguments for string formatting

        Returns:
            Translated string or key if translation not found
        """
        # Try current language
        text = self._get_nested(self.translations.get(self.current_language, {}), key)

        # Fallback to default language
        if text is None and self.current_language != self.default_language:
            text = self._get_nested(
                self.translations.get(self.default_language, {}), key
            )

        # Fallback to key itself
        if text is None:
            return key

        # Format with arguments if provided
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text

        return text

    def _get_nested(self, dictionary: dict, key: str) -> Optional[str]:
        """
        Get value from nested dictionary using dot notation

        Args:
            dictionary: Dictionary to search
            key: Dot-separated key (e.g., 'error.invalid_password')

        Returns:
            Value if found, None otherwise
        """
        keys = key.split(".")
        value = dictionary

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None

        return value if isinstance(value, str) else None

    def get_available_languages(self) -> Dict[str, str]:
        """
        Get available languages with their names

        Returns:
            Dictionary mapping language codes to language names
        """
        languages = {}
        for lang_code in self.translations.keys():
            lang_name = self.get(f"language.{lang_code}")
            languages[lang_code] = lang_name if lang_name else lang_code.upper()
        return languages

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language


# Global translator instance
_translator: Optional[Translator] = None


def get_translator() -> Translator:
    """
    Get or create the global translator instance

    Returns:
        Global Translator instance
    """
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def set_language(language_code: str) -> bool:
    """
    Set the global translator language

    Args:
        language_code: Language code to set

    Returns:
        True if successful
    """
    return get_translator().set_language(language_code)


def translate(key: str, **kwargs) -> str:
    """
    Shortcut function for translation

    Args:
        key: Translation key
        **kwargs: Format arguments

    Returns:
        Translated string
    """
    return get_translator().get(key, **kwargs)


# Alias for shorter usage
t = translate

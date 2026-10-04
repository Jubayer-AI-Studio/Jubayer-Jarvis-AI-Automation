"""
Language Loader for JARVIS-AETHER
Provides clean modular loading of language packs.
"""

from . import bangla, english, urdu, arabic, banglish

AVAILABLE_LANGUAGES = {
    "BANGLA": bangla,
    "ENGLISH": english,
    "BANGLISH": banglish,
    "URDU": urdu,
    "ARABIC": arabic
}

def load_language(name="BANGLA"):
    """Loads the requested language pack. Defaults to BANGLA."""
    name_key = name.upper()
    return AVAILABLE_LANGUAGES.get(name_key, bangla)

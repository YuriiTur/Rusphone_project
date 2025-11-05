import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from key_type3 import KeyboardAnalyzer, get_common_chars


@pytest.fixture
def analyzer():
    return KeyboardAnalyzer("qwerty")


@pytest.fixture
def short_text():
    return "привет мир"

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.key_typ3 import KeyboardAnalyzer


@pytest.fixture
def standard_analyzer():
    return KeyboardAnalyzer("standard")


@pytest.fixture
def challenge_analyzer():
    return KeyboardAnalyzer("challenge")


@pytest.fixture
def rusphone_analyzer():
    return KeyboardAnalyzer("rusphone")


@pytest.fixture
def short_text():
    return "привет мир тестирование"


@pytest.fixture
def files_exist():
    """Проверяет наличие файлов данных"""
    files = ["voina-i-mir.txt", "digramms.txt", "1grams-3.txt"]
    return [f for f in files if os.path.exists(f)]

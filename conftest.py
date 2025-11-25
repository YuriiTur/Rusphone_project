import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from key_type3 import KeyboardAnalyzer, get_common_chars

# ВЫХОД: Система готова к импорту модулей проекта и использованию pytest


# ВХОД: Создание фикстуры analyzer с раскладкой qwerty для тестов
@pytest.fixture
def analyzer():
    return KeyboardAnalyzer("qwerty")


# ВЫХОД: Готовый анализатор клавиатуры для использования в тестах


# ВХОД: Создание фикстуры short_text с тестовым русским текстом
@pytest.fixture
def short_text():
    return "привет мир"


# ВЫХОД: Тестовый текст для анализа в тестах

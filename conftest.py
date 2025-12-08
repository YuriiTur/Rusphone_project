# ВХОД: Настройка окружения pytest и импорт модулей новой лабораторной работы
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.keyboard_analyzer import KeyboardAnalyzer
from modules.utils import get_available_texts, get_available_layouts

# ВЫХОД: Система готова к импорту модулей лабораторной работы


# ВХОД: Создание фикстуры analyzer с раскладкой ytsuken для тестирования
@pytest.fixture
def analyzer():
    return KeyboardAnalyzer(layout_name="ytsuken")


# ВЫХОД: Готовый анализатор клавиатуры с загруженной раскладкой


# ВХОД: Создание фикстуры с коротким русским текстом для тестов
@pytest.fixture
def short_text():
    return "привет мир тестирование"


# ВЫХОД: Тестовый текст для анализа клавиатурных раскладок


# ВХОД: Создание фикстуры с текстом содержащим биграммы
@pytest.fixture
def digram_text():
    return "то но ро го ка от ва ор"


# ВЫХОД: Текст с биграммами для анализа переборов пальцев


# ВХОД: Создание фикстуры для имитации папки с текстами
@pytest.fixture
def mock_texts_dir(tmpdir):
    texts_dir = tmpdir.mkdir("texts")
    texts_dir.join("test1.txt").write("тестовый текст 1")
    texts_dir.join("test2.txt").write("тестовый текст 2")
    return str(texts_dir)


# ВЫХОД: Временная папка с тестовыми файлами для проверки утилит

# ВХОД: Импорт утилит для работы с файлами и раскладками
import pytest
import os
from utils import get_available_texts, get_available_layouts

# ВЫХОД: Система готова к тестированию вспомогательных функций


class TestUtils:

    # ВХОД: Поиск текстовых файлов в указанной директории
    def test_get_available_texts(self, mock_texts_dir):
        texts = get_available_texts(mock_texts_dir)
        assert isinstance(texts, list)
        assert len(texts) == 2
        assert texts[0][0].endswith("test1.txt")

    # ВЫХОД: Найдены все текстовые файлы с правильными именами

    # ВХОД: Получение списка доступных клавиатурных раскладок
    def test_get_available_layouts(self):
        layouts = get_available_layouts()
        assert isinstance(layouts, list)
        assert len(layouts) > 0
        assert ("ytsuken", "ЙЦУКЕН") in layouts

    # ВЫХОД: Список содержит основные раскладки с правильными кодами и названиями

    # ВХОД: Проверка обработки отсутствующей директории с текстами
    def test_get_available_texts_empty_dir(self):
        texts = get_available_texts("nonexistent_directory")
        assert texts == []

    # ВЫХОД: Пустой список при отсутствии директории

    # ВХОД: Проверка фильтрации только текстовых файлов
    def test_get_available_texts_only_txt(self, tmpdir):
        texts_dir = tmpdir.mkdir("mixed")
        texts_dir.join("test.txt").write("текст")
        texts_dir.join("test.py").write("код")
        texts = get_available_texts(str(texts_dir))
        assert len(texts) == 1
        assert texts[0][0].endswith("test.txt")

    # ВЫХОД: Только .txt файлы включены в список

import pytest
import os
from key_type3 import KeyboardAnalyzer, get_common_chars


class TestKeyboardAnalyzer:
    """Минимальные тесты для всех функций"""

    def test_init(self):
        """Тест инициализации анализатора"""
        analyzer = KeyboardAnalyzer("qwerty")
        assert analyzer.layout == "qwerty"
        assert hasattr(analyzer, "keys")
        assert hasattr(analyzer, "keyboard_map")

    def test_calculate_shtraf(self, analyzer):
        """Тест расчета штрафа"""
        # Домашний ряд - штраф 0
        key_code, finger = analyzer.keys["ф"]
        shtraf = analyzer._calculate_shtraf(key_code, finger)
        assert shtraf == 0

        # Верхний ряд - штраф >= 1
        key_code, finger = analyzer.keys["й"]
        shtraf = analyzer._calculate_shtraf(key_code, finger)
        assert shtraf >= 1

    def test_load_text_file(self, analyzer):
        """Тест загрузки файла"""
        # Создаем временный файл
        test_content = "тест"
        test_file = "test_temp.txt"

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        try:
            loaded = analyzer._load_text_file(test_file)
            assert loaded == test_content
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_analyze_text(self, analyzer, short_text):
        """Тест анализа текста"""
        result = analyzer.analyze_text(short_text, "test")

        assert result["text_name"] == "test"
        assert result["layout"] == "qwerty"
        assert result["characters_analyzed"] > 0
        assert result["average_penalty"] >= 0

    def test_analyze_all_files(self, analyzer):
        """Тест анализа всех файлов"""
        results = analyzer.analyze_all_files()
        assert isinstance(results, list)

    def test_print_results(self, analyzer, short_text):
        """Тест вывода результатов"""
        result = analyzer.analyze_text(short_text, "test")
        results_list = [result]

        # Проверяем что функция не падает
        try:
            analyzer.print_results(results_list)
            assert True
        except Exception:
            pytest.fail("print_results упал")

    def test_get_common_chars(self):
        """Тест получения общих символов"""
        common_chars = get_common_chars()
        assert isinstance(common_chars, set)
        assert "а" in common_chars
        assert " " in common_chars


class TestArguments:
    """2 теста на аргументы функций"""

    def test_analyze_text_arguments(self, analyzer):
        """Тест аргументов analyze_text"""
        # Пустой текст
        result = analyzer.analyze_text("", "test")
        assert result is None

        # С общими символами
        result = analyzer.analyze_text("привет123", "test", set("привет"))
        assert result["characters_analyzed"] == 6

    def test_analyze_all_files_arguments(self, analyzer):
        """Тест аргументов analyze_all_files"""
        # С общими символами
        results = analyzer.analyze_all_files(set("абвгд"))
        assert isinstance(results, list)

        # Без аргументов
        results = analyzer.analyze_all_files()
        assert isinstance(results, list)


class TestLayouts:
    """Тесты разных раскладок"""

    def test_vyzov_layout(self):
        """Тест раскладки Вызов"""
        analyzer = KeyboardAnalyzer("vyzov")
        assert analyzer.layout == "vyzov"
        assert "б" in analyzer.keys

    def test_rusphone_layout(self):
        """Тест фонетической раскладки"""
        analyzer = KeyboardAnalyzer("rusphone")
        assert analyzer.layout == "rusphone"
        assert "я" in analyzer.keys

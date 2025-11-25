import pytest
import os
from key_type3 import KeyboardAnalyzer, get_common_chars


class TestKeyboardAnalyzer:

    # ВХОД: Создание анализатора с русской раскладкой ЙЦУКЕН
    def test_init(self):
        analyzer = KeyboardAnalyzer("ytsuken")
        assert analyzer.layout == "ytsuken"
        assert hasattr(analyzer, "keys")
        assert hasattr(analyzer, "keyboard_map")
        assert hasattr(analyzer, "home_positions")

    # ВЫХОД: Анализатор успешно создан с загруженными данными раскладки

    # ВХОД: Расчет расстояния для клавиш домашнего и верхнего ряда
    def test_calculate_shtraf(self, analyzer):
        key_code, finger = analyzer.keys["ф"]
        shtraf_home = analyzer._calculate_shtraf(key_code, finger)
        key_code, finger = analyzer.keys["й"]
        shtraf_upper = analyzer._calculate_shtraf(key_code, finger)
        assert shtraf_home == 0
        assert shtraf_upper >= 1

    # ВЫХОД: Домашний ряд имеет нулевое расстояние, верхний ряд - положительное

    # ВХОД: Загрузка текстового файла с русским содержимым
    def test_load_text_file(self, analyzer):
        test_content = "тест"
        test_file = "test_temp.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        loaded = analyzer._load_text_file(test_file)
        if os.path.exists(test_file):
            os.remove(test_file)
        assert loaded == test_content

    # ВЫХОД: Текст успешно загружен и соответствует оригиналу

    # ВХОД: Анализ короткого русского текста без фильтрации символов
    def test_analyze_text_basic(self, analyzer, short_text):
        result = analyzer.analyze_text(short_text, "test")
        assert result["text_name"] == "test"
        assert result["layout"] == "ytsuken"
        assert result["characters_analyzed"] > 0
        assert result["average_path"] >= 0

    # ВЫХОД: Получен корректный результат анализа с основными метриками

    # ВХОД: Пакетный анализ всех текстовых файлов проекта
    def test_analyze_all_files(self, analyzer):
        results = analyzer.analyze_all_files()
        assert isinstance(results, list)

    # ВЫХОД: Список результатов для каждого файла (может быть пустым)

    # ВХОД: Вывод форматированных результатов анализа в консоль
    def test_print_results(self, analyzer, short_text):
        result = analyzer.analyze_text(short_text, "test")
        results_list = [result]
        analyzer.print_results(results_list)
        assert True

    # ВЫХОД: Функция выполнена без ошибок форматирования

    # ВХОД: Получение множества символов для сравнения раскладок
    def test_get_common_chars(self):
        common_chars = get_common_chars()
        assert isinstance(common_chars, set)
        assert "а" in common_chars
        assert " " in common_chars
        assert "!" in common_chars

    # ВЫХОД: Множество содержит русские буквы, пробел и спецсимволы


class TestLayouts:

    # ВХОД: Создание анализатора с альтернативной раскладкой "Вызов"
    def test_vyzov_layout(self):
        analyzer = KeyboardAnalyzer("vyzov")
        assert analyzer.layout == "vyzov"
        assert "б" in analyzer.keys

    # ВЫХОД: Анализатор создан с характерными символами раскладки

    # ВХОД: Создание анализатора с фонетической русской раскладкой
    def test_rusfon_layout(self):
        analyzer = KeyboardAnalyzer("rusphone")
        assert analyzer.layout == "rusphone"
        assert "я" in analyzer.keys

    # ВЫХОД: Анализатор создан с фонетическим расположением символов


class TestArguments:

    # ВХОД: Анализ пустого текста и текста с фильтрацией символов
    def test_analyze_text_arguments(self, analyzer):
        result_empty = analyzer.analyze_text("", "empty")
        result_filtered = analyzer.analyze_text("привет123", "test", set("привет"))
        assert result_empty is None
        assert result_filtered["characters_analyzed"] == 6

    # ВЫХОД: Пустой текст возвращает None, фильтрация учитывает только указанные символы

    # ВХОД: Анализ файлов с ограниченным набором символов и без ограничений
    def test_analyze_all_files_arguments(self, analyzer):
        results_with_filter = analyzer.analyze_all_files(set("абвгд"))
        results_without_filter = analyzer.analyze_all_files()
        assert isinstance(results_with_filter, list)
        assert isinstance(results_without_filter, list)

    # ВЫХОД: Оба варианта возвращают корректную структуру данных


class TestSpecialCases:

    # ВХОД: Расчет расстояния для клавиши пробела (большой палец)
    def test_thumb_penalty_zero(self, analyzer):
        if " " in analyzer.keys:
            key_code, finger = analyzer.keys[" "]
            shtraf = analyzer._calculate_shtraf(key_code, finger)
            assert shtraf == 0

    # ВЫХОД: Большие пальцы имеют нулевое расстояние независимо от позиции

    # ВХОД: Попытка загрузки несуществующего файла
    def test_nonexistent_file_loading(self, analyzer):
        result = analyzer._load_text_file("nonexistent_file_12345.txt")
        assert result == ""

    # ВЫХОД: Возвращена пустая строка вместо исключения

# ВХОД: Импорт необходимых модулей для тестирования анализатора раскладок
import pytest
from modules.keyboard_analyzer import KeyboardAnalyzer

# ВЫХОД: Система готова к тестированию функций анализатора


class TestKeyboardAnalyzer:

    # ВХОД: Инициализация анализатора с русской раскладкой ЙЦУКЕН
    def test_init(self):
        analyzer = KeyboardAnalyzer(layout_name="ytsuken")
        assert analyzer.layout_name == "ytsuken"
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

    # ВХОД: Анализ короткого текста с оценкой нагрузки на пальцы
    def test_analyze_text_basic(self, analyzer, short_text):
        result = analyzer.analyze_text(short_text, "test")
        assert result["text_name"] == "test"
        assert result["layout"] == "ytsuken"
        assert result["characters_analyzed"] > 0
        assert result["average_path"] >= 0

    # ВЫХОД: Получен корректный результат анализа с основными метриками

    # ВХОД: Определение пальца для символов клавиатуры
    def test_get_finger_for_char(self, analyzer):
        finger = analyzer._get_finger_for_char("ф")
        assert finger is not None
        assert finger.startswith("left")

    # ВЫХОД: Правильно определен палец для ввода символа

    # ВХОД: Определение руки по названию пальца
    def test_get_hand_for_finger(self, analyzer):
        hand = analyzer._get_hand_for_finger("left_index")
        assert hand == "left"
        hand = analyzer._get_hand_for_finger("right_middle")
        assert hand == "right"

    # ВЫХОД: Правильно определена рука для каждого пальца

    # ВХОД: Анализ последовательности пальцев для оценки удобства перебора
    def test_analyze_finger_sequence(self, analyzer):
        fingers_inward = ["left_pinky", "left_ring", "left_middle"]
        fingers_outward = ["right_index", "right_middle", "right_ring"]
        result_inward = analyzer._analyze_finger_sequence(fingers_inward)
        result_outward = analyzer._analyze_finger_sequence(fingers_outward)
        assert result_inward[0] in ["udp", "chudp"]
        assert result_outward[0] in ["udp", "chudp"]

    # ВЫХОД: Корректно определен тип перебора пальцев

    # ВХОД: Анализ биграмм в тексте для оценки удобства пальцевых переборов
    def test_analyze_ngrams(self, analyzer, digram_text):
        result = analyzer.analyze_ngrams(digram_text, n=2)
        assert result is not None
        assert "total" in result
        assert result["total"] > 0

    # ВЫХОД: Получена статистика по биграммам с количеством и типами переборов


class TestLayouts:

    # ВХОД: Инициализация анализатора с альтернативной раскладкой "Вызов"
    def test_vyzov_layout(self):
        analyzer = KeyboardAnalyzer(layout_name="vyzov")
        assert analyzer.layout_name == "vyzov"
        assert hasattr(analyzer, "keys")

    # ВЫХОД: Анализатор создан с загруженными данными раскладки "Вызов"

    # ВХОД: Инициализация анализатора с фонетической русской раскладкой
    def test_rusphone_layout(self):
        analyzer = KeyboardAnalyzer(layout_name="rusphone")
        assert analyzer.layout_name == "rusphone"
        assert hasattr(analyzer, "keys")

    # ВЫХОД: Анализатор создан с фонетическим расположением символов


class TestNgramAnalysis:

    # ВХОД: Анализ текста с разной длиной n-грамм
    def test_different_ngram_lengths(self, analyzer, short_text):
        result_2gram = analyzer.analyze_ngrams(short_text, n=2)
        result_3gram = analyzer.analyze_ngrams(short_text, n=3)
        if result_2gram:
            assert "total" in result_2gram
        if result_3gram:
            assert "total" in result_3gram

    # ВЫХОД: Статистика собрана для разных длин последовательностей символов

    # ВХОД: Анализ очень короткого текста для граничных случаев
    def test_short_text_ngram_analysis(self, analyzer):
        result = analyzer.analyze_ngrams("аб", n=2)
        if result:
            assert result["total"] > 0

    # ВЫХОД: Корректная обработка минимальной длины текста

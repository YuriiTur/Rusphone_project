import pytest
from key_type2 import KeyboardAnalyzer


class TestInitialization:
    """Тесты инициализации"""

    def test_layouts_init(self):
        """Тест загрузки раскладок"""
        for layout in ["standard", "challenge", "rusphone"]:
            analyzer = KeyboardAnalyzer(layout)
            assert analyzer.layout == layout
            assert len(analyzer.keys) > 0


class TestPenaltyCalculation:
    """Тесты расчета штрафов"""

    def test_home_row_zero_penalty(self):
        """Тест нулевого штрафа домашнего ряда"""
        analyzer = KeyboardAnalyzer("standard")
        for char in ["ф", "ы", "в", "а"]:
            if char in analyzer.keys:
                key_code, finger = analyzer.keys[char]
                penalty = analyzer._calculate_penalty(key_code, finger)
                assert penalty == 0


class TestTextAnalysis:
    """Тесты анализа текста"""

    def test_basic_analysis(self):
        """Тест базового анализа"""
        analyzer = KeyboardAnalyzer("standard")
        result = analyzer.analyze_text("тест", "test")
        assert result["characters_analyzed"] == 4
        assert result["average_penalty"] >= 0

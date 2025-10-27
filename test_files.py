import pytest
import os
from key_type2 import KeyboardAnalyzer


class TestFileAnalysis:
    """Тесты анализа файлов"""

    def test_analyze_all_files(self, standard_analyzer, files_exist):
        """Тест метода analyze_all_files"""
        if files_exist:
            results = standard_analyzer.analyze_all_files()
            assert isinstance(results, list)

    def test_digrams_analysis(self, standard_analyzer):
        """Тест анализа диграмм"""
        if os.path.exists("digramms.txt"):
            with open("digramms.txt", "r", encoding="utf-8") as f:
                text = f.read()
            result = standard_analyzer.analyze_text(text, "digrams")
            assert result["characters_analyzed"] > 0


class TestLargeTextAnalysis:
    """Тесты больших текстов"""

    def test_war_and_peace(self, standard_analyzer):
        """Тест Войны и мира"""
        if os.path.exists("voina-i-mir.txt"):
            with open("voina-i-mir.txt", "r", encoding="utf-8") as f:
                text = f.read()
            result = standard_analyzer.analyze_text(text, "war_peace")
            assert result["characters_analyzed"] > 1000


class TestWorkflow:
    """Тесты рабочего процесса"""

    def test_common_chars(self, standard_analyzer):
        """Тест с общими символами"""
        common_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
        results = standard_analyzer.analyze_all_files(common_chars)
        assert isinstance(results, list)

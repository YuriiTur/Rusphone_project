"""
Базовый класс для всех раскладок клавиатуры
"""


class KeyboardLayout:
    """Базовый класс раскладки клавиатуры"""

    def __init__(self):
        self.keys = {}
        self.caps_keys = {}
        self.shift_keys = {}
        self.alt_keys = {}
        self.home_positions = {}
        self.display_name = "Базовая раскладка"
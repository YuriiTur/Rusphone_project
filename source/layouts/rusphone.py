"""
Модуль раскладки РУСФОН
"""

from .base import KeyboardLayout


class RusphoneLayout(KeyboardLayout):
    """Класс раскладки РУСФОН"""

    def __init__(self):
        super().__init__()
        self.display_name = "РУСФОН"
        self._init_layout()

    def _init_layout(self):
        """Инициализация раскладки РУСФОН"""
        self.keys = {
            'я': (16, 'left_pinky'), 'в': (17, 'left_ring'), 'е': (18, 'left_middle'),
            'р': (19, 'left_index'), 'т': (20, 'left_index'), 'ы': (21, 'left_index'),
            'у': (22, 'left_index'), 'и': (23, 'right_index'), 'о': (24, 'right_index'),
            'п': (25, 'right_index'), 'ш': (26, 'right_index'), 'щ': (27, 'right_index'),
            'а': (30, 'left_pinky'), 'с': (31, 'left_ring'), 'д': (32, 'left_middle'),
            'ф': (33, 'left_index'), 'г': (34, 'left_index'), 'х': (35, 'right_middle'),
            'й': (36, 'right_middle'), 'к': (37, 'right_middle'), 'л': (38, 'right_ring'),
            ';': (39, 'right_ring'), "'": (40, 'right_ring'),
            'з': (44, 'left_pinky'), 'ь': (45, 'left_ring'), 'ц': (46, 'left_middle'),
            'ж': (47, 'left_index'), 'б': (48, 'right_pinky'), 'н': (49, 'right_pinky'),
            'м': (50, 'right_pinky'), ',': (51, 'right_pinky'), '.': (52, 'right_pinky'),
            '/': (53, 'right_pinky'),
            'э': (43, 'right_index'), 'ю': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        self.shift_keys = {
            '!': (2, 'left_pinky'), '@': (3, 'left_ring'), 'ё': (4, 'left_middle'),
            'Ё': (5, 'left_index'), 'ъ': (6, 'right_index'), 'Ъ': (7, 'right_middle'),
            '&': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), 'ч': (13, 'right_pinky'),
            ':': (39, 'right_ring'), '"': (40, 'right_ring'), '<': (51, 'right_pinky'),
            '>': (52, 'right_pinky'), '?': (53, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }
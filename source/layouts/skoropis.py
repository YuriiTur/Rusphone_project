"""
Модуль раскладки СКОРОПИСЬ
"""

from .base import KeyboardLayout


class SkoropisLayout(KeyboardLayout):
    """Класс раскладки СКОРОПИСЬ"""

    def __init__(self):
        super().__init__()
        self.display_name = "СКОРОПИСЬ"
        self._init_layout()

    def _init_layout(self):
        """Инициализация раскладки СКОРОПИСЬ"""
        self.keys = {
            'ц': (16, 'left_pinky'), 'ь': (17, 'left_ring'), 'я': (18, 'left_middle'),
            ',': (19, 'left_index'), '.': (20, 'left_index'), 'з': (21, 'left_index'),
            'в': (22, 'left_index'), 'к': (23, 'right_index'), 'д': (24, 'right_index'),
            'ч': (25, 'right_index'), 'ш': (26, 'right_index'), 'щ': (27, 'right_index'),
            'у': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'е': (32, 'left_middle'),
            'о': (33, 'left_index'), 'а': (34, 'left_index'), 'л': (35, 'right_middle'),
            'н': (36, 'right_middle'), 'т': (37, 'right_middle'), 'с': (38, 'right_ring'),
            'р': (39, 'right_ring'), 'й': (40, 'right_ring'),
            'ф': (44, 'left_pinky'), 'э': (45, 'left_ring'), 'х': (46, 'left_middle'),
            'ы': (47, 'left_index'), 'ю': (48, 'right_pinky'), 'б': (49, 'right_pinky'),
            'м': (50, 'right_pinky'), 'п': (51, 'right_pinky'), 'г': (52, 'right_pinky'),
            'ж': (53, 'right_pinky'),
            '"': (43, 'right_index'), '*': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        self.shift_keys = {
            '.': (2, 'left_pinky'), 'ё': (3, 'left_ring'), 'ъ': (4, 'left_middle'),
            '?': (5, 'left_index'), '!': (6, 'right_index'), '': (7, 'right_middle'),
            '-': (8, 'right_ring'), "'": (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '«': (13, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }
"""
Модуль раскладки ЗУБАЧЕВ
"""

from .base import KeyboardLayout


class ZubachevLayout(KeyboardLayout):
    """Класс раскладки ЗУБАЧЕВ"""

    def __init__(self):
        super().__init__()
        self.display_name = "ЗУБАЧЕВ"
        self._init_layout()

    def _init_layout(self):
        """Инициализация раскладки ЗУБАЧЕВ"""
        self.keys = {
            'ф': (16, 'left_pinky'), 'ы': (17, 'left_ring'), 'а': (18, 'left_middle'),
            'я': (19, 'left_index'), ',': (20, 'left_index'), 'й': (21, 'left_index'),
            'м': (22, 'left_index'), 'р': (23, 'right_index'), 'п': (24, 'right_index'),
            'х': (25, 'right_index'), 'ц': (26, 'right_index'), 'щ': (27, 'right_index'),
            'г': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'у': (32, 'left_middle'),
            'о': (33, 'left_index'), 'у': (34, 'left_index'), 'л': (35, 'right_middle'),
            'т': (36, 'right_middle'), 'с': (37, 'right_middle'), 'н': (38, 'right_ring'),
            'з': (39, 'right_ring'), 'ж': (40, 'right_ring'),
            'ш': (44, 'left_pinky'), 'ь': (45, 'left_ring'), 'ю': (46, 'left_middle'),
            '.': (47, 'left_index'), 'э': (48, 'right_pinky'), 'б': (49, 'right_pinky'),
            'д': (50, 'right_pinky'), 'в': (51, 'right_pinky'), 'к': (52, 'right_pinky'),
            'ч': (53, 'right_pinky'),
            '\\': (43, 'right_index'), 'ё': (41, 'right_pinky'), ' ': (57, 'right_thumb')
        }

        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        self.shift_keys = {
            '!': (2, 'left_pinky'), '"': (3, 'left_ring'), '№': (4, 'left_middle'),
            ';': (5, 'left_index'), '%': (6, 'right_index'), ':': (7, 'right_middle'),
            '?': (8, 'right_ring'), '*': (9, 'right_pinky'), '(': (10, 'right_pinky'),
            ')': (11, 'right_pinky'), '_': (12, 'right_pinky'), '+': (13, 'right_pinky'),
            '/': (43, 'right_index'), 'ъ': (45, 'left_ring'), 'ь': (47, 'left_index')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }
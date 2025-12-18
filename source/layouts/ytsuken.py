"""
Модуль раскладки ЙЦУКЕН
"""

from .base import KeyboardLayout


class YtsukenLayout(KeyboardLayout):
    """Класс раскладки ЙЦУКЕН"""

    def __init__(self):
        super().__init__()
        self.display_name = "ЙЦУКЕН"
        self._init_layout()

    def _init_layout(self):
        """Инициализация раскладки ЙЦУКЕН"""
        self.keys = {
            'й': (16, 'left_pinky'), 'ц': (17, 'left_ring'), 'у': (18, 'left_middle'),
            'к': (19, 'left_index'), 'е': (20, 'left_index'), 'н': (21, 'right_index'),
            'г': (22, 'right_index'), 'ш': (23, 'right_middle'), 'щ': (24, 'right_ring'),
            'з': (25, 'right_pinky'), 'х': (26, 'right_pinky'), 'ъ': (27, 'right_pinky'),
            'ф': (30, 'left_pinky'), 'ы': (31, 'left_ring'), 'в': (32, 'left_middle'),
            'а': (33, 'left_index'), 'п': (34, 'left_index'), 'р': (35, 'right_index'),
            'о': (36, 'right_index'), 'л': (37, 'right_middle'), 'д': (38, 'right_ring'),
            'ж': (39, 'right_pinky'), 'э': (40, 'right_pinky'),
            'я': (44, 'left_pinky'), 'ч': (45, 'left_ring'), 'с': (46, 'left_middle'),
            'м': (47, 'left_index'), 'и': (48, 'right_index'), 'т': (49, 'right_index'),
            'ь': (50, 'right_index'), 'б': (51, 'right_middle'), 'ю': (52, 'right_ring'),
            'ё': (41, 'left_pinky'), ' ': (57, 'right_thumb')
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
            '/': (43, 'right_pinky'), ',': (53, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 36, 'right_middle': 37, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }
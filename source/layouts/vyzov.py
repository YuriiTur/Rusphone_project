"""
Модуль раскладки ВЫЗОВ
"""

from .base import KeyboardLayout


class VyzovLayout(KeyboardLayout):
    """Класс раскладки ВЫЗОВ"""

    def __init__(self):
        super().__init__()
        self.display_name = "ВЫЗОВ"
        self._init_layout()

    def _init_layout(self):
        """Инициализация раскладки ВЫЗОВ"""
        self.keys = {
            'б': (16, 'left_pinky'), 'ы': (17, 'left_ring'), 'о': (18, 'left_middle'),
            'у': (19, 'left_index'), 'ь': (20, 'left_index'), 'ё': (21, 'right_index'),
            '^': (22, 'right_index'), 'д': (23, 'right_index'), 'я': (24, 'right_middle'),
            'г': (25, 'right_middle'), 'ж': (26, 'right_middle'),
            'ч': (30, 'left_pinky'), 'и': (31, 'left_ring'), 'е': (32, 'left_middle'),
            'а': (33, 'left_index'), ',': (34, 'left_index'), 'н': (36, 'right_index'),
            'т': (37, 'right_middle'), 'с': (38, 'right_ring'), 'в': (39, 'right_pinky'),
            'з': (40, 'right_ring'),
            'х': (45, 'left_ring'), 'й': (46, 'left_middle'),
            'к': (47, 'left_index'), '_': (48, 'left_index'), '/': (49, 'right_pinky'),
            'р': (50, 'right_index'), 'м': (51, 'right_ring'), 'ф': (52, 'right_pinky'),
            'п': (53, 'right_pinky'),
            ' ': (57, 'right_thumb'), '₽': (41, 'right_thumb')
        }

        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        self.shift_keys = {
            'ё': (2, 'left_pinky'), '[': (3, 'left_ring'), '{': (4, 'left_middle'),
            '}': (5, 'left_index'), '(': (6, 'right_index'), '=': (7, 'right_middle'),
            '*': (8, 'right_ring'), ')': (9, 'right_pinky'), '+': (10, 'right_pinky'),
            ']': (11, 'right_pinky'), '!': (12, 'right_pinky'),
            ';': (34, 'left_index'), ':': (35, 'right_index'), "'": (20, 'left_index'),
            '-': (48, 'left_index'), '?': (49, 'right_pinky'), '@': (27, 'right_ring'),
            '$': (41, 'right_thumb')
        }

        self.alt_keys = {
            'ц': (30, 'left_ring'),
            'щ': (36, 'right_index'),
            'ъ': (37, 'right_middle'),
            '№': (39, 'right_pinky'),
            'э': (32, 'left_middle')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 36, 'right_middle': 37, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }
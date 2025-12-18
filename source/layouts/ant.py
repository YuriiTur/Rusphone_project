"""
Модуль раскладки АНТ
"""

from .base import KeyboardLayout


class AntLayout(KeyboardLayout):
    """Класс раскладки АНТ"""

    def __init__(self):
        super().__init__()
        self.display_name = "АНТ"
        self._init_layout()

    def _init_layout(self):
        """Инициализация раскладки АНТ"""
        self.keys = {
            'г': (16, 'left_pinky'), 'п': (17, 'left_ring'), 'р': (18, 'left_middle'),
            'д': (19, 'left_index'), 'м': (20, 'left_index'), 'ы': (21, 'left_index'),
            'и': (22, 'left_index'), 'я': (23, 'right_index'), 'у': (24, 'right_index'),
            'х': (25, 'right_index'), 'ц': (26, 'right_index'), 'ж': (27, 'right_index'),
            'в': (30, 'left_pinky'), 'н': (31, 'left_ring'), 'с': (32, 'left_middle'),
            'т': (33, 'left_index'), 'л': (34, 'left_index'), 'ь': (35, 'right_middle'),
            'о': (36, 'right_middle'), 'е': (37, 'right_middle'), 'а': (38, 'right_ring'),
            'к': (39, 'right_ring'), 'з': (40, 'right_ring'),
            'щ': (44, 'left_pinky'), 'й': (45, 'left_ring'), 'ш': (46, 'left_middle'),
            'ь': (47, 'left_index'), ',': (48, 'right_pinky'), '.': (49, 'right_pinky'),
            'ю': (50, 'right_pinky'), 'э': (51, 'right_pinky'), 'ё': (52, 'right_pinky'),
            'ф': (53, 'right_pinky'), 'ч': (43, 'right_index'), '\\': (41, 'right_pinky'),
            ' ': (57, 'right_thumb')
        }

        self.caps_keys = {}
        for char, (code, finger) in self.keys.items():
            if char.isalpha() and char != ' ':
                self.caps_keys[char.upper()] = (code, finger)

        self.shift_keys = {
            '!': (2, 'left_pinky'), '?': (3, 'left_ring'), "'": (4, 'left_middle'),
            '"': (5, 'left_index'), '=': (6, 'right_index'), '+': (7, 'right_middle'),
            '-': (8, 'right_ring'), '*': (9, 'right_pinky'), '/': (10, 'right_pinky'),
            '%': (11, 'right_pinky'), '«': (12, 'right_pinky'), '»': (13, 'right_pinky'),
            ';': (48, 'right_pinky'), ':': (49, 'right_pinky')
        }

        self.home_positions = {
            'left_pinky': 30, 'left_ring': 31, 'left_middle': 32, 'left_index': 33,
            'right_index': 23, 'right_middle': 36, 'right_ring': 38, 'right_pinky': 39,
            'left_thumb': 42, 'right_thumb': 57
        }
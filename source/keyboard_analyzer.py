"""
Основной класс анализатора раскладок клавиатуры
"""


class KeyboardAnalyzer:
    """
    Класс для анализа раскладок клавиатуры.

    Позволяет оценить нагрузку на пальцы при печати на разных раскладках.
    Поддерживает анализ пути движения от домашнего ряда, учёт модификаторов,
    статистику по рукам и типам нажатий, анализ удобства пальцевых переборов.
    """

    def __init__(self, layout_name='ytsuken'):
        """
        Инициализирует анализатор клавиатурной раскладки.

        Args:
            layout_name: Название раскладки ('ytsuken', 'vyzov', и т.д.)
        """
        self.layout_name = layout_name

        # Динамически импортируем нужную раскладку
        try:
            module_name = f"layouts.{layout_name}"
            layout_module = __import__(module_name, fromlist=[''])

            # Получаем класс раскладки
            layout_class = getattr(layout_module, f'{layout_name.capitalize()}Layout')
            self.layout = layout_class()

            # Копируем атрибуты из раскладки
            self.keys = self.layout.keys
            self.caps_keys = getattr(self.layout, 'caps_keys', {})
            self.shift_keys = getattr(self.layout, 'shift_keys', {})
            self.alt_keys = getattr(self.layout, 'alt_keys', {})
            self.home_positions = self.layout.home_positions


        except ImportError as e:
            print(f"Ошибка: Не удалось загрузить раскладку '{layout_name}': {e}")
            raise

        # Карта клавиатуры: код -> (ряд, колонка)
        self.keyboard_map = {
            # Цифровой ряд
            2: (0, 0), 3: (0, 1), 4: (0, 2), 5: (0, 3), 6: (0, 4),
            7: (0, 5), 8: (0, 6), 9: (0, 7), 10: (0, 8), 11: (0, 9),
            12: (0, 10), 13: (0, 11), 14: (0, 12),

            # Верхний ряд
            16: (1, 0), 17: (1, 1), 18: (1, 2), 19: (1, 3), 20: (1, 4),
            21: (1, 5), 22: (1, 6), 23: (1, 7), 24: (1, 8), 25: (1, 9),
            26: (1, 10), 27: (1, 11),

            # Домашний ряд
            30: (2, 0), 31: (2, 1), 32: (2, 2), 33: (2, 3), 34: (2, 4),
            35: (2, 5), 36: (2, 6), 37: (2, 7), 38: (2, 8), 39: (2, 9),
            40: (2, 10),

            # Нижний ряд
            41: (3, 0), 44: (3, 1), 45: (3, 2), 46: (3, 3), 47: (3, 4),
            48: (3, 5), 49: (3, 6), 50: (3, 7), 51: (3, 8), 52: (3, 9),
            53: (3, 10),

            # Особые клавиши
            42: (3, -1),  # Shift
            43: (1, 12),  # \
            57: (4, 5)  # Пробел
        }

        # Порядок пальцев для анализа переборов
        self.finger_order = {
            'left': ['left_pinky', 'left_ring', 'left_middle', 'left_index'],
            'right': ['right_pinky', 'right_ring', 'right_middle', 'right_index']
        }

        # Приоритет пальцев (меньше = ближе к центру)
        self.finger_priority = {
            'left_pinky': 4, 'left_ring': 3, 'left_middle': 2, 'left_index': 1,
            'right_index': 1, 'right_middle': 2, 'right_ring': 3, 'right_pinky': 4
        }

    def _calculate_shtraf(self, key_code, finger):
        """Вычисляет путь движения пальца от домашней позиции до заданной клавиши."""
        if finger in ['left_thumb', 'right_thumb']:
            return 0

        home_code = self.home_positions[finger]
        home_coords = self.keyboard_map.get(home_code)
        target_coords = self.keyboard_map.get(key_code)

        if not home_coords or not target_coords:
            return 0

        home_row, home_col = home_coords
        target_row, target_col = target_coords

        row_diff = abs(target_row - home_row)
        col_diff = abs(target_col - home_col)

        return row_diff + col_diff

    def _get_finger_for_char(self, char):
        """Получает палец для символа (без учета модификаторов)"""
        if char in self.keys:
            return self.keys[char][1]
        elif char in getattr(self, 'caps_keys', {}):
            return self.caps_keys[char][1]
        elif char in getattr(self, 'shift_keys', {}):
            return self.shift_keys[char][1]
        elif char in getattr(self, 'alt_keys', {}):
            return self.alt_keys[char][1]
        return None

    def _get_hand_for_finger(self, finger):
        """Определяет руку по названию пальца"""
        if finger.startswith('left'):
            return 'left'
        elif finger.startswith('right'):
            return 'right'
        return None

    def _analyze_finger_sequence(self, fingers):
        """
        Классификация пальцевых переборов строго по правилам:

        УДП (udp)   — внешний -> внутренний  (1 -> 2 -> 3 -> 4)  строго растёт
        ЧУДП (chudp) — внутренний -> внешний  (4 -> 3 -> 2 -> 1)  строго падает
        НУДП (nudp)  — всё остальное (смешанное направление, переходы между руками)
        """

        if len(fingers) < 2:
            return 'other', 'none'

        # Определяем руку
        hands = [self._get_hand_for_finger(f) for f in fingers]

        # Если переход между руками — сразу НУДП
        if len(set(hands)) > 1:
            return 'nudp', 'mixed'

        # Приоритеты пальцев: внешний -> 1, внутренний -> 4
        priority = {
            'left_pinky': 1, 'left_ring': 2, 'left_middle': 3, 'left_index': 4,
            'right_pinky': 1, 'right_ring': 2, 'right_middle': 3, 'right_index': 4
        }

        # Получаем последовательность приоритетов
        seq = [priority[f] for f in fingers]

        # Проверка на строго растущий (УДП)
        is_udp = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))

        # Проверка на строго убывающий (ЧУДП)
        is_chudp = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))

        if is_udp:
            return 'udp', 'outward'  # внешний -> внутренний
        elif is_chudp:
            return 'chudp', 'inward'  # внутренний -> внешний
        else:
            return 'nudp', 'mixed'

    def analyze_ngrams(self, text, n=2):
        """Анализирует n-граммы в тексте для оценки удобства пальцевых переборов."""
        if not text:
            return None

        # Убираем пробелы и приводим к нижнему регистру для анализа
        # УПРОЩАЕМ: анализируем только буквы
        clean_text = ''.join([c.lower() for c in text if c.isalpha()])

        if len(clean_text) < n:
            return None

        ngram_stats = {
            'total': 0,
            'udp': 0,
            'chudp': 0,
            'nudp': 0,
            'same_finger': 0,
            'different_hands': 0,
            'with_modifier': 0,
            'examples': {'udp': [], 'chudp': [], 'nudp': []}
        }

        # Оптимизируем: предварительно получаем пальцы для всех символов
        char_to_finger = {}
        for char in set(clean_text):
            finger = self._get_finger_for_char(char)
            if finger:
                char_to_finger[char] = finger

        # Проходим по тексту с окном размера n
        for i in range(len(clean_text) - n + 1):
            ngram = clean_text[i:i + n]

            # Получаем пальцы для каждого символа
            fingers = []
            for char in ngram:
                if char not in char_to_finger:
                    break
                fingers.append(char_to_finger[char])

            if len(fingers) != n:
                continue

            ngram_stats['total'] += 1

            # Проверяем, все ли пальцы на одной руке
            hands = [self._get_hand_for_finger(f) for f in fingers]
            unique_hands = set(hands)

            # Переход между руками — всегда неудобный перебор
            if len(unique_hands) > 1:
                ngram_stats['nudp'] += 1
                if len(ngram_stats['examples']['nudp']) < 5:
                    ngram_stats['examples']['nudp'].append(ngram)
                continue

            # Проверяем, один ли палец используется
            if len(set(fingers)) == 1:
                ngram_stats['same_finger'] += 1
                continue

            # Анализируем тип перебора
            ngram_type, direction = self._analyze_finger_sequence(fingers)
            ngram_stats[ngram_type] += 1

            # Сохраняем примеры (не более 5 каждого типа)
            if len(ngram_stats['examples'][ngram_type]) < 5:
                ngram_stats['examples'][ngram_type].append(ngram)

        # Вычисляем проценты
        if ngram_stats['total'] > 0:
            ngram_stats['udp_percent'] = (ngram_stats['udp'] / ngram_stats['total']) * 100
            ngram_stats['chudp_percent'] = (ngram_stats['chudp'] / ngram_stats['total']) * 100
            ngram_stats['nudp_percent'] = (ngram_stats['nudp'] / ngram_stats['total']) * 100
            ngram_stats['same_finger_percent'] = (ngram_stats['same_finger'] / ngram_stats['total']) * 100
            ngram_stats['different_hands_percent'] = (ngram_stats['different_hands'] / ngram_stats['total']) * 100

        return ngram_stats

    def load_text_file(self, filename):
        """Загружает текст из указанного файла."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Ошибка: Файл {filename} не найден!")
            return ""
        except Exception as e:
            print(f"Ошибка загрузки файла {filename}: {e}")
            return ""

    def analyze_text(self, text, text_name):
        """Анализирует текст с точки зрения нагрузки на пальцы."""
        if not text:
            return None

        clean_text = text

        paths = {finger: 0 for finger in [
            'left_pinky', 'left_ring', 'left_middle', 'left_index',
            'right_index', 'right_middle', 'right_ring', 'right_pinky',
            'left_thumb', 'right_thumb'
        ]}

        finger_counts = {finger: 0 for finger in paths.keys()}
        total_path = 0
        shift_count = 0
        alt_count = 0
        character_count = len(clean_text)

        left_hand_only = 0
        right_hand_only = 0
        both_hands = 0
        total_presses = 0

        left_hand_fingers = ['left_pinky', 'left_ring', 'left_middle', 'left_index', 'left_thumb']
        right_hand_fingers = ['right_pinky', 'right_ring', 'right_middle', 'right_index', 'right_thumb']

        for char in clean_text:
            options = []

            if char in self.keys:
                key_code, finger = self.keys[char]
                path = self._calculate_shtraf(key_code, finger)
                options.append(('normal', path, key_code, finger, 0, None))

            if char in getattr(self, 'caps_keys', {}):
                key_code, finger = self.caps_keys[char]
                path = self._calculate_shtraf(key_code, finger)
                options.append(('caps', path + 1, key_code, finger, 1, 'left_thumb'))

            if char in getattr(self, 'shift_keys', {}):
                key_code, finger = self.shift_keys[char]
                path = self._calculate_shtraf(key_code, finger)
                options.append(('shift', path + 1, key_code, finger, 1, 'left_thumb'))

            if char in getattr(self, 'alt_keys', {}):
                key_code, finger = self.alt_keys[char]
                path = self._calculate_shtraf(key_code, finger)
                options.append(('alt', path + 1, key_code, finger, 1, 'right_thumb'))

            if options:
                best_option = min(options, key=lambda x: x[1])
                mode, total_path_option, key_code, finger, mod_cost, mod_finger = best_option

                finger_counts[finger] += 1
                paths[finger] += total_path_option - mod_cost
                total_path += total_path_option
                total_presses += 1

                if mod_cost > 0 and mod_finger:
                    finger_counts[mod_finger] += 1
                    paths[mod_finger] += 1
                    total_path += 1
                    total_presses += 1

                    if mode in ['caps', 'shift']:
                        shift_count += 1
                    elif mode == 'alt':
                        alt_count += 1

                if mod_cost == 0:
                    if finger in left_hand_fingers:
                        left_hand_only += 1
                    elif finger in right_hand_fingers:
                        right_hand_only += 1
                else:
                    both_hands += 1

        average_path = total_path / character_count if character_count > 0 else 0

        left_hand_count = sum(finger_counts[f] for f in left_hand_fingers)
        right_hand_count = sum(finger_counts[f] for f in right_hand_fingers)
        total_hand_count = left_hand_count + right_hand_count

        left_hand_percentage = (left_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0
        right_hand_percentage = (right_hand_count / total_hand_count * 100) if total_hand_count > 0 else 0

        # Анализ n-грамм для этого текста
        ngram_results = {}
        for n in [2, 3, 4]:
            ngram_stats = self.analyze_ngrams(clean_text, n)
            if ngram_stats:
                ngram_results[f'{n}-gram'] = ngram_stats

        return {
            'text_name': text_name,
            'layout': self.layout_name,
            'layout_display_name': self.layout.display_name if hasattr(self.layout,
                                                                       'display_name') else self.layout_name,
            'total_path': total_path,
            'finger_paths': paths,
            'finger_counts': finger_counts,
            'characters_analyzed': character_count,
            'shift_count': shift_count,
            'alt_count': alt_count,
            'average_path': average_path,
            'left_hand_count': left_hand_count,
            'right_hand_count': right_hand_count,
            'left_hand_percentage': left_hand_percentage,
            'right_hand_percentage': right_hand_percentage,
            'left_hand_only': left_hand_only,
            'right_hand_only': right_hand_only,
            'two_handed': both_hands,
            'total_presses': total_presses,
            'average_presses_per_char': total_presses / character_count if character_count > 0 else 0,
            'left_hand_only_percentage': (left_hand_only / total_presses * 100) if total_presses > 0 else 0,
            'right_hand_only_percentage': (right_hand_only / total_presses * 100) if total_presses > 0 else 0,
            'two_handed_percentage': (both_hands / total_presses * 100) if total_presses > 0 else 0,
            'ngram_analysis': ngram_results
        }
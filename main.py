import csv
from enum import Enum
import matplotlib.pyplot as plt


# 1. Модель данных: Пальцы
class Finger(Enum):
    """
    Перечисление для представления 10 пальцев рук.
    Каждый палец имеет уникальный идентификатор и русское название.
    """
    L_PINKY = 0  # Левый мизинец
    L_RING = 1  # Левый безымянный
    L_MIDDLE = 2  # Левый средний
    L_INDEX = 3  # Левый указательный
    L_THUMB = 8  # Левый большой
    R_INDEX = 4  # Правый указательный
    R_MIDDLE = 5  # Правый средний
    R_RING = 6  # Правый безымянный
    R_PINKY = 7  # Правый мизинец
    R_THUMB = 9  # Правый большой

    def get_finger_name(self):
        """Возвращает русское название пальца"""
        names = {
            Finger.L_PINKY: "Л. Мизинец",
            Finger.L_RING: "Л. Безымянный",
            Finger.L_MIDDLE: "Л. Средний",
            Finger.L_INDEX: "Л. Указательный",
            Finger.L_THUMB: "Л. Большой",
            Finger.R_INDEX: "П. Указательный",
            Finger.R_MIDDLE: "П. Средний",
            Finger.R_RING: "П. Безымянный",
            Finger.R_PINKY: "П. Мизинец",
            Finger.R_THUMB: "П. Большой"
        }
        return names[self]


# 2. Класс раскладки клавиатуры
class KeyboardLayout:
    """
    Класс для представления раскладки клавиатуры.
    Хранит информацию о позициях клавиш и назначении пальцев.
    """

    def __init__(self, name):
        self.name = name
        self.key_position = {}  # Словарь: символ -> (ряд, колонка)
        self.finger_assignment = {}  # Словарь: символ -> палец

    def add_key(self, char, row, col, finger):
        """
        Добавляет клавишу в раскладку.

        Args:
            char: символ на клавише
            row: номер ряда (0 - верхний, 4 - нижний)
            col: номер колонки (слева направо)
            finger: палец, отвечающий за клавишу
        """
        self.key_position[char] = (row, col)
        self.finger_assignment[char] = finger

    def get_distance_penalty(self, char_from, char_to):
        """
        Вычисляет штраф расстояния между двумя клавишами.

        Алгоритм:
        1. Находит координаты обеих клавиш
        2. Вычисляет разницу по рядам и колонкам
        3. Берет максимальную разницу как базовый штраф
        4. Добавляет +1 если движение диагональное

        Args:
            char_from: символ первой клавиши
            char_to: символ второй клавиши

        Returns:
            Штраф расстояния (целое число)
        """
        if char_from not in self.key_position or char_to not in self.key_position:
            return 0  # Игнорируем неизвестные символы

        pos_from = self.key_position[char_from]
        pos_to = self.key_position[char_to]

        # Вычисляем разницы координат
        row_diff = abs(pos_from[0] - pos_to[0])
        col_diff = abs(pos_from[1] - pos_to[1])

        # Базовый штраф - расстояние Чебышева
        penalty = max(row_diff, col_diff)

        # Дополнительный штраф за диагональное движение
        if row_diff >= 1 and col_diff >= 1:
            penalty += 1

        return penalty

    def get_finger(self, char):
        """Возвращает палец, отвечающий за символ"""
        return self.finger_assignment.get(char)


# 3. Создание раскладки ЙЦУКЕН со всеми клавишами
def create_ytsuken_layout():
    """
    Создает и настраивает раскладку клавиатуры ЙЦУКЕН.

    Возвращает:
        Объект KeyboardLayout с полностью настроенной раскладкой
    """
    layout = KeyboardLayout("ЙЦУКЕН")

    # Верхний ряд (цифры и символы)
    # Ряд 0, колонки 0-11
    layout.add_key('1', 0, 0, Finger.L_PINKY)
    layout.add_key('2', 0, 1, Finger.L_RING)
    layout.add_key('3', 0, 2, Finger.L_MIDDLE)
    layout.add_key('4', 0, 3, Finger.L_INDEX)
    layout.add_key('5', 0, 4, Finger.L_INDEX)
    layout.add_key('6', 0, 5, Finger.R_INDEX)
    layout.add_key('7', 0, 6, Finger.R_INDEX)
    layout.add_key('8', 0, 7, Finger.R_MIDDLE)
    layout.add_key('9', 0, 8, Finger.R_RING)
    layout.add_key('0', 0, 9, Finger.R_RING)
    layout.add_key('-', 0, 10, Finger.R_PINKY)
    layout.add_key('=', 0, 11, Finger.R_PINKY)

    # Верхний ряд (буквы)
    # Ряд 1, колонки 0-11 - основные буквы верхнего ряда
    layout.add_key('й', 1, 0, Finger.L_PINKY)
    layout.add_key('ц', 1, 1, Finger.L_RING)
    layout.add_key('у', 1, 2, Finger.L_MIDDLE)
    layout.add_key('к', 1, 3, Finger.L_INDEX)
    layout.add_key('е', 1, 4, Finger.L_INDEX)
    layout.add_key('н', 1, 5, Finger.R_INDEX)
    layout.add_key('г', 1, 6, Finger.R_INDEX)
    layout.add_key('ш', 1, 7, Finger.R_MIDDLE)
    layout.add_key('щ', 1, 8, Finger.R_RING)
    layout.add_key('з', 1, 9, Finger.R_RING)
    layout.add_key('х', 1, 10, Finger.R_PINKY)
    layout.add_key('ъ', 1, 11, Finger.R_PINKY)

    # Домашний ряд (основной ряд для пальцев)
    # Ряд 2, колонки 0-10
    layout.add_key('ф', 2, 0, Finger.L_PINKY)
    layout.add_key('ы', 2, 1, Finger.L_RING)
    layout.add_key('в', 2, 2, Finger.L_MIDDLE)
    layout.add_key('а', 2, 3, Finger.L_INDEX)
    layout.add_key('п', 2, 4, Finger.L_INDEX)
    layout.add_key('р', 2, 5, Finger.R_INDEX)
    layout.add_key('о', 2, 6, Finger.R_INDEX)
    layout.add_key('л', 2, 7, Finger.R_MIDDLE)
    layout.add_key('д', 2, 8, Finger.R_RING)
    layout.add_key('ж', 2, 9, Finger.R_RING)
    layout.add_key('э', 2, 10, Finger.R_PINKY)

    # Нижний ряд
    # Ряд 3, колонки 0-10
    layout.add_key('я', 3, 0, Finger.L_PINKY)
    layout.add_key('ч', 3, 1, Finger.L_RING)
    layout.add_key('с', 3, 2, Finger.L_MIDDLE)
    layout.add_key('м', 3, 3, Finger.L_INDEX)
    layout.add_key('и', 3, 4, Finger.L_INDEX)
    layout.add_key('т', 3, 5, Finger.R_INDEX)
    layout.add_key('ь', 3, 6, Finger.R_INDEX)
    layout.add_key('б', 3, 7, Finger.R_MIDDLE)
    layout.add_key('ю', 3, 8, Finger.R_RING)
    layout.add_key('.', 3, 9, Finger.R_PINKY)

    # Специальные клавиши
    layout.add_key(' ', 4, 4, Finger.L_THUMB)  # Пробел - левый большой палец
    layout.add_key(' ', 4, 5, Finger.R_THUMB)  # Пробел - правый большой палец
    layout.add_key(',', 3, 10, Finger.R_PINKY)

    # Shift-комбинации (расположены в тех же позициях, что и основные клавиши)
    layout.add_key('!', 0, 0, Finger.L_PINKY)  # Shift + 1
    layout.add_key('?', 0, 7, Finger.R_MIDDLE)  # Shift + 7
    layout.add_key(':', 0, 9, Finger.R_RING)  # Shift + 6
    layout.add_key(';', 2, 10, Finger.R_PINKY)
    layout.add_key('(', 0, 8, Finger.R_RING)  # Shift + 9
    layout.add_key(')', 0, 9, Finger.R_RING)  # Shift + 0
    layout.add_key('"', 0, 2, Finger.L_MIDDLE)  # Shift + 2
    layout.add_key('\'', 0, 3, Finger.L_INDEX)  # Shift + 3

    # Управляющие клавиши (условное расположение)
    layout.add_key('\t', 2, 0, Finger.L_PINKY)  # Tab
    layout.add_key('\n', 4, 10, Finger.R_PINKY)  # Enter
    layout.add_key('\r', 4, 10, Finger.R_PINKY)  # Enter

    return layout


# 4. Анализатор нагрузки
class WorkloadAnalyzer:
    """
    Класс для анализа нагрузки на пальцы при печати.
    Считывает диграммы из файла и вычисляет штрафы расстояний.
    """

    def __init__(self, layout):
        self.layout = layout
        # Словарь для хранения нагрузки по каждому пальцу
        self.workload = {finger: 0 for finger in Finger}

    def analyze_digrams_from_file(self, filename):
        """
        Анализирует нагрузку на основе файла с диграммами.

        Процесс:
        1. Читает CSV файл с диграммами
        2. Для каждой диграммы вычисляет штраф расстояния
        3. Назначает штраф пальцу, который нажимает вторую клавишу
        4. Суммирует общую нагрузку

        Args:
            filename: путь к файлу с диграммами
        """
        total_penalty = 0
        digram_count = 0

        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) < 1:
                        continue
                    digram = row[0].strip()  # Берем первую колонку как диграмму
                    if len(digram) != 2:
                        continue  # Пропускаем некорректные диграммы

                    weight = 1  # Вес диграммы (можно использовать частоты)
                    char_from, char_to = digram[0], digram[1]

                    # Пропускаем английские буквы (фильтрация)
                    if char_from.isalpha() and char_from.isascii():
                        continue
                    if char_to.isalpha() and char_to.isascii():
                        continue

                    # Вычисляем штраф расстояния между клавишами
                    penalty = self.layout.get_distance_penalty(char_from.lower(), char_to.lower())

                    # Определяем палец для второй клавиши (которая нажимается)
                    finger_to = self.layout.get_finger(char_to.lower())

                    # Добавляем штраф к нагрузке пальца
                    if finger_to is not None:
                        self.workload[finger_to] += penalty * weight

                    # Суммируем общий штраф
                    total_penalty += penalty * weight
                    digram_count += 1

            # Вывод результатов анализа
            print(f"Общий штраф для раскладки '{self.layout.name}': {total_penalty}")
            print(f"Проанализировано диграмм: {digram_count}")

            # Вывод штрафа для каждого пальца
            print("\nШтраф по пальцам:")
            print("-" * 40)
            total_finger_penalty = sum(self.workload.values())
            for finger in Finger:
                finger_name = finger.get_finger_name()
                penalty = self.workload[finger]
                # Вычисляем процент от общей нагрузки
                percentage = (penalty / total_finger_penalty * 100) if total_finger_penalty > 0 else 0
                print(f"{finger_name}: {penalty:4d} ({percentage:5.1f}%)")

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    def plot_results(self):
        """
        Визуализирует результаты анализа в виде графиков.

        Создает:
        1. Линейный график нагрузки по пальцам
        2. Круговую диаграмму распределения нагрузки
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        fingers = list(Finger)
        finger_names = [f.get_finger_name() for f in fingers]
        workloads = [self.workload[f] for f in fingers]

        # График 1: Линейный график общей нагрузки
        ax1.plot(finger_names, workloads, 'o-', linewidth=3, markersize=8,
                 color='steelblue', markerfacecolor='red', markeredgecolor='darkred')

        ax1.set_title('Общая нагрузка по пальцам', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Пальцы')
        ax1.set_ylabel('Общий штраф')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#f8f9fa')

        # Поворачиваем подписи для лучшей читаемости
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # График 2: Круговая диаграмма распределения нагрузки
        nonzero_workloads = [w for w in workloads if w > 0]
        nonzero_fingers = [finger_names[i] for i, w in enumerate(workloads) if w > 0]

        if nonzero_workloads:
            ax2.pie(nonzero_workloads, labels=nonzero_fingers, autopct='%1.1f%%',
                    startangle=90, colors=plt.cm.Pastel1(range(len(nonzero_workloads))))
            ax2.set_title('Распределение нагрузки между пальцами (%)', fontsize=14, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'Нет данных', horizontalalignment='center',
                     verticalalignment='center', transform=ax2.transAxes, fontsize=16)
            ax2.set_title('Распределение нагрузки', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.show()


# 5. Главная функция
def main():
    """
    Основная функция программы.
    Координирует весь процесс анализа:
    1. Создает раскладку
    2. Запускает анализ
    3. Визуализирует результаты
    """
    # Создаем раскладку ЙЦУКЕН
    layout_ytsuken = create_ytsuken_layout()

    # Файл с диграммами для анализа
    digrams_filename = "voina-i-mir.txt"

    # Создаем анализатор и запускаем анализ
    analyzer = WorkloadAnalyzer(layout_ytsuken)
    analyzer.analyze_digrams_from_file(digrams_filename)

    # Визуализация результатов
    analyzer.plot_results()


if __name__ == "__main__":
    # Точка входа в программу
    main()
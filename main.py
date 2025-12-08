#!/usr/bin/env python3
"""
Основной файл анализатора раскладок клавиатуры
"""

import multiprocessing as mp
from functools import partial
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyboard_analyzer import KeyboardAnalyzer
from utils import (
    get_available_texts,
    get_available_layouts,
    print_comparison_table,
    print_detailed_analysis
)


def analyze_layout_for_file(layout_code, filename, text_name):
    """
    Анализирует одну раскладку для указанного файла.

    Args:
        layout_code: Код раскладки
        filename: Путь к файлу
        text_name: Название текста

    Returns:
        Результаты анализа
    """
    try:
        analyzer = KeyboardAnalyzer(layout_name=layout_code)  # Изменено здесь!
        text = analyzer.load_text_file(filename)

        if not text:
            print(f"Ошибка: Не удалось загрузить текст из файла {filename}")
            return None

        result = analyzer.analyze_text(text, text_name)
        return result

    except Exception as e:
        print(f"Ошибка при анализе раскладки {layout_code}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Основная функция программы"""
    print("=" * 80)
    print("АНАЛИЗАТОР РАСКЛАДОК КЛАВИАТУРЫ")
    print("Анализ нагрузки на пальцы и удобства пальцевых переборов")
    print("=" * 80)

    # Получаем доступные тексты
    texts = get_available_texts('texts')

    if not texts:
        print("Ошибка: В папке 'texts' не найдено текстовых файлов!")
        print("Создайте папку 'texts' и поместите туда файлы для анализа.")
        return

    print("\nДоступные тексты для анализа:")
    for i, (filename, name) in enumerate(texts, 1):
        print(f"  {i}. {name} ({filename})")

    # Выбор текста
    while True:
        try:
            choice = input("\nВыберите текст для анализа (номер): ")
            choice_idx = int(choice) - 1

            if 0 <= choice_idx < len(texts):
                selected_file, selected_name = texts[choice_idx]
                break
            else:
                print(f"Пожалуйста, введите число от 1 до {len(texts)}")
        except ValueError:
            print("Пожалуйста, введите число")

    print(f"\nВыбран текст: {selected_name}")

    # Получаем доступные раскладки
    layouts = get_available_layouts()
    layout_codes = [layout[0] for layout in layouts]
    layout_names = dict(layouts)

    print(f"\nДоступные раскладки ({len(layouts)}):")
    for code, name in layouts:
        print(f"  • {code}: {name}")

    # Выбор режима анализа
    print("\nРежимы анализа:")
    print("  1. Сравнить все раскладки")
    print("  2. Проанализировать конкретную раскладку")
    print("  3. Проанализировать несколько раскладок")

    while True:
        mode = input("\nВыберите режим (1-3): ")
        if mode in ['1', '2', '3']:
            break
        print("Пожалуйста, введите 1, 2 или 3")

    # Параллельный анализ
    print(f"\nЗагружаем текст из файла: {selected_file}")
    print(f"Запускаем анализ...")

    if mode == '1':  # Все раскладки
        selected_layouts = layout_codes
    elif mode == '2':  # Одна раскладка
        while True:
            layout_choice = input("Введите код раскладки (например, 'ytsuken'): ")
            if layout_choice in layout_codes:
                selected_layouts = [layout_choice]
                break
            else:
                print(f"Раскладка '{layout_choice}' не найдена. Доступные: {', '.join(layout_codes)}")
    else:  # Несколько раскладок
        selected_layouts = []
        while True:
            print(f"\nДоступные раскладки: {', '.join(layout_codes)}")
            layout_choice = input("Введите код раскладки (или 'готово' для завершения): ")

            if layout_choice.lower() == 'готово':
                if selected_layouts:
                    break
                else:
                    print("Нужно выбрать хотя бы одну раскладку")
            elif layout_choice in layout_codes:
                if layout_choice not in selected_layouts:
                    selected_layouts.append(layout_choice)
                    print(f"Добавлена раскладка: {layout_names[layout_choice]}")
                else:
                    print("Эта раскладка уже выбрана")
            else:
                print(f"Раскладка '{layout_choice}' не найдена")

    print(f"\nБудет проанализировано {len(selected_layouts)} раскладок:")
    for layout_code in selected_layouts:
        print(f"  • {layout_names[layout_code]}")

    # Создаем пул процессов
    num_processes = min(mp.cpu_count(), len(selected_layouts))
    print(f"\nИспользуется {num_processes} процессов для параллельного анализа")

    with mp.Pool(processes=num_processes) as pool:
        # Создаем частичную функцию с фиксированными параметрами файла
        analyze_func = partial(
            analyze_layout_for_file,
            filename=selected_file,
            text_name=selected_name
        )

        # Запускаем параллельные задачи
        results = pool.map(analyze_func, selected_layouts)

    # Фильтруем None результаты (ошибки)
    valid_results = [r for r in results if r is not None]

    if not valid_results:
        print("\nОшибка: Не удалось получить результаты анализа!")
        return

    print(f"\nУспешно проанализировано {len(valid_results)} из {len(selected_layouts)} раскладок")

    # Выводим таблицу сравнения
    print_comparison_table(valid_results, selected_name)

    # Детальный анализ
    if len(valid_results) == 1:
        print_detailed_analysis(valid_results[0])
    else:
        print("\n" + "=" * 80)
        print("ДЕТАЛЬНЫЙ АНАЛИЗ ОТДЕЛЬНЫХ РАСКЛАДОК")
        print("=" * 80)

        while True:
            print("\nДоступные раскладки для детального анализа:")
            for i, result in enumerate(valid_results, 1):
                layout_name = result.get('layout_display_name', result['layout'])
                print(f"  {i}. {layout_name}")
            print(f"  0. Завершить")

            try:
                choice = input("\nВыберите раскладку для детального анализа (номер): ")
                if choice == '0':
                    break

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(valid_results):
                    print_detailed_analysis(valid_results[choice_idx])
                else:
                    print(f"Пожалуйста, введите число от 1 до {len(valid_results)} или 0")
            except ValueError:
                print("Пожалуйста, введите число")

    # Экспорт результатов
    export = input("\nЭкспортировать результаты в файл? (да/нет): ")
    if export.lower() in ['да', 'д', 'y', 'yes']:
        export_results(valid_results, selected_name)


def export_results(results, text_name):
    """Экспортирует результаты в текстовый файл"""
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"результаты_анализа_{text_name}_{timestamp}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"РЕЗУЛЬТАТЫ АНАЛИЗА РАСКЛАДОК КЛАВИАТУРЫ\n")
            f.write(f"Текст: {text_name}\n")
            f.write(f"Время анализа: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            # Таблица сравнения
            f.write("ТАБЛИЦА СРАВНЕНИЯ РАСКЛАДОК\n")
            f.write("-" * 160 + "\n")

            # Заголовок таблицы
            headers = [
                "Раскладка", "Символов", "Нажатий", "Наж/симв", "Общий путь",
                "Ср. путь", "Левая", "Правая", "2 руки", "Shift", "Alt",
                "2-г УдП", "2-г ЧудП", "2-г НудП", "3-г УдП", "3-г ЧудП", "3-г НудП"
            ]

            f.write("{:<12} {:<10} {:<10} {:<10} {:<12} {:<10} {:<8} {:<8} {:<8} {:<8} {:<6} "
                    "{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}\n".format(*headers))
            f.write("-" * 160 + "\n")

            # Данные
            sorted_results = sorted(results, key=lambda x: x['total_path'])
            for result in sorted_results:
                ngram_stats = result.get('ngram_analysis', {})

                bigram_stats = ngram_stats.get('2-gram', {})
                bigram_udp = f"{bigram_stats.get('udp_percent', 0):.1f}%" if bigram_stats else "0%"
                bigram_chudp = f"{bigram_stats.get('chudp_percent', 0):.1f}%" if bigram_stats else "0%"
                bigram_nudp = f"{bigram_stats.get('nudp_percent', 0):.1f}%" if bigram_stats else "0%"

                trigram_stats = ngram_stats.get('3-gram', {})
                trigram_udp = f"{trigram_stats.get('udp_percent', 0):.1f}%" if trigram_stats else "0%"
                trigram_chudp = f"{trigram_stats.get('chudp_percent', 0):.1f}%" if trigram_stats else "0%"
                trigram_nudp = f"{trigram_stats.get('nudp_percent', 0):.1f}%" if trigram_stats else "0%"

                f.write("{:<12} {:<10} {:<10} {:<10.2f} {:<12} {:<10.2f} "
                        "{:<7.1f}% {:<7.1f}% {:<7.1f}% {:<8} {:<6} "
                        "{:<8} {:<8} {:<8} {:<8} {:<8} {:<8}\n".format(
                    result.get('layout_display_name', result['layout']),
                    result['characters_analyzed'],
                    result['total_presses'],
                    result['average_presses_per_char'],
                    result['total_path'],
                    result['average_path'],
                    result['left_hand_only_percentage'],
                    result['right_hand_only_percentage'],
                    result['two_handed_percentage'],
                    result['shift_count'],
                    result['alt_count'],
                    bigram_udp,
                    bigram_chudp,
                    bigram_nudp,
                    trigram_udp,
                    trigram_chudp,
                    trigram_nudp
                ))

            f.write("\n\n" + "=" * 80 + "\n")
            f.write("ДЕТАЛЬНЫЙ АНАЛИЗ РАСКЛАДОК\n")
            f.write("=" * 80 + "\n\n")

            for result in sorted_results:
                layout_name = result.get('layout_display_name', result['layout'])
                f.write(f"РАСКЛАДКА: {layout_name}\n")
                f.write("-" * 60 + "\n")

                f.write(f"Общая статистика:\n")
                f.write(f"  • Символов: {result['characters_analyzed']}\n")
                f.write(
                    f"  • Нажатий: {result['total_presses']} ({result['average_presses_per_char']:.2f} на символ)\n")
                f.write(f"  • Общий путь: {result['total_path']}\n")
                f.write(f"  • Средний путь: {result['average_path']:.2f}\n")

                f.write(f"\nРаспределение по рукам:\n")
                f.write(f"  • Левая рука: {result['left_hand_count']} ({result['left_hand_percentage']:.1f}%)\n")
                f.write(f"  • Правая рука: {result['right_hand_count']} ({result['right_hand_percentage']:.1f}%)\n")

                f.write(f"\nНагрузка по пальцам:\n")
                total_presses = sum(result['finger_counts'].values())
                finger_names = {
                    'left_pinky': 'Левый мизинец',
                    'left_ring': 'Левый безымянный',
                    'left_middle': 'Левый средний',
                    'left_index': 'Левый указательный',
                    'right_index': 'Правый указательный',
                    'right_middle': 'Правый средний',
                    'right_ring': 'Правый безымянный',
                    'right_pinky': 'Правый мизинец',
                    'left_thumb': 'Левый большой',
                    'right_thumb': 'Правый большой'
                }

                for finger, name in finger_names.items():
                    count = result['finger_counts'][finger]
                    if count > 0:
                        percentage = (count / total_presses * 100)
                        f.write(f"  • {name}: {count} нажатий ({percentage:.1f}%)\n")

                f.write("\n\n")

        print(f"Результаты сохранены в файл: {filename}")

    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")


if __name__ == "__main__":
    main()
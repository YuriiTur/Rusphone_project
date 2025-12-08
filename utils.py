"""
Утилиты для анализа раскладок клавиатуры
"""

import os
from collections import defaultdict


def get_available_texts(texts_dir='texts'):
    """Получает список доступных текстовых файлов"""
    if not os.path.exists(texts_dir):
        return []

    texts = []
    for filename in os.listdir(texts_dir):
        if filename.endswith('.txt'):
            # Извлекаем имя без расширения
            name = filename.replace('.txt', '').replace('-', ' ').title()
            texts.append((os.path.join(texts_dir, filename), name))

    return texts


def get_available_layouts(layouts_dir='layouts'):
    """Получает список доступных раскладок"""
    layouts = [
        ('ytsuken', 'ЙЦУКЕН'),
        ('vyzov', 'ВЫЗОВ'),
        ('rusphone', 'РУСФОН'),
        ('zubachev', 'ЗУБАЧЕВ'),
        ('skoropis', 'СКОРОПИСЬ'),
        ('diktor', 'ДИКТОР'),
        ('ant', 'АНТ')
    ]
    return layouts


def print_comparison_table(results, text_name):
    """Выводит таблицу сравнения раскладок для одного текста"""
    print(f"\n{'=' * 160}")
    print(f"СРАВНЕНИЕ РАСКЛАДОК ДЛЯ ТЕКСТА: {text_name}")
    print(f"{'=' * 160}")

    # Заголовок таблицы
    print(f"{'Раскладка':<12} {'Символов':<10} {'Нажатий':<10} {'Наж/симв':<10} "
          f"{'Общий путь':<12} {'Ср. путь':<10} {'Левая':<8} {'Правая':<8} {'2 руки':<8} "
          f"{'Shift':<8} {'Alt':<6} {'2-г УдП':<8} {'2-г ЧудП':<8} {'2-г НудП':<8} "
          f"{'3-г УдП':<8} {'3-г ЧудП':<8} {'3-г НудП':<8}")
    print(f"{'-' * 160}")

    # Сортируем результаты по общему пути (чем меньше, тем лучше)
    sorted_results = sorted(results, key=lambda x: x['total_path'])

    for result in sorted_results:
        # Получаем статистику по n-граммам
        ngram_stats = result.get('ngram_analysis', {})

        # Для 2-грамм
        bigram_stats = ngram_stats.get('2-gram', {})
        bigram_udp = f"{bigram_stats.get('udp_percent', 0):.1f}%" if bigram_stats else "0%"
        bigram_chudp = f"{bigram_stats.get('chudp_percent', 0):.1f}%" if bigram_stats else "0%"
        bigram_nudp = f"{bigram_stats.get('nudp_percent', 0):.1f}%" if bigram_stats else "0%"

        # Для 3-грамм
        trigram_stats = ngram_stats.get('3-gram', {})
        trigram_udp = f"{trigram_stats.get('udp_percent', 0):.1f}%" if trigram_stats else "0%"
        trigram_chudp = f"{trigram_stats.get('chudp_percent', 0):.1f}%" if trigram_stats else "0%"
        trigram_nudp = f"{trigram_stats.get('nudp_percent', 0):.1f}%" if trigram_stats else "0%"

        print(f"{result.get('layout_display_name', result['layout']):<12} "
              f"{result['characters_analyzed']:<10} "
              f"{result['total_presses']:<10} "
              f"{result['average_presses_per_char']:<10.2f} "
              f"{result['total_path']:<12} "
              f"{result['average_path']:<10.2f} "
              f"{result['left_hand_only_percentage']:<7.1f}% "
              f"{result['right_hand_only_percentage']:<7.1f}% "
              f"{result['two_handed_percentage']:<7.1f}% "
              f"{result['shift_count']:<8} "
              f"{result['alt_count']:<6} "
              f"{bigram_udp:<8} "
              f"{bigram_chudp:<8} "
              f"{bigram_nudp:<8} "
              f"{trigram_udp:<8} "
              f"{trigram_chudp:<8} "
              f"{trigram_nudp:<8}")


def print_detailed_analysis(result):
    """Выводит детальный анализ одной раскладки"""
    print(f"\n{'=' * 80}")
    print(f"ДЕТАЛЬНЫЙ АНАЛИЗ РАСКЛАДКИ: {result.get('layout_display_name', result['layout'])}")
    print(f"Текст: {result['text_name']}")
    print(f"{'=' * 80}")

    print(f"Общая статистика:")
    print(f"  • Символов: {result['characters_analyzed']}")
    print(f"  • Нажатий: {result['total_presses']} ({result['average_presses_per_char']:.2f} на символ)")
    print(f"  • Общий путь: {result['total_path']}")
    print(f"  • Средний путь: {result['average_path']:.2f}")

    print(f"\nРаспределение по рукам:")
    print(f"  • Левая рука: {result['left_hand_count']} ({result['left_hand_percentage']:.1f}%)")
    print(f"  • Правая рука: {result['right_hand_count']} ({result['right_hand_percentage']:.1f}%)")

    print(f"\nТипы нажатий:")
    print(f"  • Только левая рука: {result['left_hand_only']} ({result['left_hand_only_percentage']:.1f}%)")
    print(f"  • Только правая рука: {result['right_hand_only']} ({result['right_hand_only_percentage']:.1f}%)")
    print(f"  • Двуручные: {result['two_handed']} ({result['two_handed_percentage']:.1f}%)")

    # Анализ n-грамм
    ngram_stats = result.get('ngram_analysis', {})
    if ngram_stats:
        print(f"\nАнализ пальцевых переборов:")

        for ngram_type, stats in ngram_stats.items():
            if stats['total'] > 0:
                print(f"\n  {ngram_type.upper()}:")
                print(f"    • Всего {ngram_type}: {stats['total']}")
                print(f"    • Удобные (УдП): {stats['udp']} ({stats.get('udp_percent', 0):.1f}%)")
                print(f"    • Частично удобные (ЧудП): {stats['chudp']} ({stats.get('chudp_percent', 0):.1f}%)")
                print(f"    • Неудобные (НудП): {stats['nudp']} ({stats.get('nudp_percent', 0):.1f}%)")

                if stats['examples']['udp']:
                    print(f"    • Примеры УдП: {', '.join(stats['examples']['udp'][:3])}")
                if stats['examples']['chudp']:
                    print(f"    • Примеры ЧудП: {', '.join(stats['examples']['chudp'][:3])}")
                if stats['examples']['nudp']:
                    print(f"    • Примеры НудП: {', '.join(stats['examples']['nudp'][:3])}")

    print(f"\nНагрузка по пальцам:")
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
            print(f"  • {name}: {count} нажатий ({percentage:.1f}%)")
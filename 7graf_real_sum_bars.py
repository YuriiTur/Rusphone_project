# -*- coding: utf-8 -*-
"""
Горизонтальные столбики (7 раскладок)
с суммой Нагрузок (H) и Штрафов (Ш) по 3 текстам.
Работает с key_typ3.py
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# ---------------- Глушилка вывода всего key_typ3 -----------------
class Silent:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
    def __exit__(self, *args):
        sys.stdout = self._stdout
        sys.stderr = self._stderr

with Silent():
    from key_typ3 import KeyboardAnalyzer, get_common_chars


# -------------- Параметры -----------------
TEXT_FILES = [
    ('voina-i-mir.txt', 'Война и мир'),
    ('digramms.txt', 'Диграммы'),
    ('1grams-3.txt', '1-граммы')
]

LAYOUTS = [
    ('ytsuken', 'Йцукен'),
    ('vyzov', 'Вызов'),
    ('rusphone', 'Русфон'),
    ('zubachev', 'Зубачев'),
    ('skoropis', 'Скоропись'),
    ('diktor', 'Диктор'),
    ('ant', 'Ант')
]

COLORS = {
    'Йцукен': '#ff3333',
    'Вызов': '#000000',
    'Русфон': '#ffb6c1',
    'Зубачев': '#3366ff',
    'Скоропись': '#44aa00',
    'Диктор': '#9933cc',
    'Ант': '#cc6600'
}

# ------------ Сбор данных ---------------
def collect_data():
    common_chars = get_common_chars()
    results = {}

    for code, name in LAYOUTS:
        with Silent():
            analyzer = KeyboardAnalyzer(layout=code)
            stats_list = analyzer.analyze_all_files(common_chars)

        total_counts = {}
        total_penalties = {}

        for stats in stats_list:
            # H — нагрузка
            for f, v in stats["finger_counts"].items():
                total_counts[f] = total_counts.get(f, 0) + v

            # Ш — штрафы (это finger_paths)
            for f, v in stats["finger_paths"].items():
                total_penalties[f] = total_penalties.get(f, 0) + v

        results[name] = {
            "counts": total_counts,
            "penalties": total_penalties
        }

    return results


# ------------ Построение графика ----------
def plot_bars(data):

    order = [
        ('left_thumb',   'Большой Л'),
        ('right_thumb',  'Большой П'),
        ('left_index',   'Указательный Л'),
        ('right_index',  'Указательный П'),
        ('left_middle',  'Средний Л'),
        ('right_middle', 'Средний П'),
        ('left_ring',    'Безымянный Л'),
        ('right_ring',   'Безымянный П'),
        ('left_pinky',   'Мизинец Л'),
        ('right_pinky',  'Мизинец П'),
    ]

    fingers = [o[0] for o in order]
    labels = [o[1] for o in order]

    n_fingers = len(fingers)
    layouts = list(data.keys())
    n_layouts = len(layouts)

    bar_height = 0.18
    gap = 0.05
    total_bar_height = n_layouts * (bar_height + gap)
    y_positions = np.arange(n_fingers) * (total_bar_height + 0.15)

    fig, ax = plt.subplots(figsize=(16, 12))

    for i, layout in enumerate(layouts):
        offset = (i - (n_layouts - 1) / 2.0) * (bar_height + gap)
        ys = y_positions + offset

        counts = [data[layout]['counts'].get(f, 0) for f in fingers]
        fines  = [data[layout]['penalties'].get(f, 0) for f in fingers]

        ax.barh(
            ys,
            counts,
            height=bar_height,
            label=layout,
            color=COLORS[layout]
        )

        # подписи H и Ш
        for j, y in enumerate(ys):
            H = counts[j]
            S = fines[j]
            if H == 0 and S == 0:
                continue

            ax.text(
                H + max(1, max(counts) * 0.002),
                y,
                f"H:{H:,}; Ш:{S:,}",
                va='center',
                fontsize=7
            )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    ax.set_xlabel("Нажатия (H) и суммарные штрафы (Ш)")
    ax.set_title("Сравнение нагрузок и штрафов на пальцы (7 раскладок, сумма 3 текстов)",
                 fontsize=16, fontweight='bold')

    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.show()



# ------------ Запуск -------------------
if __name__ == "__main__":
    data = collect_data()
    plot_bars(data)

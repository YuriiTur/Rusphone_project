# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# --- временно глушим вывод всего, что печатает key_type2 ---
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
    from key_type2 import KeyboardAnalyzer, get_common_chars

# --- параметры ---
TEXT_FILES = [
    ('voina-i-mir.txt', 'Война и мир'),
    ('digramms.txt', 'Диграммы'),
    ('1grams-3.txt', '1-граммы'),
]

LAYOUTS = [
    ('standard', 'Йцукен'),
    ('challenge', 'Вызов'),
    ('rusphone', 'Русфон'),
]

COLORS = {
    'Йцукен': '#ff3333',
    'Вызов': '#000000',
    'Русфон': '#ffb6c1',
}

def collect_data():
    """Суммирует результаты для каждой раскладки без вывода в консоль"""
    common_chars = get_common_chars()
    results = {}
    for code, name in LAYOUTS:
        with Silent():
            analyzer = KeyboardAnalyzer(layout=code)
            data = analyzer.analyze_all_files(common_chars)
        total_counts, total_penalties = {}, {}
        for d in data:
            for f, v in d['finger_counts'].items():
                total_counts[f] = total_counts.get(f, 0) + v
            for f, v in d['finger_penalties'].items():
                total_penalties[f] = total_penalties.get(f, 0) + v
        results[name] = {'counts': total_counts, 'penalties': total_penalties}
    return results

def plot_bars(data):
    order = [
        ('left_thumb', 'Большой Л'),
        ('right_thumb', 'Большой П'),
        ('left_index', 'Указательный Л'),
        ('right_index', 'Указательный П'),
        ('left_middle', 'Средний Л'),
        ('right_middle', 'Средний П'),
        ('left_ring', 'Безымянный Л'),
        ('right_ring', 'Безымянный П'),
        ('left_pinky', 'Мизинец Л'),
        ('right_pinky', 'Мизинец П'),
    ]
    fingers = [o[0] for o in order]
    labels = [o[1] for o in order]
    n_fingers = len(fingers)
    n_layouts = len(data)
    bar_height = 0.18
    gap = 0.05
    total_bar_height = n_layouts * (bar_height + gap)
    y_positions = np.arange(n_fingers) * (total_bar_height + 0.05)

    fig, ax = plt.subplots(figsize=(14, 10))
    layouts = list(data.keys())

    for i, layout in enumerate(layouts):
        offset = (i - (n_layouts - 1) / 2.0) * (bar_height + gap)
        ys = y_positions + offset
        counts = [data[layout]['counts'].get(f, 0) for f in fingers]
        fines = [data[layout]['penalties'].get(f, 0) for f in fingers]
        ax.barh(ys, counts, height=bar_height, label=layout, color=COLORS.get(layout))
        for j, y in enumerate(ys):
            h, sh = counts[j], fines[j]
            if h == 0 and sh == 0:
                continue
            ax.text(h + max(1, max(counts) * 0.002),
                    y, f"H:{int(h):,}; Ш:{int(sh):,}",
                    va='center', fontsize=7)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('Количество нажатий (H) и суммарные штрафы (Ш)')
    ax.set_title('Сравнение нагрузок и штрафов на пальцы по раскладкам',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = collect_data()
    plot_bars(data)

# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

# === Цвета ===
COLOR_LEFT = '#1f77b4'      # Синий
COLOR_RIGHT = '#ff7f0e'     # Оранжевый
COLOR_TWO = '#9467bd'       # Фиолетовый (двуручие)

# === Реальные суммарные данные из extract_stats (H по пальцам) ===
# СЛЕВА: Левые пальцы (L)
# СПРАВА: Правые пальцы (P)
# ДВУРУЧИЕ: 0 (в данных нет)

real = {
    "Йцукен": {
        "left":   [576119, 3188861, 1513199, 452746, 462321],
        "right":  [576119, 4557113, 867558, 473734, 535461],
        "two":    [0]
    },
    "Вызов": {
        "left":   [486393, 1299712, 554321, 355307, 344601],
        "right":  [649179, 2683181, 1150791, 547226, 770681],
        "two":    [0]
    },
    "Русфон": {
        "left":   [522432, 2498098, 1184618, 1365565, 498000],
        "right":  [521932, 2313047, 965668, 1126939, 953648],
        "two":    [0]
    },
    "Зубачев": {
        "left":   [492300, 3444688, 1372595, 1107609, 534820],
        "right":  [529233, 2666214, 1422020, 1249007, 1793804],
        "two":    [0]
    },
    "Скоропись": {
        "left":   [499270, 3344929, 1330517, 1012467, 458529],
        "right":  [536471, 4542136, 1142700, 1103029, 1136055],
        "two":    [0]
    },
    "Диктор": {
        "left":   [519077, 2100429, 1472080, 1303507, 534409],
        "right":  [499654, 1969710, 1191584, 1093299, 1172792],
        "two":    [0]
    },
    "Ант": {
        "left":   [489330, 1818861, 2200000, 1303829, 340769],
        "right":  [576119, 1926083, 1521702, 809665, 727490],
        "two":    [0]
    }
}

# === Отрисовка ===
layouts = list(real.keys())
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()

def draw_pie(ax, name, left, right, two):
    total_left = sum(left)
    total_right = sum(right)
    total_two = sum(two)
    total = total_left + total_right + total_two

    values = [total_left, total_right, total_two]
    labels = ["Левая рука", "Правая рука", "Двуручие"]
    colors = [COLOR_LEFT, COLOR_RIGHT, COLOR_TWO]

    perc = [(v / total * 100) if total > 0 else 0 for v in values]

    labels_final = []
    for lbl, p in zip(labels, perc):
        labels_final.append(f"{lbl} ({p:.1f}%)")

    wedges, _ = ax.pie(
        values,
        labels=labels_final,
        colors=colors,
        startangle=90,
        labeldistance=1.08,
        wedgeprops={'edgecolor': 'white'}
    )

    ax.set_title(name, fontsize=12, fontweight="bold")
    ax.axis("equal")


for i, layout in enumerate(layouts):
    draw_pie(
        axes[i],
        layout,
        real[layout]["left"],
        real[layout]["right"],
        real[layout]["two"]
    )

fig.delaxes(axes[-1])

plt.suptitle("Распределение нагрузок по рукам (7 раскладок, сумма 3 текстов)",
             fontsize=16, fontweight="bold")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("7pie_real.png", dpi=300)
plt.show()

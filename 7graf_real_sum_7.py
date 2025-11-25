# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt

# ====== Цвета для раскладок ======
colors = {
    "Йцукен": "red",
    "Вызов": "black",
    "Русфон": "blue",
    "Зубачев": "green",
    "Скоропись": "#FFD700",   # золотой – видно всегда
    "Диктор": "purple",
    "Ант": "#8B4513"          # коричневый – видно всегда
}

# ====== Порядок пар пальцев ======
finger_pairs = [
    ("Большой", ["left_thumb", "right_thumb"]),
    ("Указательный", ["left_index", "right_index"]),
    ("Средний", ["left_middle", "right_middle"]),
    ("Безымянный", ["left_ring", "right_ring"]),
    ("Мизинец", ["left_pinky", "right_pinky"]),
]

# ====== Загружаем JSON ======
with open("summed_fingers.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ====== Построение графиков ======
def plot_fingers(data):
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    axes = axes.flatten()

    fig.suptitle("Сравнение нагрузок на пальцы (7 раскладок, сумма 3 текстов)",
                 fontsize=20, fontweight="bold")

    eps = 0.0001  # фиктивная высота, чтобы нули были видны

    for ax, (finger_name, pair) in zip(axes, finger_pairs):

        for layout, values in data.items():
            left = values.get(pair[0], 0)
            right = values.get(pair[1], 0)

            # Чтобы нулевые раскладки тоже отображались
            y_left = left if left != 0 else eps
            y_right = right if right != 0 else eps

            ax.plot(
                ["Левая", "Правая"],
                [y_left, y_right],
                marker="o",
                markersize=6,
                linewidth=2,
                label=layout,
                color=colors[layout]
            )

        ax.set_title(f"Палец: {finger_name}", fontsize=13)
        ax.set_ylabel("Нажатия")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    # пустую последнюю ячейку убираем
    fig.delaxes(axes[-1])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


plot_fingers(data)

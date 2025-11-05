import matplotlib.pyplot as plt
import numpy as np

# --- Цвета ---
COLOR_LEFT = '#1f77b4'      # Синий
COLOR_RIGHT = '#ff7f0e'     # Оранжевый
COLOR_TWO = '#9467bd'       # Фиолетовый

# --- Данные по трём раскладкам 
data = {
    'ЙЦУКЕН': {
        'left': [336883, 1819640, 685725, 161738, 401456],
        'right': [224588, 1300013, 231567, 73896, 293521],
        'two_handed': [200000]
    },
    'Вызов': {
        'left': [280736, 654094, 908794, 195100, 264718],
        'right': [280736, 693976, 384139, 148917, 354770],
        'two_handed': [50000]
    },
    'Русфон': {
        'left': [200000, 250000, 220000, 190000, 160000],
        'right': [180000, 230000, 200000, 170000, 150000],
        'two_handed': [25000]
    }
}

# --- Подготовка фигуры ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# --- Функция для одной круговой диаграммы ---
def draw_pie(ax, layout_name, left, right, two):
    total_left = sum(left)
    total_right = sum(right)
    total_two = sum(two)
    total = total_left + total_right + total_two

    values = [total_left, total_right, total_two]
    labels = ['Л. Рука', 'П. Рука', 'Двуручие']
    colors = [COLOR_LEFT, COLOR_RIGHT, COLOR_TWO]

    # вычисление процентов
    if total == 0:
        perc = [0, 0, 0]
    else:
        perc = [(v / total) * 100 for v in values]

    # финальные подписи (с процентом у двуручия)
    label_final = []
    for i, lbl in enumerate(labels):
        if lbl == 'Двуручие':
            label_final.append(f'{lbl} ({perc[i]:.1f}%)')
        else:
            label_final.append(lbl)

    # Отрисовка диаграммы (теперь без autotexts)
    wedges, texts = ax.pie(
        values,
        labels=label_final,
        colors=colors,
        startangle=90,
        labeldistance=1.1,
        wedgeprops={'edgecolor': 'white'}
    )

    # проценты внутри (только для рук)
    for i, wedge in enumerate(wedges):
        if labels[i] != 'Двуручие':
            ang = (wedge.theta2 + wedge.theta1) / 2
            x = 0.6 * np.cos(np.deg2rad(ang))
            y = 0.6 * np.sin(np.deg2rad(ang))
            ax.text(x, y, f'{perc[i]:.1f}%', ha='center', va='center',
                    fontsize=10, color='white', fontweight='bold')

    ax.set_title(layout_name, fontsize=12, fontweight='bold')
    ax.axis('equal')

# --- Рисуем все три раскладки ---
layout_names = list(data.keys())
for i, layout in enumerate(layout_names):
    draw_pie(axes[i],
             layout,
             data[layout]['left'],
             data[layout]['right'],
             data[layout]['two_handed'])


fig.delaxes(axes[3])

# Заголовок и оформление
plt.suptitle("Сравнение нагрузок на руки и двуручия по раскладкам",
             fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig("7diagr_real.png", dpi=300)
plt.show()

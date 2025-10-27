from key_type2 import KeyboardAnalyzer, get_common_chars
import matplotlib.pyplot as plt

def plot_finger_loads(all_results):
    plt.figure(figsize=(10, 6))
    fingers = ['L миз', 'L без', 'L сред', 'L указ', 'R указ', 'R сред', 'R без', 'R миз', 'L бол', 'R бол']

    for layout, penalties in all_results.items():
        layout_name = 'ЙЦУКЕН' if layout == 'standard' else 'Вызов' if layout == 'challenge' else 'Русфон'
        values = [
            penalties['left_pinky'], penalties['left_ring'], penalties['left_middle'], penalties['left_index'],
            penalties['right_index'], penalties['right_middle'], penalties['right_ring'], penalties['right_pinky'],
            penalties['left_thumb'], penalties['right_thumb']
        ]
        plt.plot(fingers, values, marker='o', label=layout_name)

    plt.title("Нагрузка по пальцам для трёх раскладок")
    plt.xlabel("Пальцы (левая → правая рука)")
    plt.ylabel("Суммарный штраф (относительно home ряда)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("finger_loads.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    text = open("voina-i-mir.txt", "r", encoding="utf-8").read()
    common_chars = get_common_chars()

    all_results = {}
    for layout_code in ['standard', 'challenge', 'rusphone']:
        analyzer = KeyboardAnalyzer(layout=layout_code)
        filtered_text = ''.join(c for c in text if c in common_chars)
        # исправлено ↓↓↓
        result = analyzer.analyze_text(filtered_text, "Война и мир", common_chars)
        all_results[layout_code] = result['finger_penalties']

    plot_finger_loads(all_results)

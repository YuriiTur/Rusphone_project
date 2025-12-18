import re
import os
import matplotlib.pyplot as plt


def parse_summary_table(lines):
    summary = {}
    n = len(lines)
    i = 0

    # ищем начало таблицы
    while i < n and "ТАБЛИЦА СРАВНЕНИЯ РАСКЛАДОК" not in lines[i]:
        i += 1
    if i == n:
        return summary

    # идём до строки с заголовком "Раскладка ..."
    i += 1
    while i < n and not lines[i].strip().startswith("Раскладка"):
        i += 1
    if i == n:
        return summary

    # пропускаем строку заголовка и линию из дефисов
    i += 1
    if i < n and set(lines[i].strip()) <= {"-"}:
        i += 1

    # строки с данными раскладок
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            break
        if stripped.startswith("================================================================================") or stripped.startswith("ДЕТАЛЬНЫЙ"):
            break
        if set(stripped) <= {"-"}:
            i += 1
            continue

        tokens = re.split(r"\s+", stripped)

        # ожидаем не меньше 20 токенов (см. шапку таблицы)
        if len(tokens) < 20:
            i += 1
            continue

        try:
            layout = tokens[0]

            def _int(tok):
                return int(tok.replace(" ", "").replace("\u00a0", ""))

            def _float(tok):
                tok = tok.rstrip("%").replace(",", ".")
                return float(tok)

            symbols = _int(tokens[1])
            presses = _int(tokens[2])
            n_per_sym = _float(tokens[3])
            total_path = _int(tokens[4])
            avg_path = _float(tokens[5])

            # в таблице проценты могут быть как "48.3  %" так и "48.3%"
            left_pct = _float(tokens[6])
            right_pct = _float(tokens[8])
            twohands_pct = _float(tokens[10])

            shift_count = _int(tokens[12])
            alt_count = _int(tokens[13])

            bigram_ud_pct = _float(tokens[14])
            bigram_chud_pct = _float(tokens[15])
            bigram_nud_pct = _float(tokens[16])
            trigram_ud_pct = _float(tokens[17])
            trigram_chud_pct = _float(tokens[18])
            trigram_nud_pct = _float(tokens[19])
        except Exception:
            i += 1
            continue

        summary[layout] = {
            "symbols": symbols,
            "presses": presses,
            "n_per_sym": n_per_sym,
            "total_path": total_path,
            "avg_path": avg_path,
            "left_pct_table": left_pct,
            "right_pct_table": right_pct,
            "twohands_pct": twohands_pct,
            "shift_count": shift_count,
            "alt_count": alt_count,
            "bigram_ud_pct": bigram_ud_pct,
            "bigram_chud_pct": bigram_chud_pct,
            "bigram_nud_pct": bigram_nud_pct,
            "trigram_ud_pct": trigram_ud_pct,
            "trigram_chud_pct": trigram_chud_pct,
            "trigram_nud_pct": trigram_nud_pct,
        }

        i += 1

    return summary


def parse_analysis_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # название текста
    text_name = None
    for line in lines:
        m = re.search(r"Текст:\s*(.+)", line)
        if m:
            text_name = m.group(1).strip()
            break
    if text_name is None:
        text_name = os.path.splitext(os.path.basename(path))[0]

    summary = parse_summary_table(lines)

    layouts = {}
    n = len(lines)
    i = 0
    while i < n:
        line = lines[i]
        m = re.match(r"РАСКЛАДКА:\s*(.+)", line.strip())
        if m:
            layout_name = m.group(1).strip()
            j = i + 1
            while j < n and not lines[j].startswith("РАСКЛАДКА:"):
                j += 1
            block = "".join(lines[i:j])

            data = {
                "presses": None,
                "total_path": None,
                "avg_path": None,
                "left_abs": None,
                "left_pct": None,
                "right_abs": None,
                "right_pct": None,
                "fingers": {},

                # поля из сводной таблицы
                "symbols": None,
                "n_per_sym": None,
                "left_pct_table": None,
                "right_pct_table": None,
                "twohands_pct": None,
                "shift_count": None,
                "alt_count": None,
                "bigram_ud_pct": None,
                "bigram_chud_pct": None,
                "bigram_nud_pct": None,
                "trigram_ud_pct": None,
                "trigram_chud_pct": None,
                "trigram_nud_pct": None,
            }

            # Нажатия / путь из детального блока
            m_p = re.search(r"Нажатий:\s*([\d ]+)", block)
            if m_p:
                data["presses"] = int(m_p.group(1).replace(" ", ""))

            m_t = re.search(r"Общий путь:\s*([\d ]+)", block)
            if m_t:
                data["total_path"] = int(m_t.group(1).replace(" ", ""))

            m_a = re.search(r"Средний путь:\s*([\d.,]+)", block)
            if m_a:
                data["avg_path"] = float(m_a.group(1).replace(",", "."))

            # Левая / правая рука (из детального блока — это реальные проценты по нажатиям)
            m_l = re.search(r"Левая рука:\s*([\d ]+)\s*\(([\d.,]+)%\)", block)
            m_r = re.search(r"Правая рука:\s*([\d ]+)\s*\(([\d.,]+)%\)", block)
            if m_l:
                data["left_abs"] = int(m_l.group(1).replace(" ", ""))
                data["left_pct"] = float(m_l.group(2).replace(",", "."))
            if m_r:
                data["right_abs"] = int(m_r.group(1).replace(" ", ""))
                data["right_pct"] = float(m_r.group(2).replace(",", "."))

            # Пальцы
            finger_patterns = {
                "L_pinky": "Левый мизинец",
                "L_ring": "Левый безымянный",
                "L_middle": "Левый средний",
                "L_index": "Левый указательный",
                "R_index": "Правый указательный",
                "R_middle": "Правый средний",
                "R_ring": "Правый безымянный",
                "R_pinky": "Правый мизинец",
                "L_thumb": "Левый большой",
                "R_thumb": "Правый большой",
            }
            for key, label in finger_patterns.items():
                regex = label + r":\s*([\d ]+)[^(\n]*\(([\d.,]+)%\)"
                mf = re.search(regex, block)
                if mf:
                    abs_val = int(mf.group(1).replace(" ", ""))
                    pct_val = float(mf.group(2).replace(",", "."))
                    data["fingers"][key] = {"abs": abs_val, "pct": pct_val}

            # докидываем данные из сводной таблицы, если есть
            if layout_name in summary:
                s = summary[layout_name]
                for k in [
                    "symbols", "presses", "n_per_sym", "total_path", "avg_path",
                    "left_pct_table", "right_pct_table", "twohands_pct",
                    "shift_count", "alt_count",
                    "bigram_ud_pct", "bigram_chud_pct", "bigram_nud_pct",
                    "trigram_ud_pct", "trigram_chud_pct", "trigram_nud_pct",
                ]:
                    if s.get(k) is not None:
                        data[k] = s[k]

            layouts[layout_name] = data
            i = j
        else:
            i += 1

    # раскладки, которые есть только в сводной таблице
    for layout_name, s in summary.items():
        if layout_name not in layouts:
            data = {
                "presses": s.get("presses"),
                "total_path": s.get("total_path"),
                "avg_path": s.get("avg_path"),
                "left_abs": None,
                "left_pct": s.get("left_pct_table"),
                "right_abs": None,
                "right_pct": s.get("right_pct_table"),
                "fingers": {},
                "symbols": s.get("symbols"),
                "n_per_sym": s.get("n_per_sym"),
                "left_pct_table": s.get("left_pct_table"),
                "right_pct_table": s.get("right_pct_table"),
                "twohands_pct": s.get("twohands_pct"),
                "shift_count": s.get("shift_count"),
                "alt_count": s.get("alt_count"),
                "bigram_ud_pct": s.get("bigram_ud_pct"),
                "bigram_chud_pct": s.get("bigram_chud_pct"),
                "bigram_nud_pct": s.get("bigram_nud_pct"),
                "trigram_ud_pct": s.get("trigram_ud_pct"),
                "trigram_chud_pct": s.get("trigram_chud_pct"),
                "trigram_nud_pct": s.get("trigram_nud_pct"),
            }
            layouts[layout_name] = data

    return text_name, layouts


def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def plot_bar(x_labels, values, title, ylabel, out_path):
    plt.figure(figsize=(10, 5))
    plt.bar(x_labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_stacked_hands(layout_names, layouts, out_path, title):
    left = []
    right = []
    for name in layout_names:
        lp = layouts[name].get("left_pct")
        rp = layouts[name].get("right_pct")
        if lp is None:
            lp = layouts[name].get("left_pct_table")
        if rp is None:
            rp = layouts[name].get("right_pct_table")
        left.append(lp if lp is not None else 0.0)
        right.append(rp if rp is not None else 0.0)

    plt.figure(figsize=(10, 5))
    plt.bar(layout_names, left, label="Левая рука")
    plt.bar(layout_names, right, bottom=left, label="Правая рука")
    plt.ylabel("Доля, %")
    plt.title(title)
    plt.xticks(rotation=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_finger_stack(layout_names, layouts, out_path, title):
    finger_order = [
        "L_pinky", "L_ring", "L_middle", "L_index",
        "R_index", "R_middle", "R_ring", "R_pinky",
        "L_thumb", "R_thumb",
    ]
    finger_labels = {
        "L_pinky": "Л мизинец",
        "L_ring": "Л безым.",
        "L_middle": "Л средн.",
        "L_index": "Л указ.",
        "R_index": "П указ.",
        "R_middle": "П средн.",
        "R_ring": "П безым.",
        "R_pinky": "П мизинец",
        "L_thumb": "Л большой",
        "R_thumb": "П большой",
    }

    bottoms = [0.0] * len(layout_names)
    plt.figure(figsize=(10, 6))
    for key in finger_order:
        vals = []
        for name in layout_names:
            fdata = layouts[name]["fingers"].get(key)
            vals.append(fdata["pct"] if fdata else 0.0)
        plt.bar(layout_names, vals, bottom=bottoms, label=finger_labels[key])
        bottoms = [b + v for b, v in zip(bottoms, vals)]

    plt.ylabel("Доля, %")
    plt.title(title)
    plt.xticks(rotation=20)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_shift_alt(layout_names, layouts, out_path, title):
    x = list(range(len(layout_names)))
    shift_vals = [layouts[name].get("shift_count") or 0 for name in layout_names]
    alt_vals = [layouts[name].get("alt_count") or 0 for name in layout_names]
    width = 0.4

    plt.figure(figsize=(10, 5))
    left_x = [xi - width / 2 for xi in x]
    right_x = [xi + width / 2 for xi in x]
    plt.bar(left_x, shift_vals, width=width, label="Shift")
    plt.bar(right_x, alt_vals, width=width, label="Alt")
    plt.xticks(x, layout_names, rotation=20)
    plt.ylabel("Количество нажатий")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_ngrams_group(layout_names, layouts, out_path, title,
                      field_prefix="bigram",
                      labels=("УдП", "ЧудП", "НудП")):
    x = list(range(len(layout_names)))
    width = 0.25

    fields = [
        f"{field_prefix}_ud_pct",
        f"{field_prefix}_chud_pct",
        f"{field_prefix}_nud_pct",
    ]

    vals = []
    for field in fields:
        vals.append([
            layouts[name].get(field) or 0.0
            for name in layout_names
        ])

    plt.figure(figsize=(10, 6))
    offsets = [-width, 0, width]
    for i_field in range(3):
        xs = [xi + offsets[i_field] for xi in x]
        plt.bar(xs, vals[i_field], width=width, label=labels[i_field])

    plt.xticks(x, layout_names, rotation=20)
    plt.ylabel("Доля, %")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def make_plots_for_file(path, out_root="plots"):
    import re as _re

    text_name, layouts = parse_analysis_file(path)
    if not layouts:
        print("В файле", path, "не найдено раскладок")
        return

    safe_text = _re.sub(r"[^A-Za-zА-Яа-я0-9_]+", "_", text_name).strip("_")
    out_dir = os.path.join(out_root, safe_text)
    ensure_dir(out_dir)

    # фиксированный порядок раскладок для красоты графиков
    preferred_order = ["ВЫЗОВ", "ЗУБАЧЕВ", "СКОРОПИСЬ", "ДИКТОР", "АНТ", "ЙЦУКЕН", "РУСФОН"]
    layout_names = [name for name in preferred_order if name in layouts] or list(layouts.keys())

    # 1. Нажатия
    presses = [layouts[name].get("presses") or 0 for name in layout_names]
    plot_bar(
        layout_names, presses,
        f"Количество нажатий (текст: {text_name})",
        "Нажатий, шт.",
        os.path.join(out_dir, "presses.png"),
    )

    # 2. Общий путь
    total_path = [layouts[name].get("total_path") or 0 for name in layout_names]
    plot_bar(
        layout_names, total_path,
        f"Общий путь (текст: {text_name})",
        "Условные единицы пути",
        os.path.join(out_dir, "total_path.png"),
    )

    # 3. Средний путь
    avg_path = [layouts[name].get("avg_path") or 0 for name in layout_names]
    plot_bar(
        layout_names, avg_path,
        f"Средний путь (текст: {text_name})",
        "Условные единицы пути",
        os.path.join(out_dir, "avg_path.png"),
    )

    # 4. Руки
    plot_stacked_hands(
        layout_names, layouts,
        os.path.join(out_dir, "hands.png"),
        f"Распределение нагрузки по рукам (текст: {text_name})",
    )

    # 5. Пальцы
    if any(layouts[name]["fingers"] for name in layout_names):
        plot_finger_stack(
            layout_names, layouts,
            os.path.join(out_dir, "fingers.png"),
            f"Нагрузка по пальцам, % (текст: {text_name})",
        )

    # 6. Shift / Alt
    if any(layouts[name].get("shift_count") is not None for name in layout_names):
        plot_shift_alt(
            layout_names, layouts,
            os.path.join(out_dir, "shift_alt.png"),
            f"Использование модификаторов Shift/Alt (текст: {text_name})",
        )

    # 7. 2-граммы
    if any(layouts[name].get("bigram_ud_pct") is not None for name in layout_names):
        plot_ngrams_group(
            layout_names, layouts,
            os.path.join(out_dir, "bigrams.png"),
            f"2-граммы (УдП/ЧудП/НудП), % (текст: {text_name})",
            field_prefix="bigram",
            labels=("2-г УдП", "2-г ЧудП", "2-г НудП"),
        )

    # 8. 3-граммы
    if any(layouts[name].get("trigram_ud_pct") is not None for name in layout_names):
        plot_ngrams_group(
            layout_names, layouts,
            os.path.join(out_dir, "trigrams.png"),
            f"3-граммы (УдП/ЧудП/НудП), % (текст: {text_name})",
            field_prefix="trigram",
            labels=("3-г УдП", "3-г ЧудП", "3-г НудП"),
        )

    print(f"Графики для '{text_name}' сохранены в папке {out_dir}")


def main():
    cwd = os.getcwd()
    files = [
        f for f in os.listdir(cwd)
        if f.startswith("результаты_анализа_") and f.endswith(".txt")
    ]
    if not files:
        print("Нет файлов 'результаты_анализа_*.txt' в папке", cwd)
        return

    print("Будут обработаны файлы:")
    for f in files:
        print("  -", f)

    for f in files:
        make_plots_for_file(os.path.join(cwd, f))


if __name__ == "__main__":
    main()

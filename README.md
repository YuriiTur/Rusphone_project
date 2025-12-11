# Сбор статистики для оптимизации русских раскладок для слепопечатников
Данный проект представляет собой программу для анализа различных клавиатурных раскладок (русских)

- Рассмотренные раскладки:
	- Йцукен
	- Вызов
	- Диктор
	- Скоропись

## Лабораторные и как их запустить

### Установка Git
Для клонирования репозитория со всеми лабораторными через консоль нужен установленный **Git**:
#### Linux
```
sudo apt install git
```
#### Windows
-  [Ссылка на установщик](https://git-scm.com/downloads/win)

### Клонирование репозитория
```
git clone https://github.com/YuriiTur/Rusphone_project
```
```
cd layout_analyzer
```
#### Лабораторная 1
**Подсчёт нагрузки и штрафов на пальцы (количество кликов)**

![lab1](https://github.com/YuriiTur/Rusphone_project/blob/Lab1/aqzGNkVJZXLbIpDpAwKmyy4K7CgmHxPJqv_tonqqKBkbeKxqJOnRVX_vvoDSJ6HvrUL8aLN17RW5VSx5z656Ue14.jpg)

Переключение на ветку этой лабораторной:
```
git checkout lab1
```
Запуск:
```
python layout_analyzer.py 1grams-3.txt
```
Названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt`
#### Лабораторная 1+
**Подсчёт штрафов на пальцы**

![lab1+](https://github.com/YuriiTur/Rusphone_project/blob/Lab1%2B/tTZuoKSOoh4gvZ0jpjCd5A4Wi0KrZltbh7LDgWzgmG2iHETLTyjNf6ypyvJMsPvzTV9x5RA1bo7VMQ_iTUamX_mS.jpg)

Переключение на ветку этой лабораторной:
```
git checkout lab1+
```
Запуск:
```
python layout_analyzer.py 1grams-3.txt
```
Названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt`
#### Лабораторная 2
**Нагрузка по пальцам ("Война и мир")**

![lab2](https://github.com/YuriiTur/Rusphone_project/blob/Lab2/fingers.png)

**Нагрузка по пальцам (Digramms)**

![lab2](https://github.com/YuriiTur/Rusphone_project/blob/Lab2/fingers1.png)

**Нагрузка по пальцам ("1Gramms 3")**

![lab2](https://github.com/YuriiTur/Rusphone_project/blob/Lab2/fingers2.png)

Переключение на ветку этой лабораторной:
```
git checkout lab2
```
Запуск:
```
python layout_analyzer.py 1grams-3.txt
```
Названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt`

## Вывод

На основе анализа эргономических метрик для семи русских раскладок можно сделать следующие выводы:

ЙЦУКЕН (стандартная) показывает наихудшие результаты: максимальный путь пальцев, сильный перекос нагрузки на указательные пальцы, самое частое использование Shift и наибольший процент неудобных комбинаций букв. Это наименее эффективная раскладка.

ВЫЗОВ демонстрирует лучшую общую сбалансированность: минимальный путь пальцев, наименьшая зависимость от модификаторов и оптимальное распределение удобных/неудобных сочетаний. Наиболее эффективная раскладка для большинства пользователей.

СКОРОПИСЬ и ДИКТОР показывают почти идентичные отличные результаты, лишь немного уступая Вызову. Их схожесть позволяет рассматривать их как единую эффективную альтернативу с акцентом на естественность для русского языка.

АНТ представляет собой сильную самостоятельную разработку с выдающимся балансом нагрузки между пальцами и хорошими показателями по всем метрикам. Особенно рекомендуется тем, кто стремится минимизировать нагрузку на мизинцы.

ЗУБАЧЕВ показывает хорошие, но не выдающиеся результаты, находясь в середине рейтинга по большинству параметров. Надёжная, но не оптимальная альтернатива.

РУСФОН демонстрирует специфический профиль с упором на фонетический принцип, что даёт смешанные результаты: хорошее использование модификаторов, но не самый лучший баланс по другим параметрам.

Общий итог: Все альтернативные раскладки превосходят ЙЦУКЕН. Для перехода рекомендуется выбирать между Вызовом (максимальная эффективность), Скорописью/Диктором (оптимальный баланс) или Антом (лучшее распределение нагрузки). Даже Зубачев и Русфон представляют собой улучшение по сравнению со стандартом, но уступают лидерам по комплексности преимуществ.

## Приложения
### Рассматриваемые раскладки
#### Йцукен
![icuken](https://github.com/YuriiTur/Rusphone_project/blob/main/qwerty.png)

#### Диктор
![diktor](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/diktor.png)

#### Вызов
![vyzov](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/vyzov.png)

#### Скоропись
![skoropis](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/skoropis.png)

#### Русфон
![Rusphone](https://github.com/YuriiTur/Rusphone_project/blob/main/Rusfon.jpg)

#### Зубачев
![zubachew](https://github.com/YuriiTur/Rusphone_project/blob/main/zubachew.png)

#### Ант
![Ant](https://github.com/YuriiTur/Rusphone_project/blob/main/ant.png)

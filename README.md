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

Так как раскладки *Скоропись* и *Диктор* оказались очень схожими как по расположению букв так и по результату анализа - рассмотрим различия раскладок *Йцукен* и *Вызов*.
- *Вызов*:
	- явно выигрывает по распределению нагрузки между пальцами
		- но нагрузка на мизинцы наибольшая среди всех раскладок
	- несколько проигрывает в количестве одноручных комбинаций
- *Йцукен*:
	- огромная нагрузка на указательные пальцы > неизбежное отсутствие сбалансированной нагрузки на пальцы
	- преимущество в наборе всех типов комбинаций, кроме удобных трёхбуквенных (проигрывает всем)

В результате можно сделать вывод, что раскладка *Вызов* может стать лучшей заменой *Йцукена*, правда только если несколько повышенная нагрузка на мизинец не будет критичной.

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

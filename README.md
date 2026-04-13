# 🚚 LogiX Route Analyzer

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3.35+-green.svg)](https://sqlite.org)
[![Pandas](https://img.shields.io/badge/Pandas-1.5+-red.svg)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Учебный проект по анализу логистических маршрутов.**

Цель: Найти узкие места (задержки) в цепочке поставок, обработав сырые логи с помощью **SQL** и визуализировав результаты в **Python (Matplotlib / Seaborn)**.

## 🎯 Проблематика
Виртуальная логистическая компания сталкивается с нарушением сроков доставки.
Данные разрознены. Необходимо:
1. Собрать историю перемещений посылок.
2. Найти склады с аномально долгим временем обработки.
3. Визуализировать "бутылочное горлышко".

## 🛠 Стек технологий
- **Data Processing:** Pandas, NumPy
- **Database:** SQLite 3, SQLAlchemy (Core)
- **Visualization:** Matplotlib, Seaborn
- **Dev Tools:** Git, Jupyter Notebook, Faker (для генерации данных)

## 📂 Структура проекта

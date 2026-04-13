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
logistics-route-analyzer/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/                 # Папка для сырых и обработанных данных (в гите обычно пустая)
│   ├── raw/
│   │   └── delivery_log.csv
│   └── processed/
│       └── bottlenecks_report.csv
│
├── sql/                  # SQL-скрипты для создания и анализа БД
│   ├── 01_init_db.sql
│   ├── 02_insert_sample.sql
│   └── 03_query_bottlenecks.sql
│
├── src/                  # Исходный код Python
│   ├── data_generator.py # Генератор синтетических логов (чтобы проект работал без реальных данных)
│   ├── db_loader.py      # Загрузка CSV в SQLite
│   ├── analyzer.py       # Основная логика поиска проблем
│   └── visualizer.py     # Построение графиков
│
├── notebooks/            # Jupyter для демонстрации EDA
│   └── 01_analysis_demo.ipynb
│
└── output/               # Результаты визуализации
    └── figures/

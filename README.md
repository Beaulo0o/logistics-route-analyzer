# 🚚 Logistics Route Analyzer

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3.35+-green?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Pandas](https://img.shields.io/badge/Pandas-1.5+-red?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.6+-orange?style=for-the-badge)](https://matplotlib.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Учебный проект по анализу логистических маршрутов**  
> Поиск узких мест в цепочке поставок с помощью SQL и визуализация в Python.

---

## 📖 Оглавление

- [🎯 Проблематика](#-проблематика)
- [🛠 Стек технологий](#-стек-технологий)
- [📂 Структура проекта](#-структура-проекта)
- [🚀 Быстрый старт](#-быстрый-старт)
- [📊 Результаты анализа](#-результаты-анализа)
- [📝 Выводы](#-выводы)
- [📄 Лицензия](#-лицензия)

---

## 🎯 Проблематика

Виртуальная логистическая компания сталкивается с **систематическим нарушением сроков доставки**.  
Данные о перемещении посылок разрознены и требуют аналитической обработки.

### Задачи проекта:

| № | Задача | Инструмент |
|---|--------|------------|
| 1️⃣ | Собрать историю перемещений посылок | SQL (SQLite) |
| 2️⃣ | Найти склады с аномально долгим временем обработки | Оконные функции SQL |
| 3️⃣ | Визуализировать «бутылочное горлышко» | Python (Matplotlib, Seaborn) |
| 4️⃣ | Сформулировать рекомендации | Jupyter Notebook |

---

## 🛠 Стек технологий

| Категория | Инструменты |
|-----------|-------------|
| **Язык** | Python 3.9+ |
| **Обработка данных** | Pandas, NumPy |
| **База данных** | SQLite 3 |
| **Визуализация** | Matplotlib, Seaborn |
| **Генерация данных** | Faker |
| **Интерактивный анализ** | Jupyter Notebook |
| **Контроль версий** | Git, GitHub |

---

## 📂 Структура проекта
"""
logistics-route-analyzer/
│
├── README.md # Документация проекта
├── requirements.txt # Зависимости Python
├── .gitignore # Игнорируемые файлы Git
├── logistics.db # База данных SQLite (после запуска)
│
├── data/
│ ├── raw/ # Сырые сгенерированные данные
│ │ └── delivery_log.csv
│ └── processed/ # Обработанные отчёты
│ └── bottlenecks_report.csv
│
├── sql/ # SQL-скрипты
│ ├── 01_init_db.sql # Создание таблиц и представлений
│ ├── 02_insert_sample.sql # Пример ручной вставки
│ └── 03_query_bottlenecks.sql # Аналитические запросы
│
├── src/ # Исходный код Python
│ ├── data_generator.py # Генератор синтетических логов
│ ├── db_loader.py # Загрузка CSV в SQLite
│ ├── analyzer.py # Поиск узких мест
│ └── visualizer.py # Построение графиков
│
├── notebooks/ # Jupyter ноутбуки
│ └── 01_analysis_demo.ipynb # Интерактивный EDA
│
└── output/ # Результаты визуализации
└── figures/
├── bottleneck_ranking.png
├── processing_time_distribution.png
└── heatmap_weekly_load.png
"""

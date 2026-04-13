"""
Анализатор узких мест. Выполняет SQL-запросы и выводит результаты в консоль.
"""
import sqlite3
import pandas as pd

DB_PATH = "logistics.db"

def analyze():
    print("🔍 АНАЛИЗ УЗКИХ МЕСТ ЛОГИСТИКИ\n" + "="*50)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Запрос 1: Топ проблемных складов
    print("\n📌 ТОП-5 ПРОБЛЕМНЫХ СКЛАДОВ ПО ВРЕМЕНИ ОБРАБОТКИ:")
    query1 = """
    SELECT 
        location_name AS "Склад",
        parcels_processed AS "Посылок",
        avg_processing_hours AS "Среднее (ч)",
        max_processing_hours AS "Макс (ч)",
        delayed_over_24h AS "Задержек >24ч"
    FROM v_bottlenecks
    ORDER BY avg_processing_hours DESC
    LIMIT 5
    """
    df1 = pd.read_sql_query(query1, conn)
    print(df1.to_string(index=False))
    
    # Запрос 2: Общая статистика
    print("\n📌 ОБЩАЯ СТАТИСТИКА:")
    query2 = """
    SELECT 
        COUNT(DISTINCT parcel_id) AS total_parcels,
        MIN(event_timestamp) AS first_event,
        MAX(event_timestamp) AS last_event
    FROM logistics_log
    """
    df2 = pd.read_sql_query(query2, conn)
    print(df2.to_string(index=False))
    
    # Запрос 3: Аномалии (посылки с задержкой > 2 суток на одном складе)
    print("\n📌 АНОМАЛЬНЫЕ ЗАДЕРЖКИ (>48 ЧАСОВ НА СКЛАДЕ):")
    query3 = """
    WITH delays AS (
        SELECT 
            parcel_id,
            location_name,
            event_type,
            event_timestamp,
            LAG(event_timestamp) OVER (PARTITION BY parcel_id ORDER BY event_timestamp) AS prev_timestamp
        FROM logistics_log
        WHERE event_type IN ('ARRIVED', 'DEPARTED')
    )
    SELECT 
        parcel_id AS "Посылка",
        location_name AS "Склад",
        ROUND((JULIANDAY(event_timestamp) - JULIANDAY(prev_timestamp)) * 24, 1) AS "Часов простоя"
    FROM delays
    WHERE event_type = 'DEPARTED' 
      AND prev_timestamp IS NOT NULL
      AND (JULIANDAY(event_timestamp) - JULIANDAY(prev_timestamp)) * 24 > 48
    ORDER BY "Часов простоя" DESC
    LIMIT 10
    """
    df3 = pd.read_sql_query(query3, conn)
    if df3.empty:
        print("   Аномальных задержек не обнаружено (так и задумано или повезло)")
    else:
        print(df3.to_string(index=False))
    
    conn.close()
    
    # Сохраняем отчет
    output_path = "data/processed/bottlenecks_report.csv"
    os.makedirs("data/processed", exist_ok=True)
    df1.to_csv(output_path, index=False)
    print(f"\n📁 Отчет сохранен в {output_path}")

if __name__ == "__main__":
    import os
    analyze()

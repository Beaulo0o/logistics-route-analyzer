"""
Загрузчик данных из CSV в SQLite.
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "logistics.db"
CSV_PATH = "data/raw/delivery_log.csv"
SQL_INIT = "sql/01_init_db.sql"

def load_to_sqlite():
    print("📥 Загрузка данных в SQLite...")
    
    # Проверка наличия CSV
    if not os.path.exists(CSV_PATH):
        print(f"❌ Файл {CSV_PATH} не найден!")
        print("   Сначала запустите: python src/data_generator.py")
        return
    
    # Чтение CSV
    df = pd.read_csv(CSV_PATH)
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
    
    # Подключение к БД
    conn = sqlite3.connect(DB_PATH)
    
    # Применяем схему
    with open(SQL_INIT, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    # Загружаем данные
    df.to_sql('logistics_log', conn, if_exists='append', index=False)
    
    # Проверка
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logistics_log")
    count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT parcel_id) FROM logistics_log")
    parcels = cursor.fetchone()[0]
    
    print(f"✅ Загружено {count} записей ({parcels} уникальных посылок)")
    print(f"📁 База данных: {DB_PATH}")
    
    conn.close()

if __name__ == "__main__":
    load_to_sqlite()

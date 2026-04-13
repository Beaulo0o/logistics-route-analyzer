"""
Визуализация результатов анализа логистики.
"""
import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd
import seaborn as sns
import sqlite3
import os
import numpy as np

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

DB_PATH = "logistics.db"
OUTPUT_DIR = "output/figures"

def create_visualizations():
    print("🎨 Создание визуализаций...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. ГОРИЗОНТАЛЬНЫЙ БАР-ЧАРТ (УЗКИЕ МЕСТА)
    df_bottlenecks = pd.read_sql_query("""
        SELECT 
            location_name as warehouse, 
            avg_processing_hours, 
            parcels_processed,
            delayed_over_24h
        FROM v_bottlenecks 
        ORDER BY avg_processing_hours DESC 
        LIMIT 8
    """, conn)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = plt.cm.RdYlGn_r(df_bottlenecks['avg_processing_hours'] / df_bottlenecks['avg_processing_hours'].max())
    bars = ax.barh(df_bottlenecks['warehouse'], df_bottlenecks['avg_processing_hours'], color=colors)
    
    ax.bar_label(bars, fmt='%.1f ч', padding=5, fontsize=11, fontweight='bold')
    ax.axvline(x=8, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Норматив (8 часов)')
    
    ax.set_xlabel('Среднее время обработки (часы)', fontsize=13)
    ax.set_ylabel('')
    ax.set_title('🔍 ТОП-8 ПРОБЛЕМНЫХ ЛОГИСТИЧЕСКИХ ЦЕНТРОВ\nПо среднему времени простоя посылок', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.legend(loc='lower right')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Добавляем количество посылок справа
    for i, (wh, count) in enumerate(zip(df_bottlenecks['warehouse'], df_bottlenecks['parcels_processed'])):
        ax.text(df_bottlenecks['avg_processing_hours'].max() * 1.05, i, 
                f'{count} пос.', va='center', fontsize=10, color='gray')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/bottleneck_ranking.png", dpi=200, bbox_inches='tight', facecolor='white')
    print(f"   ✅ {OUTPUT_DIR}/bottleneck_ranking.png")
    
    # 2. ГИСТОГРАММА РАСПРЕДЕЛЕНИЯ ВРЕМЕНИ ОБРАБОТКИ
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    df_all_times = pd.read_sql_query("""
        WITH durations AS (
            SELECT 
                (JULIANDAY(event_timestamp) - JULIANDAY(LAG(event_timestamp) OVER (PARTITION BY parcel_id ORDER BY event_timestamp))) * 24 AS hours
            FROM logistics_log
            WHERE event_type = 'DEPARTED'
        )
        SELECT hours FROM durations WHERE hours IS NOT NULL AND hours < 100
    """, conn)
    
    ax2.hist(df_all_times['hours'], bins=40, edgecolor='black', alpha=0.7, color='steelblue')
    ax2.axvline(x=df_all_times['hours'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Среднее: {df_all_times["hours"].mean():.1f} ч')
    ax2.axvline(x=8, color='orange', linestyle=':', linewidth=2, label='Норматив: 8 ч')
    
    ax2.set_xlabel('Время обработки на складе (часы)', fontsize=13)
    ax2.set_ylabel('Количество посылок', fontsize=13)
    ax2.set_title('📊 РАСПРЕДЕЛЕНИЕ ВРЕМЕНИ ОБРАБОТКИ ПОСЫЛОК НА СКЛАДАХ', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/processing_time_distribution.png", dpi=200, bbox_inches='tight', facecolor='white')
    print(f"   ✅ {OUTPUT_DIR}/processing_time_distribution.png")
    
    # 3. ТЕПЛОВАЯ КАРТА ЗАГРУЗКИ ПО ДНЯМ НЕДЕЛИ И СКЛАДАМ
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    
    df_heatmap = pd.read_sql_query("""
        SELECT 
            location_name,
            CASE strftime('%w', event_timestamp)
                WHEN '0' THEN 'Вс'
                WHEN '1' THEN 'Пн'
                WHEN '2' THEN 'Вт'
                WHEN '3' THEN 'Ср'
                WHEN '4' THEN 'Чт'
                WHEN '5' THEN 'Пт'
                WHEN '6' THEN 'Сб'
            END as day_of_week,
            COUNT(*) as volume
        FROM logistics_log
        WHERE event_type = 'ARRIVED'
        GROUP BY location_name, day_of_week
    """, conn)
    
    pivot = df_heatmap.pivot(index='location_name', columns='day_of_week', values='volume')
    # Сортировка дней недели
    days_order = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    pivot = pivot.reindex(columns=days_order)
    
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax3, linewidths=0.5, cbar_kws={'label': 'Количество прибытий'})
    ax3.set_title('🔥 ТЕПЛОВАЯ КАРТА ЗАГРУЗКИ СКЛАДОВ ПО ДНЯМ НЕДЕЛИ', fontsize=14, fontweight='bold', pad=15)
    ax3.set_xlabel('День недели', fontsize=12)
    ax3.set_ylabel('')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/heatmap_weekly_load.png", dpi=200, bbox_inches='tight', facecolor='white')
    print(f"   ✅ {OUTPUT_DIR}/heatmap_weekly_load.png")
    
    conn.close()
    print("\n🎉 Визуализация завершена!")

if __name__ == "__main__":
    create_visualizations()

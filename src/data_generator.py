"""
Генератор синтетических логов для логистического анализа.
Создает реалистичные данные о перемещении посылок с внедренными проблемами (узкими местами).
"""
import csv
import random
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('ru_RU')

# Конфигурация генерации
NUM_PARCELS = 500
OUTPUT_PATH = "data/raw/delivery_log.csv"

# Логистические центры с разной эффективностью (коэффициент задержки)
WAREHOUSES = {
    "Москва-Хаб": {"base_delay": 3, "efficiency": 0.8, "region": "Центр"},
    "Санкт-Петербург-Сортировочный": {"base_delay": 4, "efficiency": 0.9, "region": "Северо-Запад"},
    "Екатеринбург-ЛЦ": {"base_delay": 5, "efficiency": 1.0, "region": "Урал"},
    "Новосибирск-Транзит": {"base_delay": 4, "efficiency": 1.2, "region": "Сибирь"},
    "Краснодар-Южный": {"base_delay": 6, "efficiency": 1.5, "region": "Юг"},
    "Нижний Новгород-Волга": {"base_delay": 8, "efficiency": 2.5, "region": "Поволжье"},  # ПРОБЛЕМНЫЙ СКЛАД
    "Казань-ЛЦ": {"base_delay": 5, "efficiency": 1.1, "region": "Поволжье"},
    "Владивосток-ДВ": {"base_delay": 7, "efficiency": 1.3, "region": "ДВ"},
    "Ростов-на-Дону": {"base_delay": 5, "efficiency": 1.0, "region": "Юг"},
    "Самара-ЛЦ": {"base_delay": 7, "efficiency": 2.0, "region": "Поволжье"},  # ПРОБЛЕМНЫЙ СКЛАД
}

def generate_route():
    """Генерирует случайный маршрут из 2-4 складов."""
    all_warehouses = list(WAREHOUSES.keys())
    num_stops = random.randint(2, 4)
    route = random.sample(all_warehouses, num_stops)
    return route

def generate_events(parcel_id, start_date):
    """Создает события для одной посылки."""
    events = []
    route = generate_route()
    weight = round(random.uniform(0.5, 25.0), 2)
    current_time = start_date + timedelta(hours=random.randint(0, 12))
    
    # Событие CREATED на первом складе
    origin = route[0]
    events.append({
        'parcel_id': parcel_id,
        'event_type': 'CREATED',
        'location_name': origin,
        'event_timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'weight_kg': weight,
        'distance_km': 0
    })
    
    # Проходим по всем складам маршрута
    for i in range(len(route)):
        warehouse = route[i]
        wh_data = WAREHOUSES[warehouse]
        
        # Симуляция времени в пути (если не первый склад)
        if i > 0:
            travel_hours = random.randint(4, 48)
            current_time += timedelta(hours=travel_hours)
            distance = random.randint(200, 1500)
            
            # ARRIVED
            events.append({
                'parcel_id': parcel_id,
                'event_type': 'ARRIVED',
                'location_name': warehouse,
                'event_timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'weight_kg': weight,
                'distance_km': distance
            })
        
        # Время обработки на складе (с внедренной проблемой)
        # Проблемные склады имеют высокий efficiency коэффициент
        base_hours = wh_data['base_delay']
        efficiency = wh_data['efficiency']
        
        # 20% шанс аномально долгой обработки (поломка сортировщика)
        if random.random() < 0.15:
            processing_hours = base_hours * efficiency * random.uniform(3.0, 6.0)
        else:
            processing_hours = base_hours * efficiency * random.uniform(0.8, 1.5)
        
        # Добавляем немного шума в зависимости от времени суток (ночные смены медленнее)
        if 22 <= current_time.hour or current_time.hour <= 6:
            processing_hours *= 1.3
            
        current_time += timedelta(hours=processing_hours)
        
        # DEPARTED (если не последний склад)
        if i < len(route) - 1:
            events.append({
                'parcel_id': parcel_id,
                'event_type': 'DEPARTED',
                'location_name': warehouse,
                'event_timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'weight_kg': weight,
                'distance_km': 0
            })
    
    # DELIVERED на последнем складе
    final_warehouse = route[-1]
    delivery_time = current_time + timedelta(hours=random.randint(2, 12))
    events.append({
        'parcel_id': parcel_id,
        'event_type': 'DELIVERED',
        'location_name': final_warehouse,
        'event_timestamp': delivery_time.strftime('%Y-%m-%d %H:%M:%S'),
        'weight_kg': weight,
        'distance_km': 0
    })
    
    return events

def main():
    print("🚀 Запуск генератора синтетических логов...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    all_events = []
    start_date = datetime(2024, 2, 1, 8, 0, 0)
    
    for i in range(NUM_PARCELS):
        parcel_id = f"PKG-{i+1:04d}"
        # Распределяем создание посылок по месяцу
        days_offset = random.randint(0, 25)
        parcel_start = start_date + timedelta(days=days_offset, hours=random.randint(0, 8))
        
        try:
            events = generate_events(parcel_id, parcel_start)
            all_events.extend(events)
        except Exception as e:
            print(f"Ошибка при генерации {parcel_id}: {e}")
    
    # Сортировка по времени для красоты
    all_events.sort(key=lambda x: x['event_timestamp'])
    
    # Запись в CSV
    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['parcel_id', 'event_type', 'location_name', 'event_timestamp', 'weight_kg', 'distance_km']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_events)
    
    print(f"✅ Сгенерировано {len(all_events)} событий для {NUM_PARCELS} посылок")
    print(f"📁 Файл сохранен: {OUTPUT_PATH}")
    print("\n📊 Статистика по складам:")
    for wh in ["Нижний Новгород-Волга", "Самара-ЛЦ"]:
        print(f"   - {wh}: внедрена проблема (аномальные задержки)")

if __name__ == "__main__":
    main()

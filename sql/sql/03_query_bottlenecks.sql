SELECT 
    location_name AS "Склад",
    parcels_processed AS "Обработано посылок",
    avg_processing_hours AS "Среднее время (ч)",
    max_processing_hours AS "Макс. время (ч)",
    delayed_over_24h AS "Задержек > 24ч"
FROM v_bottlenecks
WHERE avg_processing_hours > 2
ORDER BY avg_processing_hours DESC
LIMIT 10;

-- ЗАПРОС 2: Детализация по дням недели (когда пиковые нагрузки)
SELECT 
    location_name,
    strftime('%w', event_timestamp) AS day_of_week,
    COUNT(*) AS volume
FROM logistics_log
WHERE event_type = 'ARRIVED'
GROUP BY location_name, day_of_week
ORDER BY volume DESC;

-- ЗАПРОС 3: Топ-10 посылок с самыми большими задержками
WITH delays AS (
    SELECT 
        parcel_id,
        MIN(CASE WHEN event_type = 'CREATED' THEN event_timestamp END) AS created_time,
        MAX(CASE WHEN event_type = 'DELIVERED' THEN event_timestamp END) AS delivered_time
    FROM logistics_log
    GROUP BY parcel_id
    HAVING delivered_time IS NOT NULL
)
SELECT 
    parcel_id,
    ROUND((JULIANDAY(delivered_time) - JULIANDAY(created_time)) * 24, 1) AS total_hours,
    created_time,
    delivered_time
FROM delays
ORDER BY total_hours DESC
LIMIT 10;

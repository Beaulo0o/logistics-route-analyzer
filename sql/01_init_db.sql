DROP TABLE IF EXISTS logistics_log;

CREATE TABLE logistics_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('CREATED', 'ARRIVED', 'DEPARTED', 'DELIVERED', 'LOST')),
    location_name TEXT NOT NULL,
    event_timestamp DATETIME NOT NULL,
    weight_kg REAL,
    distance_km INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для ускорения аналитических запросов
CREATE INDEX idx_parcel_time ON logistics_log(parcel_id, event_timestamp);
CREATE INDEX idx_location ON logistics_log(location_name);
CREATE INDEX idx_event_type ON logistics_log(event_type);

-- Представление для быстрого доступа к проблемным точкам
DROP VIEW IF EXISTS v_bottlenecks;
CREATE VIEW v_bottlenecks AS
WITH events_ordered AS (
    SELECT 
        parcel_id,
        location_name,
        event_type,
        event_timestamp,
        LAG(event_timestamp) OVER (PARTITION BY parcel_id ORDER BY event_timestamp) AS prev_timestamp
    FROM logistics_log
    WHERE event_type IN ('ARRIVED', 'DEPARTED')
),
duration_calc AS (
    SELECT 
        parcel_id,
        location_name,
        ROUND((JULIANDAY(event_timestamp) - JULIANDAY(prev_timestamp)) * 24, 2) AS wait_hours
    FROM events_ordered
    WHERE event_type = 'DEPARTED' AND prev_timestamp IS NOT NULL
)
SELECT 
    location_name,
    COUNT(*) AS parcels_processed,
    ROUND(AVG(wait_hours), 2) AS avg_processing_hours,
    MAX(wait_hours) AS max_processing_hours,
    MIN(wait_hours) AS min_processing_hours,
    COUNT(CASE WHEN wait_hours > 24 THEN 1 END) AS delayed_over_24h
FROM duration_calc
GROUP BY location_name;

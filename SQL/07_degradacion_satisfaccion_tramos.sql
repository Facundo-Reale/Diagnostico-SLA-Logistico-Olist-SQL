-- =====================================================================
-- 07_degradacion_satisfaccion_tramos.sql
-- Propósito: Cuantificar el colapso del Customer Experience agrupando
-- el retraso en días respecto a la promesa de entrega (SLA).
-- =====================================================================

WITH calculo_dias AS (
    SELECT 
        r.review_score,
        DATE_DIFF(DATE(o.order_delivered_customer_date), DATE(o.order_estimated_delivery_date), DAY) AS dias_retraso
    FROM `brasil_ecommerce.orders` o
    JOIN `brasil_ecommerce.order_reviews` r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
      AND o.order_purchase_timestamp >= '2017-01-01'
),
etiquetas AS (
    SELECT 
        review_score,
        CASE 
            WHEN dias_retraso <= 0 THEN '1. 0 Días (A Tiempo)'
            WHEN dias_retraso = 1 THEN '2. 1 Día Tarde'
            WHEN dias_retraso = 2 THEN '3. 2 Días Tarde'
            WHEN dias_retraso BETWEEN 3 AND 5 THEN '4. 3 a 5 Días Tarde'
            WHEN dias_retraso BETWEEN 6 AND 10 THEN '5. 6 a 10 Días Tarde'
            ELSE '6. Más de 10 Días Tarde'
        END AS tramo_entrega
    FROM calculo_dias
)
SELECT 
    tramo_entrega,
    COUNT(*) AS total_pedidos,
    ROUND(AVG(review_score), 2) AS promedio_estrellas,
    ROUND(COUNTIF(review_score = 1) / COUNT(*) * 100, 1) AS pct_1_estrella,
    ROUND(COUNTIF(review_score = 2) / COUNT(*) * 100, 1) AS pct_2_estrellas,
    ROUND(COUNTIF(review_score = 3) / COUNT(*) * 100, 1) AS pct_3_estrellas,
    ROUND(COUNTIF(review_score = 4) / COUNT(*) * 100, 1) AS pct_4_estrellas,
    ROUND(COUNTIF(review_score = 5) / COUNT(*) * 100, 1) AS pct_5_estrellas
FROM etiquetas
GROUP BY tramo_entrega
ORDER BY tramo_entrega ASC;
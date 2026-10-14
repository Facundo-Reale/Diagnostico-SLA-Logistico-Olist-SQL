-- =====================================================================
-- 06_estandar_historico_reviews.sql
-- Propósito: Establecer la vara estándar histórica de satisfacción de
-- clientes (distribución porcentual de 1 a 5 estrellas).
-- =====================================================================

SELECT 
    'Estándar Histórico (Global)' AS escenario,
    COUNT(*) AS total_pedidos,
    ROUND(AVG(r.review_score), 2) AS promedio_estrellas,
    ROUND(COUNTIF(r.review_score = 1) / COUNT(*) * 100, 1) AS pct_1_estrella,
    ROUND(COUNTIF(r.review_score = 2) / COUNT(*) * 100, 1) AS pct_2_estrellas,
    ROUND(COUNTIF(r.review_score = 3) / COUNT(*) * 100, 1) AS pct_3_estrellas,
    ROUND(COUNTIF(r.review_score = 4) / COUNT(*) * 100, 1) AS pct_4_estrellas,
    ROUND(COUNTIF(r.review_score = 5) / COUNT(*) * 100, 1) AS pct_5_estrellas
FROM `brasil_ecommerce.orders` o
JOIN `brasil_ecommerce.order_reviews` r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp >= '2017-01-01';
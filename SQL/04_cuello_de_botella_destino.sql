-- =====================================================================
-- 04_cuello_de_botella_destino.sql
-- Propósito: Medir el rendimiento de la última milla por estado de destino
-- para aislar las asimetrías geográficas (SP vs. RJ).
-- =====================================================================

SELECT 
    customer_state AS estado_destino,
    COUNT(order_item_id) AS volumen_pedidos,
    ROUND(COUNT(order_item_id) * 100.0 / SUM(COUNT(order_item_id)) OVER(), 2) AS share_demanda,
    ROUND(AVG(is_sla_breach) * 100, 2) AS tasa_falla_sla
FROM `brasil_ecommerce.fct_order_deliveries`
GROUP BY customer_state
ORDER BY volumen_pedidos DESC;
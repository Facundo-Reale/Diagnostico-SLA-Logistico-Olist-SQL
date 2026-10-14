-- =====================================================================
-- 05_analisis_relacional_corredores.sql
-- Propósito: Cruce relacional origen-destino para aislar la tasa de falla
-- y la responsabilidad del transportista en el corredor crítico SP -> RJ.
-- =====================================================================

SELECT 
    seller_state AS estado_origen,
    customer_state AS estado_destino,
    COUNT(order_item_id) AS total_envios,
    ROUND(COUNT(order_item_id) * 100.0 / SUM(COUNT(order_item_id)) OVER(), 2) AS share_corredor_nacional,
    ROUND(AVG(is_sla_breach) * 100, 2) AS tasa_falla_corredor,
    ROUND(COUNTIF(is_sla_breach = 1 AND is_late_carrier_transit = 1) 
          / NULLIF(COUNTIF(is_sla_breach = 1), 0) * 100, 2) AS pct_responsabilidad_transporte
FROM `brasil_ecommerce.fct_order_deliveries`
GROUP BY seller_state, customer_state
HAVING total_envios > 100
ORDER BY tasa_falla_corredor DESC, total_envios DESC;
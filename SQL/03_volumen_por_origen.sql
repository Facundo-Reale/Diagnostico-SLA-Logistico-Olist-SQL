-- =====================================================================
-- 03_volumen_por_origen.sql
-- Propósito: Evaluar la concentración por estado de despacho y verificar
-- si el origen del paquete condiciona el éxito de la entrega.
-- =====================================================================

SELECT 
    seller_state AS estado_origen,
    COUNT(order_item_id) AS volumen_pedidos,
    ROUND(COUNT(order_item_id) * 100.0 / SUM(COUNT(order_item_id)) OVER(), 2) AS cuota_volumen_nacional,
    ROUND(AVG(is_sla_breach) * 100, 2) AS tasa_falla_general
FROM `brasil_ecommerce.fct_order_deliveries`
GROUP BY seller_state
ORDER BY volumen_pedidos DESC;
SELECT 
    COUNT(order_item_id) AS volumen_total,
    
    -- Tasa de Fallas Nacional Histórica
    ROUND(SUM(is_sla_breach) / COUNT(order_item_id) * 100, 2) AS pct_sla_breach,
    
    -- Distribución de Culpa Histórica
    ROUND(SUM(CASE WHEN is_sla_breach = 1 AND is_late_seller_dispatch = 1 AND is_late_carrier_transit = 0 THEN 1 ELSE 0 END) 
          / NULLIF(SUM(is_sla_breach), 0) * 100, 2) AS pct_culpa_vendedor,

    ROUND(SUM(CASE WHEN is_sla_breach = 1 AND is_late_seller_dispatch = 0 AND is_late_carrier_transit = 1 THEN 1 ELSE 0 END) 
          / NULLIF(SUM(is_sla_breach), 0) * 100, 2) AS pct_culpa_correo,

    ROUND(SUM(CASE WHEN is_sla_breach = 1 AND is_late_seller_dispatch = 1 AND is_late_carrier_transit = 1 THEN 1 ELSE 0 END) 
          / NULLIF(SUM(is_sla_breach), 0) * 100, 2) AS pct_culpa_compartida

FROM `brasil_ecommerce.fct_order_deliveries`
WHERE order_purchase_timestamp >= '2017-01-01';
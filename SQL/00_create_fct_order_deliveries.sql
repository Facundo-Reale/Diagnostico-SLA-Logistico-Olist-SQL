CREATE OR REPLACE TABLE `brasil_ecommerce.fct_order_deliveries` AS
SELECT 
    o.order_id,
    i.order_item_id,
    c.customer_id,
    c.customer_state,
    i.seller_id,
    s.seller_state,
    
    -- Fechas agregadas para análisis temporal
    o.order_purchase_timestamp,
    FORMAT_TIMESTAMP('%Y-%m', o.order_purchase_timestamp) AS purchase_month,
    
    -- Métricas de tiempo en días decimales
    ROUND(TIMESTAMP_DIFF(o.order_estimated_delivery_date, o.order_purchase_timestamp, HOUR) / 24.0, 2) AS expected_total_cycle_days,
    ROUND(TIMESTAMP_DIFF(o.order_delivered_customer_date, o.order_purchase_timestamp, HOUR) / 24.0, 2) AS actual_total_cycle_days,
    ROUND(TIMESTAMP_DIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date, HOUR) / 24.0, 2) AS sla_variance_days,
    
    -- Banderas lógicas (SLA y Atribución)
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 
        ELSE 0 
    END AS is_sla_breach,
    
    CASE 
        WHEN o.order_delivered_carrier_date > i.shipping_limit_date THEN 1 
        ELSE 0 
    END AS is_late_seller_dispatch,
    
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date 
         AND o.order_delivered_carrier_date <= i.shipping_limit_date THEN 1 
        ELSE 0 
    END AS is_late_carrier_transit

FROM `brasil_ecommerce.orders` o
INNER JOIN `brasil_ecommerce.items` i ON o.order_id = i.order_id
INNER JOIN `brasil_ecommerce.customers` c ON o.customer_id = c.customer_id
INNER JOIN `brasil_ecommerce.sellers` s ON i.seller_id = s.seller_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
  -- Filtros de coherencia cronológica (Data Quality)
  AND o.order_delivered_customer_date >= o.order_purchase_timestamp
  AND o.order_delivered_carrier_date >= o.order_purchase_timestamp
  AND o.order_delivered_customer_date >= o.order_delivered_carrier_date;
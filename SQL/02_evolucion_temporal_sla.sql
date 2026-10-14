SELECT 
    purchase_month,
    COUNT(order_item_id) AS total_pedidos,
    SUM(is_sla_breach) AS total_sla_breaches,
    ROUND(AVG(is_sla_breach) * 100, 2) AS tasa_sla_breach
FROM `brasil_ecommerce.fct_order_deliveries`
GROUP BY purchase_month
ORDER BY purchase_month ASC;
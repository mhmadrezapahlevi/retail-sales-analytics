-- =========================================================
-- Retail Sales Analytics — Business Analysis Queries
-- Assumes a "clean" version of sales_transactions
-- (negative qty / zero price / duplicate rows removed).
-- =========================================================

-- Q0. Core KPIs
SELECT
    ROUND(SUM(revenue), 0)                       AS total_revenue,
    COUNT(DISTINCT order_id)                     AS total_orders,
    COUNT(DISTINCT customer_id)                  AS total_customers,
    SUM(quantity)                                AS total_units_sold,
    ROUND(SUM(revenue - cogs), 0)                AS gross_profit,
    ROUND(100.0 * SUM(revenue - cogs) / NULLIF(SUM(revenue),0), 2) AS gross_margin_pct,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id),0), 0)    AS avg_order_value
FROM sales_transactions
WHERE quantity > 0 AND unit_price > 0;

-- Q1. Monthly revenue trend
SELECT
    DATE_TRUNC('month', order_date) AS month,
    ROUND(SUM(revenue), 0)          AS revenue,
    COUNT(DISTINCT order_id)        AS orders
FROM sales_transactions
WHERE quantity > 0 AND unit_price > 0
GROUP BY 1
ORDER BY 1;

-- Q2. Most profitable products / categories
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(t.revenue), 0)              AS revenue,
    ROUND(SUM(t.revenue - t.cogs), 0)      AS gross_profit,
    ROUND(100.0 * SUM(t.revenue - t.cogs) / NULLIF(SUM(t.revenue),0), 2) AS margin_pct,
    SUM(t.quantity)                        AS units_sold
FROM sales_transactions t
JOIN products p ON t.product_id = p.product_id
WHERE t.quantity > 0 AND t.unit_price > 0
GROUP BY p.product_name, p.category
ORDER BY revenue DESC;

-- Q2b. Category-level rollup
SELECT
    p.category,
    ROUND(SUM(t.revenue), 0) AS revenue,
    ROUND(100.0 * SUM(t.revenue - t.cogs) / NULLIF(SUM(t.revenue),0), 2) AS margin_pct
FROM sales_transactions t
JOIN products p ON t.product_id = p.product_id
WHERE t.quantity > 0 AND t.unit_price > 0
GROUP BY p.category
ORDER BY revenue DESC;

-- Q3. Revenue by region
SELECT
    region,
    ROUND(SUM(revenue), 0)   AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id),0), 0) AS avg_order_value
FROM sales_transactions
WHERE quantity > 0 AND unit_price > 0 AND region IS NOT NULL
GROUP BY region
ORDER BY revenue DESC;

-- Q4. Most valuable customers (top 10 by revenue)
SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    c.region,
    ROUND(SUM(t.revenue), 0)  AS total_revenue,
    COUNT(DISTINCT t.order_id) AS total_orders
FROM sales_transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.quantity > 0 AND t.unit_price > 0
GROUP BY c.customer_id, c.customer_name, c.segment, c.region
ORDER BY total_revenue DESC
LIMIT 10;

-- Q5. Average Order Value (overall and by segment)
SELECT
    c.segment,
    ROUND(SUM(t.revenue) / NULLIF(COUNT(DISTINCT t.order_id),0), 0) AS avg_order_value,
    COUNT(DISTINCT t.order_id) AS orders
FROM sales_transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.quantity > 0 AND t.unit_price > 0
GROUP BY c.segment
ORDER BY avg_order_value DESC;

-- Q6. Does discount level affect profit? (bucket discount_pct, compare margin)
SELECT
    CASE
        WHEN discount_pct = 0 THEN '0% (no discount)'
        WHEN discount_pct < 0.05 THEN '0-5%'
        WHEN discount_pct < 0.10 THEN '5-10%'
        WHEN discount_pct < 0.20 THEN '10-20%'
        ELSE '20%+'
    END AS discount_bucket,
    COUNT(*) AS line_items,
    ROUND(SUM(revenue), 0) AS revenue,
    ROUND(100.0 * SUM(revenue - cogs) / NULLIF(SUM(revenue),0), 2) AS margin_pct
FROM sales_transactions
WHERE quantity > 0 AND unit_price > 0
GROUP BY 1
ORDER BY 1;

-- Q7. Products with declining demand (compare last 3 months vs prior 3 months)
WITH monthly AS (
    SELECT
        product_id,
        DATE_TRUNC('month', order_date) AS month,
        SUM(quantity) AS units
    FROM sales_transactions
    WHERE quantity > 0
    GROUP BY product_id, DATE_TRUNC('month', order_date)
),
recent AS (
    SELECT product_id, SUM(units) AS units_recent
    FROM monthly
    WHERE month >= (SELECT MAX(month) FROM monthly) - INTERVAL '2 months'
    GROUP BY product_id
),
prior AS (
    SELECT product_id, SUM(units) AS units_prior
    FROM monthly
    WHERE month >= (SELECT MAX(month) FROM monthly) - INTERVAL '5 months'
      AND month <  (SELECT MAX(month) FROM monthly) - INTERVAL '2 months'
    GROUP BY product_id
)
SELECT
    p.product_name,
    COALESCE(pr.units_prior, 0)  AS units_prior_3mo,
    COALESCE(r.units_recent, 0)  AS units_recent_3mo,
    ROUND(100.0 * (COALESCE(r.units_recent,0) - COALESCE(pr.units_prior,0))
          / NULLIF(pr.units_prior, 0), 1) AS pct_change
FROM products p
LEFT JOIN recent r ON p.product_id = r.product_id
LEFT JOIN prior  pr ON p.product_id = pr.product_id
ORDER BY pct_change ASC;

-- Q8. Peak season check: revenue by month-of-year (averaged across years)
SELECT
    month_num,
    ROUND(AVG(monthly_rev), 0) AS avg_revenue
FROM (
    SELECT 
        DATE_TRUNC('month', order_date) AS ym,
        EXTRACT(MONTH FROM order_date) AS month_num,
        SUM(revenue) AS monthly_rev
    FROM sales_transactions
    WHERE quantity > 0 AND unit_price > 0
    GROUP BY DATE_TRUNC('month', order_date), EXTRACT(MONTH FROM order_date)
) sub
GROUP BY month_num
ORDER BY month_num;
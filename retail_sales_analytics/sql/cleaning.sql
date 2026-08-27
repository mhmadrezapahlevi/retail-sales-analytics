-- =========================================================
-- Retail Sales Analytics — Data Cleaning & Validation Queries
-- Run these BEFORE trusting any KPI or dashboard number.
-- =========================================================

-- 1. Row counts (sanity check against source CSV row counts)
SELECT COUNT(*) AS total_transactions FROM sales_transactions;
SELECT COUNT(*) AS total_customers    FROM customers;
SELECT COUNT(*) AS total_products     FROM products;

-- 2. Duplicate transaction rows (should be 0 after cleaning)
SELECT transaction_id, COUNT(*) AS n
FROM sales_transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- Full-row duplicates (same order/customer/product/qty/date repeated)
SELECT order_id, customer_id, product_id, order_date, quantity, COUNT(*) AS n
FROM sales_transactions
GROUP BY order_id, customer_id, product_id, order_date, quantity
HAVING COUNT(*) > 1;

-- 3. Missing / null values
SELECT
    SUM(CASE WHEN region      IS NULL THEN 1 ELSE 0 END) AS missing_region,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer,
    SUM(CASE WHEN product_id  IS NULL THEN 1 ELSE 0 END) AS missing_product,
    SUM(CASE WHEN order_date  IS NULL THEN 1 ELSE 0 END) AS missing_date
FROM sales_transactions;

SELECT COUNT(*) AS missing_city FROM customers WHERE city IS NULL;

-- 4. Invalid values: negative or zero quantity/price (data entry errors)
SELECT * FROM sales_transactions WHERE quantity <= 0;
SELECT * FROM sales_transactions WHERE unit_price <= 0;
SELECT * FROM sales_transactions WHERE revenue < 0;

-- 5. Outlier detection: revenue far above normal range (z-score style, simplified)
--    Flags rows where revenue is more than 5x the product's typical order revenue
WITH product_avg AS (
    SELECT product_id, AVG(revenue) AS avg_revenue, STDDEV(revenue) AS sd_revenue
    FROM sales_transactions
    WHERE revenue > 0
    GROUP BY product_id
)
SELECT t.*
FROM sales_transactions t
JOIN product_avg p ON t.product_id = p.product_id
WHERE t.revenue > p.avg_revenue + (5 * p.sd_revenue);

-- 6. Referential integrity: transactions pointing to customers/products that don't exist
SELECT t.*
FROM sales_transactions t
LEFT JOIN customers c ON t.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT t.*
FROM sales_transactions t
LEFT JOIN products p ON t.product_id = p.product_id
WHERE p.product_id IS NULL;

-- 7. Date range check (make sure nothing falls outside the expected 2024-2025 window)
SELECT MIN(order_date) AS earliest, MAX(order_date) AS latest
FROM sales_transactions;

-- 8. Suggested cleaning steps once issues above are found:
--    a) DELETE exact duplicate rows, keeping the first occurrence
--    b) Impute or drop rows with missing region (document which you chose)
--    c) Fix or exclude negative-quantity rows (likely returns entered incorrectly)
--    d) Cap/exclude extreme revenue outliers or re-derive revenue = qty * price - discount
--    e) Recompute revenue where unit_price = 0 (bad data) rather than trusting it blindly
-- =========================================================

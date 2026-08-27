-- =========================================================
-- Retail Sales Analytics — Database Schema
-- Target engine: PostgreSQL / SQLite compatible (minor tweaks may
-- be needed for MySQL, e.g. AUTOINCREMENT vs SERIAL)
-- =========================================================

DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- ---------------------------------------------------------
-- Dimension: customers
-- ---------------------------------------------------------
CREATE TABLE customers (
    customer_id   VARCHAR(10) PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    segment       VARCHAR(50),   -- Retail Store, Mini Market, Supermarket, Wholesaler, Online Reseller
    region        VARCHAR(50),
    city          VARCHAR(50),
    join_date     DATE
);

-- ---------------------------------------------------------
-- Dimension: products
-- ---------------------------------------------------------
CREATE TABLE products (
    product_id    VARCHAR(10) PRIMARY KEY,
    product_name  VARCHAR(150) NOT NULL,
    category      VARCHAR(50),
    unit_price    NUMERIC(12,2),
    unit_cost     NUMERIC(12,2)
);

-- ---------------------------------------------------------
-- Fact: sales_transactions (one row per order line item)
-- ---------------------------------------------------------
CREATE TABLE sales_transactions (
    transaction_id   VARCHAR(15) PRIMARY KEY,
    order_id         VARCHAR(15) NOT NULL,
    order_date       DATE NOT NULL,
    customer_id      VARCHAR(10) REFERENCES customers(customer_id),
    product_id       VARCHAR(10) REFERENCES products(product_id),
    region           VARCHAR(50),
    quantity         INTEGER,
    unit_price       NUMERIC(12,2),
    discount_pct     NUMERIC(6,4),
    discount_amount  NUMERIC(12,2),
    revenue          NUMERIC(14,2),
    cogs             NUMERIC(14,2)
);

CREATE INDEX idx_trx_order_date ON sales_transactions(order_date);
CREATE INDEX idx_trx_customer   ON sales_transactions(customer_id);
CREATE INDEX idx_trx_product    ON sales_transactions(product_id);
CREATE INDEX idx_trx_region     ON sales_transactions(region);

-- ---------------------------------------------------------
-- Notes for loading (example using SQLite CLI):
--   sqlite3 retail_sales.db
--   .mode csv
--   .import data/raw/customers.csv customers          (skip header row!)
--   .import data/raw/products.csv products
--   .import data/raw/sales_transactions.csv sales_transactions
--
-- Or use pandas.to_sql() from the EDA notebook to load faster and
-- handle the header row automatically. See notebooks/01_eda_starter.py
-- =========================================================

# Dashboard

Place your Power BI file here once built:

```
retail_sales_dashboard.pbix
```

## Suggested layout (Step 4)

```
RETAIL SALES DASHBOARD
------------------------------------------------
Revenue | Orders | AOV | Gross Profit   (KPI cards)
------------------------------------------------
Monthly Revenue Trend            (line chart)
------------------------------------------------
Revenue by Category | Revenue by Region  (bar charts)
------------------------------------------------
Top Products | Top Customers      (tables)
------------------------------------------------
Discount % vs Margin %            (scatter/bar)
```

Data source: `data/processed/sales_transactions_clean.csv`
(join with `data/raw/customers.csv` and `data/raw/products.csv` in
Power Query / the Data Model).

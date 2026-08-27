# %% [markdown]
# # Retail Sales Analytics — Step 1-3: Data Understanding, Cleaning & EDA
#
# This script is written in "notebook cell" style (`# %%` markers), so it can
# be opened directly as a Jupyter notebook in VS Code / Jupyter, or run as a
# plain .py script top to bottom.
#
# Workflow covered here:
#   1. Data Understanding  — shape, dtypes, missing values, duplicates
#   2. Data Cleaning        — fix/flag the issues found in step 1
#   3. Exploratory Data Analysis — trends, top products, regions, customers

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

RAW = "../data/raw"
PROCESSED = "../data/processed"

# %% [markdown]
# ## Step 1 — Data Understanding

# %%
customers = pd.read_csv(f"{RAW}/customers.csv", parse_dates=["join_date"])
products = pd.read_csv(f"{RAW}/products.csv")
trx = pd.read_csv(f"{RAW}/sales_transactions.csv", parse_dates=["order_date"])

print("customers:", customers.shape)
print("products:", products.shape)
print("sales_transactions:", trx.shape)

# %%
trx.info()

# %%
trx.describe(include="all").T

# %% [markdown]
# ### Missing values

# %%
print("Missing values per column (sales_transactions):")
print(trx.isna().sum())

print("\nMissing values per column (customers):")
print(customers.isna().sum())

# %% [markdown]
# ### Duplicates

# %%
n_dup_id = trx["transaction_id"].duplicated().sum()
n_dup_full = trx.duplicated(subset=["order_id", "customer_id", "product_id",
                                     "order_date", "quantity"]).sum()
print(f"Duplicate transaction_id rows: {n_dup_id}")
print(f"Duplicate full-row (order/customer/product/date/qty): {n_dup_full}")

# %% [markdown]
# ### Suspicious values (negative qty, zero price, extreme revenue)

# %%
print("Negative quantity rows:", (trx["quantity"] < 0).sum())
print("Zero/negative unit_price rows:", (trx["unit_price"] <= 0).sum())

q99 = trx["revenue"].quantile(0.99)
print(f"99th percentile revenue: {q99:,.0f}")
print("Rows above 10x the 99th percentile (likely outliers):",
      (trx["revenue"] > 10 * q99).sum())

# %% [markdown]
# ## Step 2 — Data Cleaning
#
# Decisions made here (document these in your case study / README):
#   - Drop exact duplicate rows (keep first occurrence)
#   - Drop rows with negative quantity or zero/negative unit_price
#     (data-entry errors; too few rows to justify imputing)
#   - Cap extreme revenue outliers by recomputing revenue from
#     quantity * unit_price - discount_amount, rather than trusting
#     the stored value blindly
#   - Fill missing `region` using the customer's region (join to customers)
#     where possible; drop the remainder (very small share of rows)

# %%
clean = trx.copy()

# 1. de-dup
clean = clean.drop_duplicates(subset=["transaction_id"])
clean = clean.drop_duplicates(
    subset=["order_id", "customer_id", "product_id", "order_date", "quantity"]
)

# 2. drop invalid rows
clean = clean[(clean["quantity"] > 0) & (clean["unit_price"] > 0)]

# 3. recompute revenue defensively and cap outliers
clean["revenue_recalc"] = (
    clean["quantity"] * clean["unit_price"] - clean["discount_amount"]
)
outlier_mask = clean["revenue"] > 10 * clean["revenue_recalc"].quantile(0.99)
clean.loc[outlier_mask, "revenue"] = clean.loc[outlier_mask, "revenue_recalc"]
clean = clean.drop(columns=["revenue_recalc"])

# 4. fill missing region from customers table
clean = clean.merge(
    customers[["customer_id", "region"]].rename(columns={"region": "region_lookup"}),
    on="customer_id", how="left"
)
clean["region"] = clean["region"].fillna(clean["region_lookup"])
clean = clean.drop(columns=["region_lookup"])
clean = clean.dropna(subset=["region"])

print("Rows before cleaning:", len(trx))
print("Rows after cleaning:", len(clean))

# %%
clean.to_csv(f"{PROCESSED}/sales_transactions_clean.csv", index=False)
print("Saved cleaned dataset to data/processed/sales_transactions_clean.csv")

# %% [markdown]
# ## Step 3 — Exploratory Data Analysis

# %% [markdown]
# ### Monthly revenue trend

# %%
monthly = (
    clean.assign(month=clean["order_date"].dt.to_period("M").dt.to_timestamp())
    .groupby("month")["revenue"].sum()
)

fig, ax = plt.subplots(figsize=(10, 4))
monthly.plot(ax=ax, marker="o")
ax.set_title("Monthly Revenue Trend")
ax.set_ylabel("Revenue (Rp)")
ax.set_xlabel("Month")
plt.tight_layout()
plt.savefig("../reports/monthly_revenue_trend.png", dpi=150)
plt.show()

# %% [markdown]
# ### Revenue & margin by category

# %%
merged = clean.merge(products, on="product_id")
merged["gross_profit"] = merged["revenue"] - merged["cogs"]

by_category = (
    merged.groupby("category")
    .agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum"))
    .assign(margin_pct=lambda d: 100 * d["gross_profit"] / d["revenue"])
    .sort_values("revenue", ascending=False)
)
print(by_category)

fig, ax = plt.subplots(figsize=(8, 4))
by_category["revenue"].plot(kind="bar", ax=ax)
ax.set_title("Revenue by Category")
ax.set_ylabel("Revenue (Rp)")
plt.tight_layout()
plt.savefig("../reports/revenue_by_category.png", dpi=150)
plt.show()

# %% [markdown]
# ### Revenue by region

# %%
by_region = clean.groupby("region")["revenue"].sum().sort_values(ascending=False)
print(by_region)

# %% [markdown]
# ### Top 10 customers by revenue

# %%
top_customers = (
    clean.merge(customers, on="customer_id")
    .groupby(["customer_id", "customer_name"])["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_customers)

# %% [markdown]
# ### Does discount level correlate with margin?

# %%
merged["discount_bucket"] = pd.cut(
    merged["discount_pct"],
    bins=[-0.01, 0, 0.05, 0.10, 0.20, 1],
    labels=["0%", "0-5%", "5-10%", "10-20%", "20%+"],
)
discount_margin = (
    merged.groupby("discount_bucket")
    .agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum"))
    .assign(margin_pct=lambda d: 100 * d["gross_profit"] / d["revenue"])
)
print(discount_margin)

# %% [markdown]
# ## Next steps
#
# - Load `data/processed/sales_transactions_clean.csv` into Power BI
#   (or re-run the queries in `sql/analysis_queries.sql` against a loaded DB)
# - Build the dashboard (Step 4)
# - Turn the patterns above into 3-5 written business insights + recommendations
#   (Step 5) — see reports/business_insights.md for a starter template

# %%

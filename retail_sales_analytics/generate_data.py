"""
Generate synthetic retail/distributor FMCG dataset for the
Retail Sales Analytics portfolio project.

Output:
  - data/raw/customers.csv
  - data/raw/products.csv
  - data/raw/sales_transactions.csv

Design goals:
  - ~500 customers, 15 products, ~25,000 orders, ~49,883 transaction rows
  - Period 2024-01-01 to 2025-12-31
  - Built-in realistic patterns: seasonality (Ramadan/Lebaran spike, year-end spike),
    a handful of "hero" products driving most revenue, regional skew,
    a slow margin erosion trend (so the "insight" step has something real to find),
    a few intentional data-quality issues (missing values, duplicates, a few
    negative/outlier rows) so the Data Cleaning step is meaningful.
"""

import numpy as np
import pandas as pd
from faker import Faker
import random

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("id_ID")
Faker.seed(SEED)

OUT = "/home/claude/retail_sales_analytics/data/raw"

# ---------------------------------------------------------------
# 1. CUSTOMERS
# ---------------------------------------------------------------
N_CUSTOMERS = 500

regions = ["Jawa Barat", "Jawa Tengah", "Jawa Timur", "DKI Jakarta",
           "Banten", "Sumatera Utara", "Sulawesi Selatan", "Bali"]
region_weights = [0.22, 0.14, 0.16, 0.18, 0.10, 0.08, 0.07, 0.05]

city_by_region = {
    "Jawa Barat": ["Bandung", "Bekasi", "Bogor", "Depok", "Cirebon"],
    "Jawa Tengah": ["Semarang", "Solo", "Magelang", "Tegal"],
    "Jawa Timur": ["Surabaya", "Malang", "Sidoarjo", "Kediri"],
    "DKI Jakarta": ["Jakarta Pusat", "Jakarta Selatan", "Jakarta Timur", "Jakarta Barat"],
    "Banten": ["Tangerang", "Serang", "Cilegon"],
    "Sumatera Utara": ["Medan", "Binjai"],
    "Sulawesi Selatan": ["Makassar", "Parepare"],
    "Bali": ["Denpasar", "Gianyar"],
}

segments = ["Retail Store", "Mini Market", "Supermarket", "Wholesaler", "Online Reseller"]
segment_weights = [0.40, 0.25, 0.12, 0.13, 0.10]

customers = []
for cid in range(1, N_CUSTOMERS + 1):
    region = np.random.choice(regions, p=region_weights)
    city = random.choice(city_by_region[region])
    join_date = fake.date_between(start_date="-3y", end_date="-3m")
    customers.append({
        "customer_id": f"CUST{cid:04d}",
        "customer_name": fake.company(),
        "segment": np.random.choice(segments, p=segment_weights),
        "region": region,
        "city": city,
        "join_date": join_date,
    })

customers_df = pd.DataFrame(customers)

# inject a few missing values (realistic messiness)
missing_idx = customers_df.sample(frac=0.02, random_state=SEED).index
customers_df.loc[missing_idx, "city"] = np.nan

customers_df.to_csv(f"{OUT}/customers.csv", index=False)
print(f"customers.csv -> {len(customers_df)} rows")

# ---------------------------------------------------------------
# 2. PRODUCTS
# ---------------------------------------------------------------
products_raw = [
    ("P001", "Minyak Goreng 1L",        "Sembako",       18500, 15800),
    ("P002", "Beras Premium 5kg",       "Sembako",       68000, 60500),
    ("P003", "Gula Pasir 1kg",          "Sembako",       15500, 13200),
    ("P004", "Mie Instan Goreng",       "Makanan Instan", 3200,  2450),
    ("P005", "Mie Instan Kuah",         "Makanan Instan", 3000,  2300),
    ("P006", "Kopi Sachet Renceng",     "Minuman",        9500,  7100),
    ("P007", "Teh Celup Box",           "Minuman",       12500,  9600),
    ("P008", "Susu UHT 1L",             "Minuman",       19500, 16400),
    ("P009", "Sabun Mandi Batang",      "Perawatan",      3800,  2900),
    ("P010", "Shampoo Sachet Renceng",  "Perawatan",      9800,  7500),
    ("P011", "Pasta Gigi 190g",         "Perawatan",     11500,  8900),
    ("P012", "Deterjen Bubuk 800g",     "Rumah Tangga",  16500, 13100),
    ("P013", "Pewangi Pakaian 900ml",   "Rumah Tangga",  13800, 10600),
    ("P014", "Air Mineral Galon",       "Minuman",       20000, 15500),
    ("P015", "Biskuit Kaleng",          "Makanan Ringan",28500, 22000),
]
products_df = pd.DataFrame(
    products_raw,
    columns=["product_id", "product_name", "category", "unit_price", "unit_cost"],
)
products_df.to_csv(f"{OUT}/products.csv", index=False)
print(f"products.csv -> {len(products_df)} rows")

# "hero" products get much higher demand weight -> makes Pareto-style insight visible
demand_weight = np.array([18, 10, 9, 14, 12, 8, 6, 7, 5, 6, 4, 5, 4, 6, 3], dtype=float)
demand_weight = demand_weight / demand_weight.sum()

# ---------------------------------------------------------------
# 3. SALES TRANSACTIONS (order_id groups multiple line items)
# ---------------------------------------------------------------
N_ORDERS = 25000
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2025-12-31")
all_days = pd.date_range(start_date, end_date, freq="D")

# Build a daily "demand index" with seasonality:
#  - baseline
#  - Ramadan/Lebaran bumps (approx Mar-Apr 2024, Mar 2025)
#  - year-end (Dec) bump
#  - slight upward trend over the 2 years
day_index = np.arange(len(all_days))
trend = 1 + 0.00025 * day_index  # slow growth over 2 years
weekday_factor = np.where(pd.Series(all_days).dt.weekday.isin([4, 5]), 1.15, 1.0)  # Fri/Sat busier

month = pd.Series(all_days).dt.month.values
year = pd.Series(all_days).dt.year.values
seasonal = np.ones(len(all_days))
seasonal[(month == 3) | (month == 4)] = 1.35   # Ramadan/Lebaran period (approx)
seasonal[month == 12] = 1.25                    # year-end
seasonal[month == 1] = 0.9                      # post-holiday dip

daily_weight = trend * weekday_factor * seasonal
daily_prob = daily_weight / daily_weight.sum()

order_dates = np.random.choice(all_days, size=N_ORDERS, p=daily_prob)
order_dates = pd.to_datetime(order_dates)

customer_ids = customers_df["customer_id"].values
# skew: a subset of customers order more often (Pareto-ish)
cust_weight = np.random.exponential(scale=1.0, size=len(customer_ids))
cust_weight = cust_weight / cust_weight.sum()
order_customers = np.random.choice(customer_ids, size=N_ORDERS, p=cust_weight)

region_map = customers_df.set_index("customer_id")["region"].to_dict()

rows = []
transaction_counter = 1
order_counter = 1

product_ids = products_df["product_id"].values
price_map = products_df.set_index("product_id")["unit_price"].to_dict()
cost_map = products_df.set_index("product_id")["unit_cost"].to_dict()

for i in range(N_ORDERS):
    order_id = f"ORD{order_counter:06d}"
    order_date = order_dates[i]
    cust_id = order_customers[i]
    region = region_map.get(cust_id, np.random.choice(regions))
    n_items = np.random.choice([1, 2, 3, 4, 5], p=[0.35, 0.30, 0.18, 0.10, 0.07])
    chosen_products = np.random.choice(product_ids, size=n_items, replace=False, p=demand_weight)

    for pid in chosen_products:
        qty = int(np.random.gamma(shape=2.0, scale=4.0)) + 1
        qty = min(qty, 60)
        base_price = price_map[pid]
        unit_cost = cost_map[pid]

        # margin erosion trend: discount tends to grow slightly over time,
        # and grows more for high-volume orders (a pattern to "discover")
        time_frac = (order_date - start_date).days / (end_date - start_date).days
        discount_pct = np.clip(
            np.random.normal(loc=0.03 + 0.05 * time_frac, scale=0.03), 0, 0.35
        )
        if qty >= 20:
            discount_pct = min(discount_pct + 0.05, 0.4)

        gross = qty * base_price
        discount_amount = round(gross * discount_pct, 2)
        revenue = round(gross - discount_amount, 2)
        cogs = round(qty * unit_cost, 2)

        rows.append({
            "transaction_id": f"TRX{transaction_counter:07d}",
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer_id": cust_id,
            "product_id": pid,
            "region": region,
            "quantity": qty,
            "unit_price": base_price,
            "discount_pct": round(discount_pct, 4),
            "discount_amount": discount_amount,
            "revenue": revenue,
            "cogs": cogs,
        })
        transaction_counter += 1

    order_counter += 1

trx_df = pd.DataFrame(rows)

# pad/trim to match the documented ~49,883 rows
target_rows = 49883
if len(trx_df) > target_rows:
    trx_df = trx_df.sample(n=target_rows, random_state=SEED).sort_values("transaction_id").reset_index(drop=True)
elif len(trx_df) < target_rows:
    extra_needed = target_rows - len(trx_df)
    extra = trx_df.sample(n=extra_needed, random_state=SEED, replace=True).copy()
    extra["transaction_id"] = [f"TRX{i:07d}" for i in range(transaction_counter, transaction_counter + extra_needed)]
    trx_df = pd.concat([trx_df, extra], ignore_index=True)

# ---- inject realistic data-quality issues on purpose ----
# a) some duplicate rows (~0.3%)
dupes = trx_df.sample(frac=0.003, random_state=SEED)
trx_df = pd.concat([trx_df, dupes], ignore_index=True)

# b) a few missing region values
miss_idx = trx_df.sample(frac=0.01, random_state=SEED + 1).index
trx_df.loc[miss_idx, "region"] = np.nan

# c) a handful of negative/zero quantity or price outliers (data entry errors)
err_idx = trx_df.sample(n=25, random_state=SEED + 2).index
trx_df.loc[err_idx[:10], "quantity"] = -1 * trx_df.loc[err_idx[:10], "quantity"]
trx_df.loc[err_idx[10:20], "unit_price"] = 0
trx_df.loc[err_idx[20:], "revenue"] = trx_df.loc[err_idx[20:], "revenue"] * 50  # extreme outliers

trx_df = trx_df.sort_values(["order_date", "order_id"]).reset_index(drop=True)
trx_df.to_csv(f"{OUT}/sales_transactions.csv", index=False)
print(f"sales_transactions.csv -> {len(trx_df)} rows, {trx_df['order_id'].nunique()} unique orders")

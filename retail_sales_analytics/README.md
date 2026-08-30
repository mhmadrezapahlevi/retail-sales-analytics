# Retail Sales Analytics Project

End-to-end analysis of retail sales data using Python and SQL to identify sales trends, product performance, customer behavior, and regional performance.

##  Overview
Menganalisis data penjualan retail sintetis (~50.000 transaksi) untuk menemukan business insights.

##  Key Findings
1. Sembako menghasilkan revenue terbesar tapi margin terendah (6,89%)
2. Diskon di atas 20% menyebabkan kerugian (margin -7,37%)
3. Revenue terkonsentrasi di Jawa Barat & DKI Jakarta
4. Top 2 customer menyumbang >Rp111 juta masing-masing
5. 3 produk dengan demand menurun: Mie Instan Kuah, Air Mineral Galon, Biskuit Kaleng

##  Tech Stack
- Python
- DuckDB
- Pandas
- SQL

##  Struktur Project
├── data/
│ └── raw/
│ ├── customers.csv
│ ├── products.csv
│ └── sales_transactions.csv
├── notebooks/
│ └── run_sql_analysis.py
├── sql/
│ └── analysis_queries.sql
├── BUSINESS_INSIGHTS.md
└── README.md


##  Cara Menjalankan

### Prerequisites
```bash
pip install duckdb pandas

Menjalankan Analisis SQL

cd notebooks
python 02_run.py

Menjalankan Query Spesifik

# Menjalankan Q7 saja (by nomor)
python run_sql_analysis.py 7

# Menjalankan Q7 (by label)
python run_sql_analysis.py Q7


logs/

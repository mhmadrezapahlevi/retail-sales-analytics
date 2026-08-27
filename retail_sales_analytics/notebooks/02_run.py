# run_sql_analysis.py (versi perbaikan untuk Q8)
import duckdb
import os
import sys
from pathlib import Path
import re

def setup_database():
    """Membuat koneksi DuckDB dan load semua CSV"""
    print("🔧 Menyiapkan database DuckDB...")
    
    con = duckdb.connect()
    data_path = Path('../data/raw')
    
    # Load CSV ke DuckDB
    try:
        con.execute(f"""
            CREATE TABLE customers AS 
            SELECT * FROM read_csv_auto('{data_path}/customers.csv')
        """)
        print("✅ customers.csv loaded")
        
        con.execute(f"""
            CREATE TABLE products AS 
            SELECT * FROM read_csv_auto('{data_path}/products.csv')
        """)
        print("✅ products.csv loaded")
        
        con.execute(f"""
            CREATE TABLE sales_transactions AS 
            SELECT * FROM read_csv_auto('{data_path}/sales_transactions.csv')
        """)
        print("✅ sales_transactions.csv loaded")
        
        # Tampilkan info tabel
        print("\n📊 Informasi Tabel:")
        for table in ['customers', 'products', 'sales_transactions']:
            count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"   - {table}: {count} baris")
        
        return con
    except Exception as e:
        print(f"❌ Error saat load CSV: {e}")
        return None

def fix_q8_query(query):
    """Fix Q8 query yang memiliki masalah alias"""
    # Cek jika ini adalah Q8
    if 'Q8' in query or 'Peak season' in query or 'EXTRACT(MONTH' in query:
        # Fix alias yang bermasalah
        query = query.replace(
            "EXTRACT(MONTH FROM order_date) AS order_date",
            "EXTRACT(MONTH FROM order_date) AS month_number"
        )
        
        # Fix referensi di outer query jika perlu
        query = query.replace(
            "GROUP BY month_number",
            "GROUP BY month_number"
        )
        
        print("🔧 Query Q8 otomatis diperbaiki (alias order_date → month_number)")
    
    return query

def extract_queries(sql_text):
    """Extract queries dengan lebih pintar"""
    sql_text = re.sub(r'/\*.*?\*/', '', sql_text, flags=re.DOTALL)
    
    queries = []
    current_query = []
    
    for line in sql_text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('--') and not current_query:
            continue
        
        current_query.append(line)
        
        if stripped.endswith(';'):
            query_text = '\n'.join(current_query).strip()
            query_text = query_text.rstrip(';').strip()
            
            if query_text and not all(l.strip().startswith('--') for l in query_text.split('\n') if l.strip()):
                # Fix Q8 query jika perlu
                query_text = fix_q8_query(query_text)
                queries.append(query_text)
            
            current_query = []
    
    if current_query:
        query_text = '\n'.join(current_query).strip()
        query_text = query_text.rstrip(';').strip()
        if query_text and not all(l.strip().startswith('--') for l in query_text.split('\n') if l.strip()):
            query_text = fix_q8_query(query_text)
            queries.append(query_text)
    
    return queries

def read_sql_file():
    """Membaca file SQL dan memisahkan queries"""
    sql_file = Path('../sql/analysis_queries.sql')
    
    if not sql_file.exists():
        print(f"❌ File SQL tidak ditemukan: {sql_file.absolute()}")
        return []
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_text = f.read()
        
        queries = extract_queries(sql_text)
        
        labeled_queries = []
        for q in queries:
            lines = q.split('\n')
            label = None
            for line in lines[:5]:
                match = re.search(r'--\s*(Q\d+[^:]*)', line, re.IGNORECASE)
                if match:
                    label = match.group(1).strip()
                    break
            
            if label:
                labeled_queries.append((label, q))
            else:
                labeled_queries.append((f"Query {len(labeled_queries)}", q))
        
        return labeled_queries
    except Exception as e:
        print(f"❌ Error membaca file SQL: {e}")
        return []

def run_single_query(con, query, query_label, query_num=None):
    """Menjalankan satu query dan menampilkan hasil"""
    print(f"\n{'='*70}")
    if query_num:
        print(f"📊 {query_label} (Query #{query_num})")
    else:
        print(f"📊 {query_label}")
    print(f"{'='*70}")
    
    query_lines = query.strip().split('\n')
    preview_lines = query_lines[:5]
    preview = '\n'.join(preview_lines)
    if len(query_lines) > 5:
        preview += f"\n... ({len(query_lines)} lines total)"
    print(f"SQL Preview:\n{preview}\n")
    
    try:
        result_df = con.execute(query).fetchdf()
        
        if result_df.empty:
            print("⚠️  (No results)")
        else:
            print(f"✅ Berhasil! {len(result_df)} baris hasil:")
            print(result_df.to_string(index=False))
        
        return result_df
    except Exception as e:
        print(f"❌ Error: {str(e)[:200]}...")
        
    
        if 'Q8' in query_label or 'Peak season' in query_label:
            print("\n🔄 Mencoba query Q8 versi alternatif...")
            try:
                alt_query = """
                SELECT
                    EXTRACT(MONTH FROM order_date) AS month_number,
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
                ORDER BY month_num
                """
                result_df = con.execute(alt_query).fetchdf()
                print(f"✅ Berhasil dengan query alternatif! {len(result_df)} baris hasil:")
                print(result_df.to_string(index=False))
                return result_df
            except Exception as e2:
                print(f"❌ Query alternatif juga error: {str(e2)[:200]}")
        
        return None

def run_all_queries():
    """Fungsi utama untuk menjalankan semua query"""
    print("\n" + "="*70)
    print("🚀 ANALISIS SQL RETAIL DENGAN DUCKDB")
    print("="*70)
    
    con = setup_database()
    if con is None:
        return None, None
    
    labeled_queries = read_sql_file()
    if not labeled_queries:
        print("\n❌ Tidak ada query untuk dijalankan.")
        return con, None
    
    print(f"\n📝 Ditemukan {len(labeled_queries)} query dalam file SQL")
    print("Mulai eksekusi...\n")
    
    results = {}
    successful = 0
    
    for i, (label, query) in enumerate(labeled_queries, 1):
        result = run_single_query(con, query, label, i)
        if result is not None:
            results[label] = result
            successful += 1
    
    print(f"\n{'='*70}")
    print(f"RINGKASAN EKSEKUSI")
    print(f"{'='*70}")
    print(f"Total query: {len(labeled_queries)}")
    print(f" Berhasil: {successful}")
    print(f" Gagal: {len(labeled_queries) - successful}")
    
    if successful > 0:
        print("\n Hasil query tersimpan dalam dictionary 'results'")
    
    return con, results

def main():
    """Main function"""
    con, results = run_all_queries()
    
    if con:
        con.close()
        print("\n Koneksi database ditutup.")
    
    return results

if __name__ == "__main__":
    results = main()
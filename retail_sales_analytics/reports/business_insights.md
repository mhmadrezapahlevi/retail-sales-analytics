# Business Insights — Retail Sales Analytics

## 1. Sembako menghasilkan revenue terbesar, tapi margin-nya paling tipis
Sembako menyumbang **Rp3,79 miliar** revenue (jauh di atas kategori lain),
tapi gross margin-nya cuma **6,89%** — margin terendah dari semua kategori.
Bandingkan dengan Makanan Instan (**19,12%**), Perawatan (**18,69%**), dan
Rumah Tangga (**16,29%**) yang jauh lebih sehat meski volumenya kecil.

**Rekomendasi:** Pertumbuhan revenue dari Sembako tidak otomatis berarti
pertumbuhan profit. Perusahaan sebaiknya mendorong cross-sell kategori
bermargin tinggi (Perawatan, Makanan Instan) ke pelanggan yang selama ini
hanya membeli Sembako, alih-alih hanya mengejar volume Sembako.

## 2. Diskon di atas 20% membuat perusahaan rugi, bukan cuma margin turun
Pola margin per bucket diskon sangat jelas dan konsisten menurun:

| Diskon | Margin |
|---|---|
| 0% | 16,65% |
| 0–5% | 14,20% |
| 5–10% | 10,08% |
| 10–20% | 6,23% |
| 20%+ | **-7,37% (rugi)** |

Transaksi dengan diskon 20% ke atas secara total menghasilkan gross
profit **negatif** (-Rp321 ribu dari Rp4,36 juta revenue).

**Rekomendasi:** Batasi diskon diskresi maksimal di kisaran 10%, kecuali
untuk kesepakatan volume yang terdokumentasi resmi. Perlu audit siapa yang
menyetujui diskon di atas 20%, karena secara matematis transaksi itu
merugikan perusahaan.

## 3. Revenue terkonsentrasi di Jawa Barat & DKI Jakarta
Dua region ini menyumbang **Rp1,86 miliar + Rp1,18 miliar = Rp3,04 miliar**,
lebih besar dari gabungan Sulawesi Selatan dan Bali (**Rp376 juta + Rp363
juta = Rp739 juta**) — sekitar 4x lipat lebih kecil.

**Rekomendasi:** Investigasi apakah rendahnya revenue di Bali dan Sulawesi
Selatan disebabkan oleh keterbatasan distribusi/jangkauan sales, atau
memang demand pasarnya lebih kecil. Kalau soal distribusi, ini peluang
ekspansi; kalau soal demand, alokasi resource sebaiknya tetap fokus ke
Jawa Barat & DKI Jakarta.

## 4. Revenue juga terkonsentrasi di segelintir customer besar
Top 2 customer (**PD Hastuti Tbk** dan **CV Agustina**) masing-masing
menyumbang lebih dari **Rp111 juta**, jauh di atas customer besar lainnya
yang berada di kisaran Rp56–86 juta. Total 10 customer teratas menyumbang
porsi signifikan dari keseluruhan revenue.

**Rekomendasi:** Bangun program account management khusus untuk top-10
hingga top-20 customer (kontak dedicated, prioritas fulfillment) untuk
mengurangi risiko kehilangan revenue besar kalau salah satu dari mereka
churn.

## 5. Tiga produk dengan demand menurun: Mie Instan Kuah, Air Mineral Galon, dan Biskuit Kaleng

Berdasarkan hasil Q7, terdapat **3 produk yang mengalami penurunan demand** dalam 3 bulan terakhir dibandingkan 3 bulan sebelumnya:

| Produk | Units Prior 3mo | Units Recent 3mo | % Change |
|---|---|---|---|
| Mie Instan Kuah | 5.558 | 5.345 | **-3,8%** |
| Air Mineral Galon | 3.037 | 2.940 | **-3,2%** |
| Biskuit Kaleng | 1.495 | 1.481 | **-0,9%** |

**Analisis & Hipotesis:**

1. **Mie Instan Kuah (-3,8%)** - Penurunan paling signifikan di antara produk yang turun. Menariknya, saudaranya **Mie Instan Goreng justru naik +5,0%**. Ini bisa mengindikasikan **pergeseran preferensi konsumen** dari varian kuah ke goreng, atau adanya **promosi/aktivitas kompetitor** khusus untuk kategori mie instan.

2. **Air Mineral Galon (-3,2%)** - Penurunan ini mungkin dipengaruhi oleh **faktor musiman** (jika data mencakup transisi musim hujan ke kemarau, konsumsi air galon bisa menurun karena cuaca lebih dingin). Bisa juga karena **persaingan harga** dengan produk sejenis.

3. **Biskuit Kaleng (-0,9%)** - Penurunan tipis, mungkin masih dalam **fluktuasi normal**. Perlu monitoring 1-2 bulan ke depan untuk memastikan apakah ini tren atau noise. Namun, Biskuit Kaleng adalah **produk dengan margin tertinggi (20,57%)** di Q2b, jadi penurunan kecil sekalipun patut diperhatikan.

**Rekomendasi:**

1. **Untuk Mie Instan Kuah:** Lakukan **analisis basket** untuk melihat apakah pelanggan yang biasanya beli Mie Instan Kuah beralih ke Mie Instan Goreng (kanibalisme internal) atau hilang ke kompetitor. Jika kanibalisme, tidak masalah karena revenue tetap masuk; jika kompetitor, perlu evaluasi harga/promosi.

2. **Untuk Air Mineral Galon:** Cek apakah penurunan ini **pola musiman berulang** (lihat data tahun sebelumnya). Jika ya, siapkan strategi demand management; jika tidak, investigate **ketersediaan stok** atau **perubahan rute distribusi** di region tertentu.

3. **Untuk Biskuit Kaleng:** Karena ini produk high-margin, **prioritaskan dalam program cross-sell** ke pelanggan Sembako yang sudah diidentifikasi di Insight 1. Biskuit Kaleng bisa jadi add-on sempurna untuk pelanggan grosir yang membeli Beras Premium dan Minyak Goreng.

4. **Monitoring berkelanjutan:** Buat **early warning system** untuk produk dengan penurunan demand >3% dalam 3 bulan beruntun. Ini akan membantu tim sales dan supply chain bertindak proaktif sebelum penurunan semakin dalam.

**Temuan tambahan yang menarik:** Sebagian besar produk justru mengalami **kenaikan demand**. Produk dengan pertumbuhan tertinggi adalah **Sabun Mandi Batang (+36,3%)** dan **Pasta Gigi (+32,3%)**, keduanya dari kategori **Perawatan** yang juga merupakan kategori margin tinggi (18,69%). Ini memperkuat Insight 1 bahwa mendorong kategori Perawatan bisa jadi strategi profit yang bagus.

---

### Ringkasan untuk CV / README (Update)

> "Menganalisis data penjualan retail sintetis (~50rb transaksi) dan menemukan bahwa kategori dengan revenue terbesar (Sembako) justru memiliki margin terendah (6,89% vs rata-rata 15%+ kategori lain), diskon di atas 20% menyebabkan kerugian (-7,37% margin), dan 3 produk mengalami penurunan demand (Mie Instan Kuah -3,8%, Air Mineral Galon -3,2%, Biskuit Kaleng -0,9%). Insight ini digunakan untuk merekomendasikan strategi cross-sell, kebijakan diskon, dan program monitoring demand produk."

### How to use this file
1. Run `notebooks/01_eda_starter.py` and `sql/analysis_queries.sql` to get
   your real numbers.
2. Replace every placeholder above with the actual figures.
3. Keep the "finding → so what → recommendation" structure — that's what
   separates a Data Analyst case study from a chart dump.
4. Copy the final 3-5 insights into your README case study and your CV
   project bullet points.

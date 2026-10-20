# ML Experiment Studio — Proyek 3

Aplikasi eksplorasi machine learning berbasis Streamlit dengan antarmuka modern bernuansa Cobalt Blue dan Orange. Proyek menyediakan ruang eksperimen untuk klasifikasi (*supervised learning*) dan pengelompokan pola (*unsupervised learning*).

## Fitur utama

### Supervised Learning
- Dataset contoh Iris atau unggah dataset CSV sendiri.
- Pilih kolom target, rasio data uji, algoritma, dan parameter model.
- Algoritma: Random Forest dan Support Vector Machine (SVM).
- Preprocessing otomatis: imputasi nilai kosong, one-hot encoding untuk fitur kategorik, dan standardisasi fitur numerik.
- Evaluasi nyata pada data uji: Accuracy, Precision, Recall, F1-score, confusion matrix, dan classification report.
- Feature importance untuk Random Forest dan unduhan prediksi data uji sebagai CSV.

### Unsupervised Learning
- Dataset contoh perilaku customer atau unggah CSV sendiri.
- Pilih fitur numerik, algoritma, dan parameter clustering.
- Algoritma: K-Means dan DBSCAN.
- Imputasi nilai kosong dan standardisasi fitur sebelum clustering.
- Visualisasi scatter plot interaktif, distribusi ukuran cluster, silhouette score bila valid, identifikasi noise untuk DBSCAN, dan ekspor label cluster ke CSV.

### UI/UX
- Palet utama: Cobalt Blue `#153EBD`, Dark Cobalt `#102F91`, Royal Blue `#4169E1`, Orange `#FF7A1A`, Background `#F4F7FF`, dan White `#FFFFFF`.
- Dashboard ringkasan, kartu metrik, panel konfigurasi, profil dataset, status eksperimen, grafik Plotly, serta layout responsif.

## Menjalankan aplikasi

Disarankan menggunakan Python 3.10 atau lebih baru.

```bash
# 1. Buat dan aktifkan virtual environment (opsional tetapi disarankan)
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 2. Instal dependensi
python -m pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py
```

Buka URL lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`.

## Dataset

- `data/dataset_supervised.csv`: data Iris dengan kolom target `species`.
- `data/dataset_unsupervised.csv`: data customer dengan kolom numerik seperti `Age`, `Annual_Income`, dan `Spending_Score`.

Untuk dataset CSV milik sendiri, gunakan baris sebagai observasi dan kolom sebagai variabel. Pada Supervised, sediakan satu kolom label/target. Pada Unsupervised, pilih setidaknya dua kolom numerik yang relevan dan hindari kolom ID jika ID bukan bagian dari sinyal yang ingin dianalisis.

## Struktur proyek

```text
ML-PROYEK3/
├── app.py
├── pages/
│   ├── 1_Supervised.py
│   └── 2_Unsupervised.py
├── utils/
│   ├── __init__.py
│   ├── ui.py
│   ├── preprocessing.py
│   └── evaluation.py
├── data/
│   ├── dataset_supervised.csv
│   └── dataset_unsupervised.csv
├── models/
│   └── train_models.py
├── .streamlit/config.toml
└── requirements.txt
```

> Catatan: nilai metrik mengikuti dataset, pemilihan fitur, dan parameter yang dijalankan. Hasil eksperimen adalah alat bantu analisis, bukan jaminan performa model pada data baru.

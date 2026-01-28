# Wiguna Repair Agent

Aplikasi agen cerdas untuk diagnosa masalah mobil, dibangun khusus untuk **Bengkel Wiguna**. Aplikasi ini menggunakan RAG (Retrieval Augmented Generation) untuk memberikan saran perbaikan berdasarkan SOP bengkel.

## Fitur Utama
- 🚗 **Diagnosa Cerdas**: Menganalisa keluhan mobil berdasarkan Merek, Model, Tahun, dan Masalah.
- 📚 **SOP Based**: Jawaban didasarkan pada dokumen SOP Bengkel Wiguna yang terindeks (bukan halusinasi AI).
- ☁️ **Cloud Ready**: Siap dideploy ke Vercel dengan database Milvus Cloud (Zilliz).
- 🇮🇩 **Bahasa Indonesia**: Didesain penuh untuk pasar lokal.

---

## 🚀 Setup Project (Lokal)

### 1. Persiapan Environment
Pastikan sudah install Python 3.11+.

```bash
# Clone repo
git clone https://github.com/Doddy70/wiguna-repair-agent.git
cd wiguna-repair-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Database (Milvus/Zilliz Cloud)
Karena aplikasi ini menggunakan Vector Database untuk menyimpan SOP, kamu perlu setup database dulu.

1.  Buat akun di [Zilliz Cloud](https://zilliz.com/).
2.  Buat Cluster baru (Free Tier cukup).
3.  Ambil **URI** dan **Token** dari dashboard.

### 3. Konfigurasi Environment (`.env`)
Buat file `.env` di root folder dan isi:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxxx

# Milvus / Zilliz Cloud Config
MILVUS_URI=https://in03-xxxx.api.gcp-us-west1.zillizcloud.com
MILVUS_TOKEN=your_token_here

# App Config
FLASK_ENV=development
FLASK_DEBUG=True
LLM_TYPE=openai
EMBEDDINGS_TYPE=openai
```

### 4. Upload Data SOP ke Cloud
Jalankan script ini sekali saja untuk mengupload semua file PDF di folder SOP ke dalam database cloud:

```bash
python gen_milvus_batch.py
```

### 5. Jalankan Aplikasi
```bash
python run.py
```
Akses di browser: `http://localhost:5000`

---

## 🌐 Cara Upload ke GitHub

Jika kamu ingin menyimpan kode ini ke GitHub:

```bash
# 1. Cek status file
git status

# 2. Tambahkan semua file perubahan
git add .

# 3. Simpan perubahan (Commit)
git commit -m "Update: Siap deploy Vercel & Zilliz Support"

# 4. Upload ke GitHub (Push)
git push origin main
```

---

## ☁️ Cara Deploy ke Vercel

1.  Push kode terbaru ke GitHub.
2.  Buka [Vercel Dashboard](https://vercel.com/dashboard) -> **Add New Project**.
3.  Import repository `wiguna-repair-agent`.
4.  Di bagian **Environment Variables**, masukkan 3 kunci penting:
    *   `OPENAI_API_KEY`
    *   `MILVUS_URI`
    *   `MILVUS_TOKEN`
5.  Klik **Deploy**.

---

## Struktur Folder

```
.
├── api/                    # Vercel entry point
├── app/                    # Source code utama
│   ├── routes/             # API Routes
│   ├── services/           # Logic OpenAI/LLM
│   ├── templates/          # File HTML (Frontend)
│   └── utils/              # Retrievers & Tools
├── gen_milvus_batch.py     # Script upload PDF ke Cloud DB
├── requirements.txt        # Daftar library Python
├── vercel.json             # Config deploy Vercel
└── README.md               # Dokumentasi ini
```

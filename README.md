# ResuMatch — Akıllı CV Toplama & Eşleştirme Sistemi

> **Durum: Geliştirme Aşamasında** 🚧  
> Bu proje aktif olarak geliştirilmektedir. Aşağıdaki özellikler kademeli olarak eklenecektir.

---

## Proje Hakkında

ResuMatch, GitHub üzerindeki açık kaynak CV'leri otomatik olarak toplayıp, makine öğrenmesi teknikleriyle iş ilanlarına göre skorlayan ve en uygun adayları sıralayan bir sistemdir. İnsan kaynakları süreçlerini otomatize etmek ve büyük veri setleri üzerinde CV analizi yapabilmek amacıyla geliştirilmektedir.

---

## Kullanılan Teknolojiler & Teknikler

### Veri Toplama (Scraping)
- **GitHub REST API v3** — PDF formatındaki CV'leri aramak ve ham URL'lerini elde etmek için kullanıldı. Selenium tabanlı yaklaşım yerine API tercih edildi; daha stabil, ban riski yok.
- **Requests** — HTTP istekleri ve PDF indirme işlemleri
- **pdfplumber / PyMuPDF (fitz)** — İndirilen PDF'lerden metin çıkarma; iki kütüphane birbirinin fallback'i olarak kullanıldı

### Veri Ön İşleme (Preprocessing)
- **NLTK** — Stop word temizleme (İngilizce)
- **Regex** — Gereksiz karakterleri, sayıları ve boşlukları temizleme
- **Pandas** — CSV okuma/yazma, boş satır temizleme, veri manipülasyonu

### Makine Öğrenmesi & NLP
- **TF-IDF (TfidfVectorizer)** — CV metinlerini sayısal vektörlere dönüştürme
- **Cosine Similarity** — İş ilanı ile CV vektörleri arasındaki benzerlik skoru hesaplama
- **Logistic Regression** — CV kategorisi tahmini için sınıflandırma modeli (sklearn)

### Görselleştirme & Raporlama
- **Matplotlib** — En iyi adayların uygunluk skoru grafiği
- **CSV Export** — Risk analizi ve puanlama sonuçlarının dışa aktarımı

---

## Proje Yapısı

```
makineogrenmesi/
│
├── scraper/
│   ├── __init__.py
│   ├── github_scraper.py      # GitHub API ile PDF CV arama
│   ├── downloader.py          # PDF indirme
│   ├── pdf_to_text.py         # PDF → metin dönüşümü
│   ├── utils.py               # Yardımcı fonksiyonlar
│   └── main_scraper.py        # Scraping pipeline'ını çalıştırır
│
├── data/
│   ├── cv_dataset_hazir.csv
│   └── cv_dataset_islenmis.csv
│
├── preprocess.py              # Temel metin temizleme
├── analiz.py                  # Veri analizi ve temizleme pipeline'ı
├── model.py                   # Model eğitimi ve tahmin
├── puanlama.py                # TF-IDF benzerlik & risk analizi
├── .env                       # API token (git'e atılmaz!)
├── .gitignore
└── README.md
```

---

## Kurulum & Çalıştırma

### 1. Gerekli kütüphaneleri kur
```bash
pip install requests pdfplumber pymupdf pandas scikit-learn nltk matplotlib python-dotenv
```

### 2. `.env` dosyası oluştur
```
GITHUB_TOKEN=ghp_senin_tokenin
```

> GitHub token almak için: Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → `repo` scope'u seç

### 3. CV'leri topla
```bash
python -m scraper.main_scraper
```

### 4. Veriyi temizle
```bash
python analiz.py
```

### 5. Modeli eğit
```bash
python model.py
```

### 6. Puanlama & görselleştirme
```bash
python puanlama.py
```

---

## Planlanan Özellikler

- [ ] Daha gelişmiş NLP modeli (BERT / sentence-transformers)
- [ ] Web arayüzü — iş ilanı girip anlık eşleştirme
- [ ] Çoklu dil desteği (Türkçe CV'ler)
- [ ] Otomatik veri güncelleme (scheduled scraping)
- [ ] Docker ile containerize edilmiş deployment
- [ ] OCR entegrasyonu (taranmış PDF'ler için)

---

## Notlar

- `.env` dosyası ve `data_downloaded/` klasörü `.gitignore`'a eklenmiştir, GitHub'a gönderilmez.
- GitHub API rate limit: token olmadan saatte 10, token ile saatte 5000 istek.
- Bazı GitHub repo'larındaki PDF'ler placeholder içerebilir; sorgu parametreleri buna göre optimize edilmiştir.

---

## Geliştirici

Azra Akşahin
İrem Kalaycı

# 🎓 DGS Koçu

## Yapay Zeka Destekli DGS Tercih ve Sınav Analiz Sistemi

**DGS Koçu**, Dikey Geçiş Sınavı’na hazırlanan öğrencilerin puan hesaplama, tercih analizi ve sınav stratejisi süreçlerini tek platformda birleştiren yapay zeka destekli bir karar destek sistemidir.

Sistem; öğrencinin tahmini DGS puanını hesaplar, hedeflediği bölüme göre geçmiş yerleştirme verilerini analiz eder, 2026 yılı için tahmini taban puan üretir ve öğrencinin puanına göre tercihin uygunluk durumunu yorumlar.

---

## 🚀 Projenin Amacı

Bu projenin amacı, DGS adaylarının tercih döneminde yalnızca puana bakarak karar vermesi yerine; geçmiş taban puanlar, kontenjanlar, bölüm eğilimleri ve sınav konu dağılımları gibi verileri birlikte değerlendirebilmesini sağlamaktır.

DGS Koçu sayesinde kullanıcı:

- Tahmini DGS puanını hesaplayabilir.
- Hedef bölümünü aratabilir.
- Geçmiş yıllara ait taban puanları görebilir.
- 2026 yılı için tahmini taban puanları inceleyebilir.
- Puanına göre tercihinin uygun, sınırda veya zor olduğunu öğrenebilir.
- Matematik konu dağılımı tahminlerini inceleyebilir.
- Deneysel soru analiz modülüyle soru metninin hangi konuya ait olduğunu tahmin ettirebilir.

---

## 🧩 Proje Modülleri

| Modül | Açıklama |
|---|---|
| **DGS Puan Hesaplama** | Matematik, Türkçe netleri ve 4’lük diploma notu ile tahmini DGS puanı hesaplar. |
| **Tercih Analizi** | Öğrenci puanını 2026 tahmini taban puanlarla karşılaştırır. |
| **Taban Puan Tahmini** | 2021-2025 yerleştirme verilerinden 2026 tahmini taban puan üretir. |
| **Soru Dağılımı Tahmini** | Geçmiş DGS Matematik konu dağılımlarından 2026 soru tahmini yapar. |
| **Soru Analizi** | NLP modeliyle soru metninin hangi konuya yakın olduğunu tahmin eder. |

---

## ⭐ Temel Özellikler

### 1. DGS Tahmini Puan Hesaplama

Kullanıcı Matematik ve Türkçe doğru/yanlış sayılarını girer. Sistem netleri şu mantıkla hesaplar:

**Net = Doğru Sayısı - (Yanlış Sayısı / 4)**

Kullanıcı ayrıca 4’lük sistemde diploma notunu girer. Sistem bu notu 100’lük sisteme dönüştürür ve tahmini DGS puanı üretir.

Hesaplanan puan otomatik olarak tercih analiz paneline aktarılır.

---

### 2. Tercih ve Taban Puan Analizi

Kullanıcı hedeflediği bölüm adını yazar. Sistem geçmiş yerleştirme verilerinden oluşturulan 2026 tahmini taban puan ile öğrencinin puanını karşılaştırır.

Tercih sonuçları şu şekilde yorumlanır:

| Durum | Anlamı |
|---|---|
| **Uygun** | Öğrencinin puanı tahmini taban puanın üzerindedir. |
| **Sınırda** | Öğrencinin puanı tahmini taban puana çok yakındır. |
| **Biraz Daha Zorla** | Öğrencinin puanı biraz düşüktür ancak çalışmayla yaklaşılabilir. |
| **Zor** | Öğrencinin puanı tahmini taban puanın oldukça altındadır. |

Tercih listesi dengeli hazırlanır. Önce uygun tercihler, sonra sınırda tercihler, daha sonra öğrencinin biraz daha çalışarak yaklaşabileceği tercihler listelenir.

---

### 3. 2026 Taban Puan Tahmini

2021-2025 yıllarına ait DGS yerleştirme verileri kullanılarak program bazlı 2026 taban puan tahmini yapılmıştır.

Kullanılan veriler ÖSYM yerleştirme sonuç PDF dosyalarından çıkarılmış, temizlenmiş ve modele uygun CSV formatına dönüştürülmüştür.

---

### 4. Matematik Soru Dağılımı Tahmini

Geçmiş yıllardaki DGS Matematik konu dağılımı verileri kullanılarak 2026 yılı için konu bazlı tahmini soru sayısı üretilmiştir.

Bu modül, sınava hazırlanan öğrencinin hangi konulara daha fazla dikkat etmesi gerektiği konusunda fikir vermeyi amaçlar.

---

### 5. Deneysel NLP Soru Analizi

Kullanıcı bir matematik sorusu yazdığında sistem, TF-IDF ve LinearSVC tabanlı NLP modeliyle sorunun hangi konuya yakın olduğunu tahmin eder ve çalışma tavsiyesi verir.

Bu modül deneysel amaçlıdır ve öğrencinin eksik olduğu konuyu anlamasına yardımcı olmak için geliştirilmiştir.

---

## 🛠️ Kullanılan Teknolojiler

### Frontend

- React.js
- Vite
- Tailwind CSS
- Recharts

### Backend

- Python
- FastAPI
- Uvicorn

### Veri İşleme ve Modelleme

- Pandas
- Scikit-learn
- pdfplumber
- joblib
- numpy
- Linear Regression
- Trend Analizi
- TF-IDF
- LinearSVC

---

## 📁 Proje Klasör Yapısı

```text
DGS-KOCU-PROJESI/
├── backend/
│   ├── models/
│   ├── main.py
│   └── model.py
│
├── data/
│   ├── pdfler/
│   ├── dgs_2026_taban_kontenjan_tahminleri.csv
│   ├── dgs_yerlestirme_ham.csv
│   ├── dgs_yerlestirme_temiz.csv
│   ├── dgs_matematik_orijinal_tablo.csv
│   ├── dgs_matematik_temiz.csv
│   ├── dgs_soru_nlp.csv
│   ├── dgs_soru_nlp_temiz.csv
│   ├── model_sonuclari.csv
│   ├── nlp_model_sonuclari.txt
│   └── taban_puan_model_sonuclari.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── index.html
│
├── notebooks/
│   ├── 03_model_egitimi.py
│   ├── 04_nlp_model_egitimi.py
│   ├── 08_yerlestirme_pdf_cek.py
│   ├── 09_yerlestirme_verisi_temizle.py
│   ├── 10_taban_puan_model_egitimi.py
│   ├── veri_cek.py
│   └── veri_duzenle.py
│
├── README.md

```

---

## 📌 Önemli Dosyalar

### Backend

| Dosya | Açıklama |
|---|---|
| `backend/main.py` | FastAPI uygulamasının ana dosyasıdır. API endpointleri burada tanımlanır. |
| `backend/model.py` | Veri okuma, model çağırma, tahmin üretme, soru analizi ve tercih önerisi fonksiyonlarını içerir. |
| `backend/models/` | Eğitilmiş model dosyalarının bulunduğu klasördür. |

### Frontend

| Dosya | Açıklama |
|---|---|
| `frontend/src/App.jsx` | React arayüzünün ana dosyasıdır. |
| `frontend/src/main.jsx` | React uygulamasının başlangıç dosyasıdır. |
| `frontend/src/index.css` | Genel stil dosyasıdır. |

### Veri Dosyaları

| Dosya | Açıklama |
|---|---|
| `data/pdfler/` | 2021-2025 yıllarına ait DGS yerleştirme sonuç PDF dosyalarıdır. |
| `data/dgs_yerlestirme_ham.csv` | PDF dosyalarından çıkarılan ham yerleştirme verisidir. |
| `data/dgs_yerlestirme_temiz.csv` | Ham verinin temizlenmiş halidir. |
| `data/dgs_2026_taban_kontenjan_tahminleri.csv` | 2026 tahmini taban puan ve kontenjan sonuçlarını içerir. |
| `data/dgs_matematik_temiz.csv` | Matematik konu dağılımı modelinde kullanılan temiz veri setidir. |
| `data/dgs_soru_nlp_temiz.csv` | NLP modeli için kullanılan temiz veri setidir. |
| `data/model_sonuclari.csv` | Matematik tahmin modelinin sonuçlarını içerir. |
| `data/nlp_model_sonuclari.txt` | NLP modelinin eğitim sonuçlarını içerir. |
| `data/taban_puan_model_sonuclari.txt` | Taban puan tahmin modelinin sonuçlarını içerir. |

---

## 📊 Veri Ön İşleme Süreci

Projede veri ön işleme aşaması önemli bir yer tutmaktadır.

Uygulanan işlemler:

- PDF dosyalarından tablo verilerinin çıkarılması
- Boş ve eksik değerlerin temizlenmesi
- Sayısal alanların uygun formata dönüştürülmesi
- Program adı, üniversite adı ve puan türü alanlarının düzenlenmesi
- Taban puan, tavan puan ve kontenjan verilerinin ayrıştırılması
- Modelleme için temiz CSV dosyalarının oluşturulması
- NLP veri setinde soru metni ve konu etiketlerinin düzenlenmesi

---

## 🤖 Modelleme Süreci

### 1. Taban Puan Tahmin Modeli

2021-2025 yıllarına ait yerleştirme verileri kullanılarak 2026 yılı için program bazlı tahmini taban puanlar oluşturulmuştur.

Her program için yıllara göre taban puan değişimi analiz edilmiştir. Bu değişimden hareketle 2026 yılı için tahmini değer üretilmiştir.

Model çıktısı:

```text
data/dgs_2026_taban_kontenjan_tahminleri.csv
```

---

### 2. Tercih Uygunluk Analizi

Öğrencinin tahmini puanı ile 2026 tahmini taban puanı karşılaştırılır.

Hesaplama mantığı:

```text
Öğrenci Puanı - Tahmini Taban Puan = Puan Farkı
```

Puan farkına göre tercih durumu belirlenir.

---

### 3. Matematik Soru Dağılımı Tahmini

DGS Matematik konu dağılımı verileri kullanılarak 2026 yılı için konu bazlı tahmini soru sayıları üretilmiştir.

Bu modül, sınav stratejisi oluşturmak için ek analiz olarak geliştirilmiştir.

---

### 4. NLP Soru Analiz Modeli

Soru metinleri TF-IDF yöntemiyle sayısallaştırılmıştır. Ardından LinearSVC modeli ile konu sınıflandırması yapılmıştır.

Bu modül, öğrencinin yanlış yaptığı veya çözmekte zorlandığı sorunun hangi konuya ait olduğunu tahmin etmeyi amaçlar.

---

## ▶️ Uygulama Nasıl Çalıştırılır?

### 1. Backend Kurulumu

Terminalde proje klasöründen backend klasörüne girilir:

```bash
cd backend
```

Gerekli Python kütüphaneleri kurulur:

```bash
pip install -r requirements.txt
```

Backend başlatılır:

```bash
uvicorn main:app --reload
```

Backend varsayılan olarak şu adreste çalışır:

```text
http://127.0.0.1:8000
```

---

### 2. Frontend Kurulumu

Yeni terminal açılır ve frontend klasörüne girilir:

```bash
cd frontend
```

Node paketleri kurulur:

```bash
npm install
```

Frontend başlatılır:

```bash
npm run dev
```

Frontend varsayılan olarak şu adreste çalışır:

```text
http://localhost:5173
```

---

## 🔗 API Endpointleri

| Endpoint | Açıklama |
|---|---|
| `GET /konular` | Matematik konu listesini getirir. |
| `GET /tahmin/{konu}` | Seçilen konu için 2026 tahmini soru sayısını döndürür. |
| `GET /gecmis/{konu}` | Seçilen konunun geçmiş yıllardaki verilerini getirir. |
| `POST /soru-analiz` | Girilen soru metninin konusunu tahmin eder. |
| `GET /programlar` | Program/bölüm listesini getirir. |
| `GET /program-ara/{aranan}` | Girilen metne göre program araması yapar. |
| `GET /tercih-oneri?puan=310&program=Bilgisayar%20Mühendisliği` | Öğrenci puanına göre tercih önerisi üretir. |

---

## 🧪 Kullanım Senaryosu

1. Kullanıcı **DGS Puan Hesaplama** sekmesine girer.
2. Matematik ve Türkçe doğru/yanlış sayılarını yazar.
3. 4’lük diploma notunu girer.
4. Sistem tahmini DGS puanını hesaplar.
5. Hesaplanan puan otomatik olarak **Tercih Analizi** sekmesine aktarılır.
6. Kullanıcı hedef bölümünü yazar.
7. Sistem geçmiş yerleştirme verilerine göre 2026 tahmini taban puanları listeler.
8. Kullanıcıya uygun, sınırda ve zorlayıcı tercihler gösterilir.

---

## 🖥️ Web Arayüzü Modülleri

| Sekme | Açıklama |
|---|---|
| **Puan Hesaplama** | Kullanıcı doğru, yanlış ve diploma notu bilgilerini girer. Sistem tahmini puanı hesaplar. |
| **Tercih Analizi** | Kullanıcı hedef bölümünü yazar. Sistem puanına uygun tercihleri listeler. |
| **Soru Dağılımı** | Geçmiş yıllardaki DGS Matematik konu dağılımı verilerine göre 2026 tahmini soru sayısı gösterilir. |
| **Soru Analizi** | Kullanıcı soru metni yazar. Sistem sorunun hangi konuya yakın olduğunu tahmin eder. |
| **Hakkında** | Projenin amacı ve kullanım alanı açıklanır. |

---

## ✅ Proje Sonuçları

Bu proje sonucunda:

- Çalışan bir full-stack web uygulaması geliştirilmiştir.
- Gerçek ÖSYM yerleştirme verileri işlenmiştir.
- 2026 yılı için tahmini taban puan analizi yapılmıştır.
- Öğrenci puanına göre tercih uygunluk sistemi kurulmuştur.
- Matematik konu dağılımı tahmin modeli geliştirilmiştir.
- NLP tabanlı soru analiz modülü eklenmiştir.
- Kullanıcı dostu ve sekmeli bir web arayüzü hazırlanmıştır.


---

## ⚠️ Önemli Not

Bu sistemde verilen puan, taban puan ve tercih yorumları tahmini analiz amaçlıdır. Resmî ÖSYM sonuçlarının yerine geçmez.

Tercih sürecinde resmî kılavuzlar ve uzman görüşleri dikkate alınmalıdır.

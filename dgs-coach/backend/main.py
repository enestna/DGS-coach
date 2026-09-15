from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import (
    tahmin_yap,
    konulari_getir,
    gecmis_veri_getir,
    tum_konular_son_yil_verisi,
    model_metrikleri_getir,
    tum_model_sonuclari_getir,
    soru_analiz_et,
    programlari_getir,
    program_ara,
    tercih_onerisi_getir
)
app = FastAPI(
    title="DGS Koçu API",
    description="DGS Matematik konu dağılımı tahmin sistemi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "DGS Koçu API Çalışıyor",
        "proje": "DGS Matematik Soru Tahmin Sistemi",
        "model": "Linear Regression",
        "durum": "Eğitilmiş modeller aktif"
    }


@app.get("/konular")
def konular():
    return {
        "konular": konulari_getir()
    }


@app.get("/gecmis/{konu}")
def gecmis(konu: str):
    veri = gecmis_veri_getir(konu)

    if veri is None:
        return {
            "hata": "Bu konu veri setinde bulunamadı."
        }

    return {
        "konu": konu,
        "veri": veri
    }


@app.get("/karsilastirma")
def karsilastirma():
    return {
        "veri": tum_konular_son_yil_verisi()
    }


@app.get("/model-sonuclari")
def model_sonuclari():
    return {
        "veri": tum_model_sonuclari_getir()
    }


@app.get("/tahmin/{konu}")
def tahmin(konu: str):
    sonuc = tahmin_yap(konu)
    metrikler = model_metrikleri_getir(konu)

    if sonuc is None:
        return {
            "hata": "Bu konu için eğitilmiş model bulunamadı."
        }

    return {
        "ders": "Matematik",
        "konu": konu,
        "tahmini_soru": sonuc,
        "model": "Linear Regression",
        "tahmin_yili": 2026,
        "metrikler": metrikler
    }

@app.post("/soru-analiz")
def soru_analiz(data: dict):
    soru = data.get("soru", "")

    if not soru.strip():
        return {
            "hata": "Lütfen analiz edilecek soru metnini giriniz."
        }

    sonuc = soru_analiz_et(soru)

    if sonuc is None:
        return {
            "hata": "NLP modeli bulunamadı. Önce NLP modelini eğitmelisiniz."
        }

    return {
        "soru": soru,
        "tespit_edilen_konu": sonuc["konu"],
        "eksik": sonuc["eksik"],
        "tavsiye": sonuc["tavsiye"]
    }

@app.get("/programlar")
def programlar():
    return {
        "programlar": programlari_getir()
    }


@app.get("/program-ara/{aranan}")
def program_arama(aranan: str):
    return {
        "aranan": aranan,
        "sonuclar": program_ara(aranan)
    }


@app.get("/tercih-oneri")
def tercih_oneri(puan: float, program: str):
    oneriler = tercih_onerisi_getir(puan, program)

    if not oneriler:
        return {
            "hata": "Aranan programa uygun sonuç bulunamadı."
        }

    return {
        "ogrenci_puani": puan,
        "aranan_program": program,
        "oneriler": oneriler
    }
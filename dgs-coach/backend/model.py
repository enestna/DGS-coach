import os
import re
import joblib
import pandas as pd


DATA_PATH = "../data/dgs_matematik_temiz.csv"
METRICS_PATH = "../data/model_sonuclari.csv"
MODEL_DIR = "models"
TAHMIN_YILI = 2026

TERCIH_TAHMIN_PATH = "../data/dgs_2026_taban_kontenjan_tahminleri.csv"


# ---------------------------------------------------------
# GENEL YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------

def dosya_adi_temizle(text):
    text = str(text).lower()
    text = text.replace("ı", "i").replace("ğ", "g").replace("ü", "u")
    text = text.replace("ş", "s").replace("ö", "o").replace("ç", "c")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text


def metin_normalize(text):
    text = str(text).lower()
    text = text.replace("ı", "i")
    text = text.replace("ğ", "g")
    text = text.replace("ü", "u")
    text = text.replace("ş", "s")
    text = text.replace("ö", "o")
    text = text.replace("ç", "c")
    return text


def guvenli_float(value, default=0):
    try:
        value = float(value)

        if pd.isna(value):
            return default

        if value == float("inf") or value == float("-inf"):
            return default

        return value
    except:
        return default


def guvenli_int(value, default=0):
    try:
        value = float(value)

        if pd.isna(value):
            return default

        if value == float("inf") or value == float("-inf"):
            return default

        return int(round(value))
    except:
        return default


def guvenli_str(value):
    if pd.isna(value):
        return ""
    return str(value)


# ---------------------------------------------------------
# DGS MATEMATİK KONU TAHMİN MODÜLÜ
# ---------------------------------------------------------

def veri_oku():
    df = pd.read_csv(DATA_PATH)

    df["yil"] = df["yil"].astype(int)
    df["soru_sayisi"] = pd.to_numeric(
        df["soru_sayisi"],
        errors="coerce"
    ).fillna(0)

    df = df[df["konu"] != "TOPLAM"]

    return df


def model_sonuclari_oku():
    df = pd.read_csv(METRICS_PATH)

    df = df[df["konu"] != "TOPLAM"]

    return df


def konulari_getir():
    df = veri_oku()

    konular = sorted(
        df["konu"]
        .dropna()
        .unique()
        .tolist()
    )

    return konular


def gecmis_veri_getir(konu):
    df = veri_oku()

    konu_df = df[df["konu"] == konu].sort_values("yil")

    if konu_df.empty:
        return None

    return [
        {
            "yil": int(row["yil"]),
            "soru": int(row["soru_sayisi"])
        }
        for _, row in konu_df.iterrows()
    ]


def tum_konular_son_yil_verisi():
    df = veri_oku()

    son_yil = int(df["yil"].max())
    son_yil_df = df[df["yil"] == son_yil]

    return [
        {
            "konu": row["konu"],
            "soru": int(row["soru_sayisi"])
        }
        for _, row in son_yil_df.iterrows()
    ]


def model_dosyasi_bul(konu):
    model_file_name = dosya_adi_temizle(konu) + ".pkl"
    model_path = os.path.join(MODEL_DIR, model_file_name)

    if not os.path.exists(model_path):
        return None

    return model_path


def tahmin_yap(konu):
    model_path = model_dosyasi_bul(konu)

    if model_path is None:
        return None

    model = joblib.load(model_path)

    tahmin = model.predict([[TAHMIN_YILI]])

    tahmin_sayisi = int(round(float(tahmin[0])))

    if tahmin_sayisi < 0:
        tahmin_sayisi = 0

    return tahmin_sayisi


def model_metrikleri_getir(konu):
    df = model_sonuclari_oku()

    konu_df = df[df["konu"] == konu]

    if konu_df.empty:
        return None

    row = konu_df.iloc[0]

    return {
        "konu": row["konu"],
        "veri_sayisi": int(row["veri_sayisi"]),
        "mae": float(row["mae"]),
        "mse": float(row["mse"]),
        "r2": float(row["r2"]),
        "model_dosyasi": row["model_dosyasi"]
    }


def tum_model_sonuclari_getir():
    df = model_sonuclari_oku()

    return df.to_dict(orient="records")


# ---------------------------------------------------------
# NLP SORU ANALİZ MODÜLÜ
# ---------------------------------------------------------

def soru_analiz_et(soru_metni):
    model_path = "models/nlp_konu_model.pkl"
    tavsiye_path = "models/nlp_tavsiye_haritasi.pkl"

    if not os.path.exists(model_path):
        return None

    if not os.path.exists(tavsiye_path):
        return None

    model = joblib.load(model_path)
    tavsiye_haritasi = joblib.load(tavsiye_path)

    tahmin_konu = model.predict([soru_metni])[0]

    tavsiye = tavsiye_haritasi.get(
        tahmin_konu,
        "Bu konu için çalışma tavsiyesi bulunamadı."
    )

    return {
        "konu": tahmin_konu,
        "tespit_edilen_konu": tahmin_konu,
        "eksik": f"{tahmin_konu} konusunda eksiğin olabilir.",
        "tavsiye": tavsiye
    }


# ---------------------------------------------------------
# DGS TERCİH / TABAN PUAN ANALİZ MODÜLÜ
# ---------------------------------------------------------

def tercih_verisi_oku():
    df = pd.read_csv(TERCIH_TAHMIN_PATH)

    metin_kolonlari = [
        "program_kodu",
        "universite",
        "fakulte",
        "program_adi",
        "program_adi_tam",
        "puan_turu"
    ]

    for col in metin_kolonlari:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    sayisal_kolonlari = [
        "son_yil",
        "son_yil_taban_puan",
        "son_yil_tavan_puan",
        "son_yil_kontenjan",
        "tahmini_taban_puan_2026",
        "tahmini_kontenjan_2026",
        "veri_yili_sayisi"
    ]

    for col in sayisal_kolonlari:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    df = df.replace([float("inf"), float("-inf")], 0)
    df = df.fillna("")

    return df


def programlari_getir():
    df = tercih_verisi_oku()

    programlar = (
        df["program_adi"]
        .dropna()
        .unique()
        .tolist()
    )

    programlar = sorted(programlar)

    return programlar


def program_ara(aranan):
    df = tercih_verisi_oku()

    aranan_normal = metin_normalize(aranan)

    df["arama_metni"] = (
        df["universite"].astype(str) + " " +
        df["program_adi"].astype(str) + " " +
        df["puan_turu"].astype(str)
    ).apply(metin_normalize)

    sonuc_df = df[df["arama_metni"].str.contains(aranan_normal, na=False)]

    sonuc_df = sonuc_df.sort_values(
        by="tahmini_taban_puan_2026",
        ascending=False
    )

    sonuc_df = sonuc_df.head(50)

    sonuc_df = sonuc_df.replace([float("inf"), float("-inf")], 0)
    sonuc_df = sonuc_df.fillna("")

    return sonuc_df.to_dict(orient="records")


def tercih_durumu_hesapla(ogrenci_puani, tahmini_taban_puan):
    fark = ogrenci_puani - tahmini_taban_puan

    if fark >= 5:
        return (
            "Uygun",
            round(fark, 2),
            "Puanın tahmini taban puanın üzerinde. Bu tercih senin için uygun görünüyor."
        )

    if -5 <= fark < 5:
        return (
            "Sınırda",
            round(fark, 2),
            "Puanın tahmini taban puana çok yakın. Bu tercih sınırda görünüyor; listende bulunabilir ama yanında daha güvenli tercihler de olmalı."
        )

    if -20 <= fark < -5:
        return (
            "Biraz Daha Zorla",
            round(fark, 2),
            "Bu tercih şu an biraz zor görünüyor ama imkânsız değil. Netlerini birkaç puan artırırsan bu bölüme yaklaşabilirsin."
        )

    return (
        "Zor",
        round(fark, 2),
        "Bu tercih şu an puanına göre zor görünüyor. Yine de hedef olarak tutabilir, daha uygun alternatiflerle tercih listeni güçlendirebilirsin."
    )


def tercih_onerisi_getir(ogrenci_puani, aranan_program):
    df = tercih_verisi_oku()

    aranan_normal = metin_normalize(aranan_program)

    df["arama_metni"] = (
        df["universite"].astype(str) + " " +
        df["program_adi"].astype(str) + " " +
        df["puan_turu"].astype(str)
    ).apply(metin_normalize)

    sonuc_df = df[df["arama_metni"].str.contains(aranan_normal, na=False)]

    if sonuc_df.empty:
        return []

    oneriler = []

    for _, row in sonuc_df.iterrows():
        tahmini_taban = guvenli_float(
            row.get("tahmini_taban_puan_2026", 0)
        )

        son_yil_taban = guvenli_float(
            row.get("son_yil_taban_puan", 0)
        )

        son_yil_tavan = guvenli_float(
            row.get("son_yil_tavan_puan", 0)
        )

        son_yil_kontenjan = guvenli_int(
            row.get("son_yil_kontenjan", 0)
        )

        tahmini_kontenjan = guvenli_int(
            row.get("tahmini_kontenjan_2026", 0)
        )

        veri_yili_sayisi = guvenli_int(
            row.get("veri_yili_sayisi", 0)
        )

        son_yil = guvenli_int(
            row.get("son_yil", 0)
        )

        durum, fark, yorum = tercih_durumu_hesapla(
            float(ogrenci_puani),
            tahmini_taban
        )

        oneriler.append({
            "program_kodu": guvenli_str(row.get("program_kodu", "")),
            "universite": guvenli_str(row.get("universite", "")),
            "fakulte": guvenli_str(row.get("fakulte", "")),
            "program_adi": guvenli_str(row.get("program_adi", "")),
            "puan_turu": guvenli_str(row.get("puan_turu", "")),
            "son_yil": son_yil,
            "son_yil_taban_puan": round(son_yil_taban, 3),
            "son_yil_tavan_puan": round(son_yil_tavan, 3),
            "son_yil_kontenjan": son_yil_kontenjan,
            "tahmini_taban_puan_2026": round(tahmini_taban, 3),
            "tahmini_kontenjan_2026": tahmini_kontenjan,
            "ogrenci_puani": round(float(ogrenci_puani), 2),
            "puan_farki": fark,
            "durum": durum,
            "yorum": yorum,
            "veri_yili_sayisi": veri_yili_sayisi
        })

    uygunlar = [
        item for item in oneriler
        if item["durum"] == "Uygun"
    ]

    sinirdakiler = [
        item for item in oneriler
        if item["durum"] == "Sınırda"
    ]

    biraz_zorla = [
        item for item in oneriler
        if item["durum"] == "Biraz Daha Zorla"
    ]

    zorlar = [
        item for item in oneriler
        if item["durum"] == "Zor"
    ]

    # Uygunlarda puana yakın olanları önce getiriyoruz.
    uygunlar = sorted(
        uygunlar,
        key=lambda x: abs(x["puan_farki"])
    )

    # Sınırda olanlarda da en yakın olanları önce getiriyoruz.
    sinirdakiler = sorted(
        sinirdakiler,
        key=lambda x: abs(x["puan_farki"])
    )

    # Biraz daha zorla grubunda da öğrenciye en yakın hedefleri önce getiriyoruz.
    biraz_zorla = sorted(
        biraz_zorla,
        key=lambda x: abs(x["puan_farki"])
    )

    zorlar = sorted(
        zorlar,
        key=lambda x: abs(x["puan_farki"])
    )

    # Dengeli tercih listesi:
    # Önce birkaç uygun, sonra birkaç sınırda, sonra biraz daha zorla grubu.
    dengeli_liste = []

    dengeli_liste.extend(uygunlar[:20])
    dengeli_liste.extend(sinirdakiler[:15])
    dengeli_liste.extend(biraz_zorla[:15])

    # Eğer 50 sonuç dolmadıysa en yakın zor tercihlerle tamamlıyoruz.
    kalan_hak = 50 - len(dengeli_liste)

    if kalan_hak > 0:
        dengeli_liste.extend(zorlar[:kalan_hak])

    return dengeli_liste[:50]
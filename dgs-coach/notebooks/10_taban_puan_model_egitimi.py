import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DATA_PATH = "../data/dgs_yerlestirme_temiz.csv"
OUTPUT_PATH = "../data/dgs_2026_taban_kontenjan_tahminleri.csv"
RESULT_PATH = "../data/taban_puan_model_sonuclari.txt"


def trend_tahmin(yillar, degerler, tahmin_yili=2026):
    """
    Basit lineer trend tahmini yapar.
    Veri azsa son değeri döndürür.
    """
    yillar = np.array(yillar, dtype=float)
    degerler = np.array(degerler, dtype=float)

    if len(yillar) < 3:
        return float(degerler[-1])

    # y = ax + b
    a, b = np.polyfit(yillar, degerler, 1)
    return float(a * tahmin_yili + b)


def guvenli_taban_puan(tahmin, son_deger):
    """
    Aşırı uç tahminleri engeller.
    Taban puan gerçekçi aralıkta tutulur.
    """
    if pd.isna(tahmin):
        return round(float(son_deger), 3)

    # DGS puanları için güvenli aralık
    tahmin = max(100, min(500, tahmin))

    return round(float(tahmin), 3)


def guvenli_kontenjan(tahmin, son_deger):
    """
    Kontenjan negatif olamaz.
    Tam sayıya yuvarlanır.
    """
    if pd.isna(tahmin):
        return int(round(float(son_deger)))

    tahmin = max(0, tahmin)

    return int(round(float(tahmin)))


df = pd.read_csv(DATA_PATH)

print("Veri boyutu:", df.shape)

df["yil"] = pd.to_numeric(df["yil"], errors="coerce")
df["kontenjan"] = pd.to_numeric(df["kontenjan"], errors="coerce").fillna(0)
df["en_kucuk_puan"] = pd.to_numeric(df["en_kucuk_puan"], errors="coerce")
df["en_buyuk_puan"] = pd.to_numeric(df["en_buyuk_puan"], errors="coerce")

df = df.dropna(subset=["yil", "program_kodu", "en_kucuk_puan"])

df["program_kodu"] = df["program_kodu"].astype(str)
df["universite"] = df["universite"].astype(str)
df["fakulte"] = df["fakulte"].astype(str)
df["program_adi"] = df["program_adi"].astype(str)
df["program_adi_tam"] = df["program_adi_tam"].astype(str)
df["puan_turu"] = df["puan_turu"].astype(str)

sonuclar = []

taban_test_gercek = []
taban_test_tahmin = []

kont_test_gercek = []
kont_test_tahmin = []

gruplar = df.groupby("program_kodu")

print("Program grubu sayısı:", len(gruplar))
print("Tahminler hesaplanıyor...")

for program_kodu, grup in gruplar:
    grup = grup.sort_values("yil")

    grup_yil = (
        grup.groupby("yil")
        .agg({
            "universite": "last",
            "fakulte": "last",
            "program_adi": "last",
            "program_adi_tam": "last",
            "puan_turu": "last",
            "kontenjan": "mean",
            "en_kucuk_puan": "mean",
            "en_buyuk_puan": "mean"
        })
        .reset_index()
        .sort_values("yil")
    )

    if len(grup_yil) == 0:
        continue

    son_satir = grup_yil.iloc[-1]

    yillar = grup_yil["yil"].tolist()
    tabanlar = grup_yil["en_kucuk_puan"].tolist()
    kontenjanlar = grup_yil["kontenjan"].tolist()

    tahmini_taban = trend_tahmin(yillar, tabanlar, 2026)
    tahmini_kontenjan = trend_tahmin(yillar, kontenjanlar, 2026)

    tahmini_taban = guvenli_taban_puan(
        tahmini_taban,
        son_satir["en_kucuk_puan"]
    )

    tahmini_kontenjan = guvenli_kontenjan(
        tahmini_kontenjan,
        son_satir["kontenjan"]
    )

    # Test metriği: En az 4 yıl verisi varsa son yılı tahmin et
    if len(grup_yil) >= 4:
        train = grup_yil.iloc[:-1]
        test = grup_yil.iloc[-1]

        test_yillar = train["yil"].tolist()

        taban_pred = trend_tahmin(
            test_yillar,
            train["en_kucuk_puan"].tolist(),
            int(test["yil"])
        )

        kont_pred = trend_tahmin(
            test_yillar,
            train["kontenjan"].tolist(),
            int(test["yil"])
        )

        taban_test_gercek.append(float(test["en_kucuk_puan"]))
        taban_test_tahmin.append(float(taban_pred))

        kont_test_gercek.append(float(test["kontenjan"]))
        kont_test_tahmin.append(float(kont_pred))

    sonuclar.append({
        "program_kodu": program_kodu,
        "universite": son_satir["universite"],
        "fakulte": son_satir["fakulte"],
        "program_adi": son_satir["program_adi"],
        "program_adi_tam": son_satir["program_adi_tam"],
        "puan_turu": son_satir["puan_turu"],
        "son_yil": int(son_satir["yil"]),
        "son_yil_taban_puan": round(float(son_satir["en_kucuk_puan"]), 3),
        "son_yil_tavan_puan": round(float(son_satir["en_buyuk_puan"]), 3),
        "son_yil_kontenjan": int(round(float(son_satir["kontenjan"]))),
        "tahmini_taban_puan_2026": tahmini_taban,
        "tahmini_kontenjan_2026": tahmini_kontenjan,
        "veri_yili_sayisi": len(grup_yil)
    })


sonuc_df = pd.DataFrame(sonuclar)

sonuc_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\n2026 tahmin dosyası oluşturuldu:", OUTPUT_PATH)
print("Tahmin yapılan program sayısı:", len(sonuc_df))

print("\nİlk 20 tahmin:")
print(sonuc_df.head(20))


def metrik_hesapla(y_true, y_pred):
    if len(y_true) == 0:
        return 0, 0, 0

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)

    try:
        r2 = r2_score(y_true, y_pred)
    except:
        r2 = 0

    return mae, mse, r2


taban_mae, taban_mse, taban_r2 = metrik_hesapla(
    taban_test_gercek,
    taban_test_tahmin
)

kont_mae, kont_mse, kont_r2 = metrik_hesapla(
    kont_test_gercek,
    kont_test_tahmin
)

print("\nTaban Puan Trend Modeli")
print("MAE:", round(taban_mae, 3))
print("MSE:", round(taban_mse, 3))
print("R2:", round(taban_r2, 3))

print("\nKontenjan Trend Modeli")
print("MAE:", round(kont_mae, 3))
print("MSE:", round(kont_mse, 3))
print("R2:", round(kont_r2, 3))


with open(RESULT_PATH, "w", encoding="utf-8") as f:
    f.write("DGS 2026 Taban Puan ve Kontenjan Tahmin Modeli\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Toplam temiz veri sayısı: {len(df)}\n")
    f.write(f"Tahmin yapılan program sayısı: {len(sonuc_df)}\n\n")

    f.write("Model yöntemi:\n")
    f.write("Her program kodu için yıllara göre lineer trend analizi yapılmıştır.\n")
    f.write("En az 3 yıllık verisi olan programlarda 2026 tahmini trend ile hesaplanmıştır.\n")
    f.write("Verisi az olan programlarda son yıl değeri referans alınmıştır.\n")
    f.write("Bu yöntemde veri sızıntısı yoktur.\n\n")

    f.write("Taban Puan Trend Modeli Sonuçları\n")
    f.write("-" * 40 + "\n")
    f.write(f"MAE: {round(taban_mae, 3)}\n")
    f.write(f"MSE: {round(taban_mse, 3)}\n")
    f.write(f"R2: {round(taban_r2, 3)}\n\n")

    f.write("Kontenjan Trend Modeli Sonuçları\n")
    f.write("-" * 40 + "\n")
    f.write(f"MAE: {round(kont_mae, 3)}\n")
    f.write(f"MSE: {round(kont_mse, 3)}\n")
    f.write(f"R2: {round(kont_r2, 3)}\n\n")

    f.write("Çıktı dosyası:\n")
    f.write(OUTPUT_PATH)

print("\nModel sonuçları kaydedildi:", RESULT_PATH)
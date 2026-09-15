import os
import re
import joblib
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DATA_PATH = "../data/dgs_matematik_temiz.csv"
MODEL_DIR = "../backend/models"
METRICS_PATH = "../data/model_sonuclari.csv"


def dosya_adi_temizle(text):
    text = text.lower()
    text = text.replace("ı", "i").replace("ğ", "g").replace("ü", "u")
    text = text.replace("ş", "s").replace("ö", "o").replace("ç", "c")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text


os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

df["yil"] = df["yil"].astype(int)
df["soru_sayisi"] = pd.to_numeric(df["soru_sayisi"], errors="coerce").fillna(0)

sonuclar = []

konular = sorted(df["konu"].unique())

print("Eğitilecek konu sayısı:", len(konular))
print("-" * 50)

for konu in konular:
    konu_df = df[df["konu"] == konu].sort_values("yil")

    X = konu_df[["yil"]]
    y = konu_df["soru_sayisi"]

    if len(konu_df) < 4:
        print(f"{konu} için yeterli veri yok, atlandı.")
        continue

    # Son 2 yılı test, önceki yılları eğitim yapıyoruz
    X_train = X.iloc[:-2]
    y_train = y.iloc[:-2]

    X_test = X.iloc[-2:]
    y_test = y.iloc[-2:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    try:
        r2 = r2_score(y_test, y_pred)
    except:
        r2 = 0

    # Final model: tüm veriyle tekrar eğitilir
    final_model = LinearRegression()
    final_model.fit(X, y)

    model_file_name = dosya_adi_temizle(konu) + ".pkl"
    model_path = os.path.join(MODEL_DIR, model_file_name)

    joblib.dump(final_model, model_path)

    tahmin_2026 = final_model.predict([[2026]])
    tahmin_2026 = int(round(float(tahmin_2026[0])))

    if tahmin_2026 < 0:
        tahmin_2026 = 0

    sonuclar.append({
        "konu": konu,
        "veri_sayisi": len(konu_df),
        "mae": round(mae, 3),
        "mse": round(mse, 3),
        "r2": round(r2, 3),
        "tahmin_2026": tahmin_2026,
        "model_dosyasi": model_file_name
    })

    print(f"{konu} modeli eğitildi.")
    print(f"MAE: {round(mae, 3)} | MSE: {round(mse, 3)} | R2: {round(r2, 3)}")
    print(f"2026 Tahmini: {tahmin_2026}")
    print("-" * 50)


sonuc_df = pd.DataFrame(sonuclar)

sonuc_df.to_csv(METRICS_PATH, index=False, encoding="utf-8-sig")

print("\nTüm modeller eğitildi.")
print("Model sonuçları kaydedildi:", METRICS_PATH)
print("Model dosyaları kaydedildi:", MODEL_DIR)
import pandas as pd

# CSV oku
df = pd.read_csv("../data/dgs_matematik_orijinal_tablo.csv")

print("ORİJİNAL VERİ:")
print(df.head())

# Uzun formata çevir
df_long = df.melt(
    id_vars=["KONULAR"],
    var_name="yil",
    value_name="soru_sayisi"
)

# Kolon isimlerini düzenle
df_long.rename(columns={
    "KONULAR": "konu"
}, inplace=True)

# Tireleri temizle
df_long["soru_sayisi"] = df_long["soru_sayisi"].replace("–", 0)

# Sayısal tipe çevir
df_long["soru_sayisi"] = pd.to_numeric(
    df_long["soru_sayisi"]
)

# Yılı integer yap
df_long["yil"] = df_long["yil"].astype(int)

# İlk satırlar
print("\nDÜZENLENMİŞ VERİ:")
print(df_long.head(20))

# Yeni CSV kaydet
df_long.to_csv(
    "../data/dgs_matematik_temiz.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nYeni temiz veri seti oluşturuldu.")
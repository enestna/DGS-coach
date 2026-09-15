import pandas as pd

url = "https://www.unirehberi.com/dgs-matematik-konulari/"

# Sayfadaki tabloları oku
tablolar = pd.read_html(url)

print("Bulunan tablo sayısı:", len(tablolar))

# İlk tabloyu al
df = tablolar[0]

print(df.head())

# CSV olarak kaydet
df.to_csv("../data/dgs_matematik_orijinal_tablo.csv", index=False, encoding="utf-8-sig")

print("CSV başarıyla kaydedildi.")
import re
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


DATA_PATH = "../data/dgs_soru_nlp.csv"
CLEAN_DATA_PATH = "../data/dgs_soru_nlp_temiz.csv"
MODEL_PATH = "../backend/models/nlp_konu_model.pkl"
TAVSIYE_PATH = "../backend/models/nlp_tavsiye_haritasi.pkl"
RESULT_PATH = "../data/nlp_model_sonuclari.txt"


def metin_temizle(text):
    text = str(text).lower().strip()

    # Türkçe karakterleri normalize ediyoruz
    text = text.replace("ı", "i")
    text = text.replace("ğ", "g")
    text = text.replace("ü", "u")
    text = text.replace("ş", "s")
    text = text.replace("ö", "o")
    text = text.replace("ç", "c")

    # Matematiksel sembolleri anlamlı kelimelere yaklaştırıyoruz
    text = text.replace("≤", " kucuk esit ")
    text = text.replace("≥", " buyuk esit ")
    text = text.replace("<", " kucuktur ")
    text = text.replace(">", " buyuktur ")
    text = text.replace("=", " esittir ")
    text = text.replace("+", " arti ")
    text = text.replace("-", " eksi ")
    text = text.replace("*", " carpi ")
    text = text.replace(".", " carpi ")
    text = text.replace("÷", " bolu ")
    text = text.replace("/", " bolu ")

    # Parantezleri boşlukla ayırıyoruz
    text = text.replace("(", " ")
    text = text.replace(")", " ")

    # Geri kalan gereksiz karakterleri temizliyoruz
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Fazla boşlukları temizliyoruz
    text = re.sub(r"\s+", " ", text)

    return text.strip()


os.makedirs("../backend/models", exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("Orijinal veri boyutu:", df.shape)

df.columns = df.columns.str.strip()

# Yanlışlıkla araya giren ikinci başlık satırlarını temizler
df = df[df["soru"] != "soru"]

# Boş satırları siler
df = df.dropna(subset=["soru", "konu", "tavsiye"])

# Aynı soruları siler
df = df.drop_duplicates(subset=["soru"])

df["soru"] = df["soru"].astype(str).str.strip()
df["konu"] = df["konu"].astype(str).str.strip()
df["tavsiye"] = df["tavsiye"].astype(str).str.strip()

df["soru_temiz"] = df["soru"].apply(metin_temizle)

# Çok kısa veya anlamsız satırları siler
df = df[df["soru_temiz"].str.len() > 5]

print("Temiz veri boyutu:", df.shape)
print("Konu sayısı:", df["konu"].nunique())

print("\nKonu dağılımı:")
print(df["konu"].value_counts())

df[["soru", "soru_temiz", "konu", "tavsiye"]].to_csv(
    CLEAN_DATA_PATH,
    index=False,
    encoding="utf-8-sig"
)

X = df["soru_temiz"]
y = df["konu"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Güçlendirilmiş NLP modeli
# word tf-idf: anlamlı kelimeleri yakalar
# char tf-idf: 2x+5, 6-(-2), 3/4 gibi matematiksel kısa yapıları daha iyi yakalar
model = Pipeline([
    ("features", FeatureUnion([
        ("word_tfidf", TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 3),
            max_features=12000,
            min_df=1,
            sublinear_tf=True
        )),
        ("char_tfidf", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 6),
            max_features=12000,
            min_df=1,
            sublinear_tf=True
        ))
    ])),
    ("classifier", LinearSVC(
        C=1.8,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nNLP Model Accuracy:", round(accuracy, 4))

rapor = classification_report(
    y_test,
    y_pred,
    zero_division=0
)

print("\nClassification Report:")
print(rapor)

tavsiye_haritasi = (
    df.groupby("konu")["tavsiye"]
    .first()
    .to_dict()
)

joblib.dump(model, MODEL_PATH)
joblib.dump(tavsiye_haritasi, TAVSIYE_PATH)

with open(RESULT_PATH, "w", encoding="utf-8") as f:
    f.write("DGS Koçu NLP Model Sonuçları\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Toplam temiz veri sayısı: {len(df)}\n")
    f.write(f"Konu sayısı: {df['konu'].nunique()}\n")
    f.write(f"Accuracy: {round(accuracy, 4)}\n\n")
    f.write("Konu Dağılımı:\n")
    f.write(str(df["konu"].value_counts()))
    f.write("\n\nClassification Report:\n")
    f.write(rapor)

print("\nNLP modeli kaydedildi:", MODEL_PATH)
print("Tavsiye haritası kaydedildi:", TAVSIYE_PATH)
print("Temiz NLP veri seti kaydedildi:", CLEAN_DATA_PATH)
print("Model sonuçları kaydedildi:", RESULT_PATH)
import re
import pandas as pd


INPUT_PATH = "../data/dgs_yerlestirme_ham.csv"
OUTPUT_PATH = "../data/dgs_yerlestirme_temiz.csv"


def temizle(text):
    if pd.isna(text):
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def sayisal_kodu_temizle(text):
    text = temizle(text)

    if re.match(r"^\d+\.0$", text):
        text = text.replace(".0", "")

    return text


def tam_sayi_cevir(text):
    text = temizle(text)

    if text in ["", "--", "-", "nan", "NaN"]:
        return 0

    text = text.replace(".0", "")

    if text.isdigit():
        return int(text)

    return 0


def puan_cevir(text):
    text = temizle(text)

    if text in ["", "--", "-", "nan", "NaN"]:
        return None

    # Türkçe ondalık virgülünü noktaya çevir
    text = text.replace(",", ".")

    try:
        return float(text)
    except:
        return None


def program_parcala(program_adi):
    """
    Örnek gelen veri:
    ABDULLAH GÜL ÜNİVERSİTESİ (KAYSERİ) (Devlet Üniversitesi)/Mühendislik Fakültesi/Bilgisayar Mühendisliği (İngilizce)

    Çıkacak:
    universite
    fakulte
    program
    """
    program_adi = temizle(program_adi)

    parcalar = program_adi.split("/")

    universite = parcalar[0].strip() if len(parcalar) > 0 else ""
    fakulte = parcalar[1].strip() if len(parcalar) > 1 else ""
    program = parcalar[-1].strip() if len(parcalar) > 0 else program_adi

    return universite, fakulte, program


df = pd.read_csv(INPUT_PATH)

print("Ham veri boyutu:", df.shape)

df.columns = df.columns.str.strip()

for col in df.columns:
    df[col] = df[col].apply(temizle)

temiz_satirlar = []

for _, row in df.iterrows():
    yil = tam_sayi_cevir(row.get("yil", ""))
    program_kodu = sayisal_kodu_temizle(row.get("program_kodu", ""))
    program_adi_tam = temizle(row.get("program_adi", ""))
    puan_turu = temizle(row.get("puan_turu", "")).upper()
    kontenjan = tam_sayi_cevir(row.get("kontenjan", ""))
    yerlesen = tam_sayi_cevir(row.get("yerlesen", ""))
    bos_kontenjan = tam_sayi_cevir(row.get("bos_kontenjan", ""))
    en_kucuk_puan = puan_cevir(row.get("en_kucuk_puan", ""))
    en_buyuk_puan = puan_cevir(row.get("en_buyuk_puan", ""))

    if not program_kodu.isdigit():
        continue

    if puan_turu not in ["SAY", "EA", "SÖZ", "SOZ"]:
        continue

    if program_adi_tam == "":
        continue

    # Taban puanı olmayan programları model için kullanmayacağız
    # Ama istersen ayrı dosyada saklanabilir
    if en_kucuk_puan is None:
        continue

    universite, fakulte, program_adi = program_parcala(program_adi_tam)

    temiz_satirlar.append({
        "yil": yil,
        "program_kodu": program_kodu,
        "universite": universite,
        "fakulte": fakulte,
        "program_adi": program_adi,
        "program_adi_tam": program_adi_tam,
        "puan_turu": "SÖZ" if puan_turu == "SOZ" else puan_turu,
        "kontenjan": kontenjan,
        "yerlesen": yerlesen,
        "bos_kontenjan": bos_kontenjan,
        "en_kucuk_puan": en_kucuk_puan,
        "en_buyuk_puan": en_buyuk_puan
    })


temiz_df = pd.DataFrame(temiz_satirlar)

print("Temizlenmeden sonra satır:", temiz_df.shape)

temiz_df = temiz_df.drop_duplicates(
    subset=["yil", "program_kodu", "program_adi_tam"]
)

temiz_df = temiz_df[
    (temiz_df["yil"] > 0) &
    (temiz_df["program_adi"] != "") &
    (temiz_df["universite"] != "") &
    (temiz_df["en_kucuk_puan"].notna())
]

temiz_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("Temiz yerleştirme CSV oluşturuldu:", OUTPUT_PATH)
print("Temiz veri boyutu:", temiz_df.shape)

print("\nİlk 20 satır:")
print(temiz_df.head(20))

print("\nYıllara göre kayıt sayısı:")
print(temiz_df["yil"].value_counts().sort_index())

print("\nPuan türüne göre kayıt sayısı:")
print(temiz_df["puan_turu"].value_counts())

print("\nEn çok geçen ilk 20 program:")
print(temiz_df["program_adi"].value_counts().head(20))

print("\nPuan istatistikleri:")
print(temiz_df["en_kucuk_puan"].describe())
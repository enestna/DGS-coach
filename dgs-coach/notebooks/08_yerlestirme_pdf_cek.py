import os
import re
import pdfplumber
import pandas as pd


PDF_DIR = "../data/pdfler"
OUTPUT_PATH = "../data/dgs_yerlestirme_ham.csv"


pdf_dosyalari = {
    2021: "dgs_2021_yerlestirme.pdf",
    2022: "dgs_2022_yerlestirme.pdf",
    2023: "dgs_2023_yerlestirme.pdf",
    2024: "dgs_2024_yerlestirme.pdf",
    2025: "dgs_2025_yerlestirme.pdf",
}


def temizle(text):
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


tum_satirlar = []

for yil, dosya_adi in pdf_dosyalari.items():
    pdf_path = os.path.join(PDF_DIR, dosya_adi)

    print(f"\nOkunuyor: {yil} - {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"Dosya bulunamadı: {pdf_path}")
        continue

    with pdfplumber.open(pdf_path) as pdf:
        print(f"Sayfa sayısı: {len(pdf.pages)}")

        for sayfa_no, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                for row in table:
                    row = [temizle(cell) for cell in row]

                    if not any(row):
                        continue

                    birlesik = " ".join(row).lower()

                    # Başlık satırlarını atla
                    if (
                        "program kodu" in birlesik
                        or "program adı" in birlesik
                        or "puan türü" in birlesik
                        or "en küçük puan" in birlesik
                    ):
                        continue

                    # Satır uzunluğu eksikse tamamla
                    while len(row) < 8:
                        row.append("")

                    # Bazı PDF'lerde fazla kolon gelirse ilk 8 kolonu al
                    row = row[:8]

                    tum_satirlar.append({
                        "yil": yil,
                        "sayfa": sayfa_no,
                        "program_kodu": row[0],
                        "program_adi": row[1],
                        "puan_turu": row[2],
                        "kontenjan": row[3],
                        "yerlesen": row[4],
                        "bos_kontenjan": row[5],
                        "en_kucuk_puan": row[6],
                        "en_buyuk_puan": row[7],
                    })

print("\nToplam ham satır:", len(tum_satirlar))

df = pd.DataFrame(tum_satirlar)

df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("Ham yerleştirme CSV oluşturuldu:", OUTPUT_PATH)

print("\nİlk 20 satır:")
print(df.head(20))

print("\nYıllara göre ham satır sayısı:")
if not df.empty:
    print(df["yil"].value_counts().sort_index())
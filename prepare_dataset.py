import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split


RAW_DATA_PATH = "data/raw/Resume.csv"

PROCESSED_DIR = "data/processed"
FULL_OUTPUT_PATH = "data/processed/resume_binary_dataset.csv"
TRAIN_PATH = "data/processed/train.csv"
VAL_PATH = "data/processed/val.csv"
TEST_PATH = "data/processed/test.csv"


POSITIVE_CATEGORIES = [
    "INFORMATION-TECHNOLOGY",
    "ENGINEERING",
    "DIGITAL-MEDIA",
    "CONSULTANT",
    "BUSINESS-DEVELOPMENT"
]


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # HTML tag temizliği, olur da karışırsa diye
    text = re.sub(r"<.*?>", " ", text)

    # satır sonları ve fazla boşluk temizliği
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    print("Dataset okunuyor...")
    df = pd.read_csv(RAW_DATA_PATH, encoding="utf-8", engine="python")

    print("Mevcut kolonlar:")
    print(df.columns.tolist())

    required_columns = ["ID", "Resume_str", "Category"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Eksik kolon: {col}. Mevcut kolonlar: {df.columns.tolist()}")

    data = pd.DataFrame()

    data["id"] = df["ID"]
    data["text"] = df["Resume_str"].apply(clean_text)
    data["category"] = df["Category"].astype(str)

    # Çok kısa / boş metinleri çıkar
    data = data[data["text"].str.len() > 50]

    # Duplicate CV metinlerini çıkar
    data = data.drop_duplicates(subset=["text"])

    # Binary label:
    # INFORMATION-TECHNOLOGY = suitable
    # diğerleri = not_suitable
    data["label"] = data["category"].apply(
          lambda x: 1 if str(x).upper() in POSITIVE_CATEGORIES else 0
    ) 
   

    data["label_name"] = data["label"].map({
        1: "suitable",
        0: "not_suitable"
    })

    print("\nKategori dağılımı:")
    print(data["category"].value_counts())

    print("\nLabel dağılımı:")
    print(data["label_name"].value_counts())

    data.to_csv(FULL_OUTPUT_PATH, index=False, encoding="utf-8-sig")

    train_df, temp_df = train_test_split(
        data,
        test_size=0.30,
        random_state=42,
        stratify=data["label"]
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=42,
        stratify=temp_df["label"]
    )

    train_df.to_csv(TRAIN_PATH, index=False, encoding="utf-8-sig")
    val_df.to_csv(VAL_PATH, index=False, encoding="utf-8-sig")
    test_df.to_csv(TEST_PATH, index=False, encoding="utf-8-sig")

    print("\nDosyalar oluşturuldu:")
    print(FULL_OUTPUT_PATH)
    print(TRAIN_PATH)
    print(VAL_PATH)
    print(TEST_PATH)

    print("\nTrain/Val/Test satır sayıları:")
    print("Train:", len(train_df))
    print("Val:", len(val_df))
    print("Test:", len(test_df))


if __name__ == "__main__":
    main()
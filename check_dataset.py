import os
import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = "data/processed/resume_binary_dataset.csv"
OUTPUT_DIR = "outputs/figures"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    print("Dataset boyutu:", df.shape)
    print("\nKolonlar:")
    print(df.columns.tolist())

    print("\nİlk 5 satır:")
    print(df.head())

    print("\nLabel dağılımı:")
    print(df["label_name"].value_counts())

    print("\nKategori dağılımı:")
    print(df["category"].value_counts())

    df["text_length"] = df["text"].astype(str).apply(lambda x: len(x.split()))

    print("\nMetin uzunluğu istatistikleri:")
    print(df["text_length"].describe())

    # Label dağılım grafiği
    plt.figure(figsize=(7, 5))
    df["label_name"].value_counts().plot(kind="bar")
    plt.title("Label Distribution")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "label_distribution.png"))
    plt.close()

    # Kategori dağılım grafiği
    plt.figure(figsize=(12, 6))
    df["category"].value_counts().plot(kind="bar")
    plt.title("Category Distribution")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "category_distribution.png"))
    plt.close()

    # Metin uzunluğu histogramı
    plt.figure(figsize=(8, 5))
    df["text_length"].plot(kind="hist", bins=30)
    plt.title("Resume Text Length Distribution")
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "text_length_distribution.png"))
    plt.close()

    print("\nGrafikler oluşturuldu:")
    print(os.path.join(OUTPUT_DIR, "label_distribution.png"))
    print(os.path.join(OUTPUT_DIR, "category_distribution.png"))
    print(os.path.join(OUTPUT_DIR, "text_length_distribution.png"))


if __name__ == "__main__":
    main()
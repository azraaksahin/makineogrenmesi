import os
import time
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
    classification_report
)


TRAIN_PATH = "data/processed/train.csv"
VAL_PATH = "data/processed/val.csv"
TEST_PATH = "data/processed/test.csv"

OUTPUT_DIR = "outputs/baseline"
FIGURE_DIR = "outputs/figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)


def specificity_score(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn / (tn + fp)


def plot_confusion_matrix(cm, save_path):
    plt.figure(figsize=(6, 5))
    plt.imshow(cm)
    plt.title("TF-IDF + Logistic Regression Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    labels = ["not_suitable", "suitable"]
    plt.xticks([0, 1], labels, rotation=30)
    plt.yticks([0, 1], labels)

    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_roc_curve(y_true, y_prob, auc, save_path):
    fpr, tpr, _ = roc_curve(y_true, y_prob)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title("TF-IDF + Logistic Regression ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    print("Veriler yükleniyor...")

    train_df = pd.read_csv(TRAIN_PATH)
    val_df = pd.read_csv(VAL_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train = train_df["text"].astype(str)
    y_train = train_df["label"]

    X_val = val_df["text"].astype(str)
    y_val = val_df["label"]

    X_test = test_df["text"].astype(str)
    y_test = test_df["label"]

    print("TF-IDF vektörleştirme başlıyor...")

    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),
        min_df=2
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    print("Model eğitiliyor...")

    train_start = time.time()
    model.fit(X_train_vec, y_train)
    train_end = time.time()

    training_time = train_end - train_start

    print("Tahmin yapılıyor...")

    inference_start = time.time()
    y_pred = model.predict(X_test_vec)
    y_prob = model.predict_proba(X_test_vec)[:, 1]
    inference_end = time.time()

    inference_time = inference_end - inference_start

    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    sensitivity = recall
    specificity = specificity_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    cm = confusion_matrix(y_test, y_pred)

    print("\nSonuçlar:")
    print("Accuracy:", acc)
    print("Precision:", precision)
    print("Recall / Sensitivity:", recall)
    print("Specificity:", specificity)
    print("F1-score:", f1)
    print("AUC:", auc)
    print("Training time:", training_time)
    print("Inference time:", inference_time)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["not_suitable", "suitable"]))

    metrics = pd.DataFrame([{
        "model": "TF-IDF + Logistic Regression",
        "accuracy": acc,
        "precision": precision,
        "recall_sensitivity": recall,
        "specificity": specificity,
        "f1_score": f1,
        "auc": auc,
        "training_time_sec": training_time,
        "inference_time_sec": inference_time
    }])

    metrics.to_csv(
        os.path.join(OUTPUT_DIR, "baseline_metrics.csv"),
        index=False,
        encoding="utf-8-sig"
    )

    plot_confusion_matrix(
        cm,
        os.path.join(FIGURE_DIR, "baseline_confusion_matrix.png")
    )

    plot_roc_curve(
        y_test,
        y_prob,
        auc,
        os.path.join(FIGURE_DIR, "baseline_roc_curve.png")
    )

    print("\nDosyalar oluşturuldu:")
    print(os.path.join(OUTPUT_DIR, "baseline_metrics.csv"))
    print(os.path.join(FIGURE_DIR, "baseline_confusion_matrix.png"))
    print(os.path.join(FIGURE_DIR, "baseline_roc_curve.png"))


if __name__ == "__main__":
    main()
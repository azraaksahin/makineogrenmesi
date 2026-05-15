import os
import time
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)

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


# =========================
# MODEL SEÇİMİ
# =========================
MODEL_NAME = "bert-base-uncased"
MODEL_SHORT_NAME = "bert"

# Diğer modeller için sadece yukarıdaki iki satırı değiştir:
# MODEL_NAME = "distilbert-base-uncased"
# MODEL_SHORT_NAME = "distilbert"
#
# MODEL_NAME = "roberta-base"
# MODEL_SHORT_NAME = "roberta"
#
# MODEL_NAME = "albert-base-v2"
# MODEL_SHORT_NAME = "albert"
#
# MODEL_NAME = "microsoft/deberta-v3-small"
# MODEL_SHORT_NAME = "deberta"


TRAIN_PATH = "data/processed/train.csv"
VAL_PATH = "data/processed/val.csv"
TEST_PATH = "data/processed/test.csv"

OUTPUT_DIR = f"outputs/transformers/{MODEL_SHORT_NAME}"
FIGURE_DIR = "outputs/figures"
METRICS_DIR = "outputs/metrics"

MAX_LENGTH = 256
EPOCHS = 3
BATCH_SIZE = 8
LEARNING_RATE = 2e-5


os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)


def specificity_score(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn / (tn + fp)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)

    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()[:, 1]

    acc = accuracy_score(labels, preds)
    precision = precision_score(labels, preds, zero_division=0)
    recall = recall_score(labels, preds, zero_division=0)
    specificity = specificity_score(labels, preds)
    f1 = f1_score(labels, preds, zero_division=0)

    try:
        auc = roc_auc_score(labels, probs)
    except:
        auc = 0.0

    return {
        "accuracy": acc,
        "precision": precision,
        "recall_sensitivity": recall,
        "specificity": specificity,
        "f1": f1,
        "auc": auc
    }


def tokenize_function(example, tokenizer):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH
    )


def plot_confusion_matrix(cm, save_path):
    plt.figure(figsize=(6, 5))
    plt.imshow(cm)
    plt.title(f"{MODEL_SHORT_NAME.upper()} Confusion Matrix")
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
    plt.title(f"{MODEL_SHORT_NAME.upper()} ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_loss_curve(log_history, save_path):
    train_loss = []
    eval_loss = []
    steps_train = []
    steps_eval = []

    for item in log_history:
        if "loss" in item and "epoch" in item:
            train_loss.append(item["loss"])
            steps_train.append(item["epoch"])

        if "eval_loss" in item and "epoch" in item:
            eval_loss.append(item["eval_loss"])
            steps_eval.append(item["epoch"])

    plt.figure(figsize=(7, 5))

    if train_loss:
        plt.plot(steps_train, train_loss, label="Training Loss")

    if eval_loss:
        plt.plot(steps_eval, eval_loss, label="Validation Loss")

    plt.title(f"{MODEL_SHORT_NAME.upper()} Training vs Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    print(f"Model başlıyor: {MODEL_SHORT_NAME} -> {MODEL_NAME}")

    train_df = pd.read_csv(TRAIN_PATH)
    val_df = pd.read_csv(VAL_PATH)
    test_df = pd.read_csv(TEST_PATH)

    train_df = train_df[["text", "label"]]
    val_df = val_df[["text", "label"]]
    test_df = test_df[["text", "label"]]

    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    test_dataset = Dataset.from_pandas(test_df)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = train_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    val_dataset = val_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
    test_dataset = test_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)

    train_dataset = train_dataset.rename_column("label", "labels")
    val_dataset = val_dataset.rename_column("label", "labels")
    test_dataset = test_dataset.rename_column("label", "labels")

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    )

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=EPOCHS,
        weight_decay=0.01,
        logging_dir=f"{OUTPUT_DIR}/logs",
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )

    print("Eğitim başlıyor...")

    train_start = time.time()
    trainer.train()
    train_end = time.time()

    training_time = train_end - train_start

    print("Test tahmini başlıyor...")

    inference_start = time.time()
    predictions = trainer.predict(test_dataset)
    inference_end = time.time()

    inference_time = inference_end - inference_start

    logits = predictions.predictions
    y_true = predictions.label_ids
    y_pred = np.argmax(logits, axis=1)
    y_prob = torch.softmax(torch.tensor(logits), dim=1).numpy()[:, 1]

    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    sensitivity = recall
    specificity = specificity_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    auc = roc_auc_score(y_true, y_prob)

    cm = confusion_matrix(y_true, y_pred)

    print("\nTest Sonuçları:")
    print("Accuracy:", acc)
    print("Precision:", precision)
    print("Recall / Sensitivity:", sensitivity)
    print("Specificity:", specificity)
    print("F1-score:", f1)
    print("AUC:", auc)
    print("Training time:", training_time)
    print("Inference time:", inference_time)

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["not_suitable", "suitable"]))

    metrics = pd.DataFrame([{
        "model": MODEL_SHORT_NAME,
        "model_name": MODEL_NAME,
        "accuracy": acc,
        "precision": precision,
        "recall_sensitivity": sensitivity,
        "specificity": specificity,
        "f1_score": f1,
        "auc": auc,
        "training_time_sec": training_time,
        "inference_time_sec": inference_time
    }])

    metrics_path = os.path.join(METRICS_DIR, f"{MODEL_SHORT_NAME}_metrics.csv")
    metrics.to_csv(metrics_path, index=False, encoding="utf-8-sig")

    plot_confusion_matrix(
        cm,
        os.path.join(FIGURE_DIR, f"{MODEL_SHORT_NAME}_confusion_matrix.png")
    )

    plot_roc_curve(
        y_true,
        y_prob,
        auc,
        os.path.join(FIGURE_DIR, f"{MODEL_SHORT_NAME}_roc_curve.png")
    )

    plot_loss_curve(
        trainer.state.log_history,
        os.path.join(FIGURE_DIR, f"{MODEL_SHORT_NAME}_loss_curve.png")
    )

    trainer.save_model(os.path.join(OUTPUT_DIR, "best_model"))
    tokenizer.save_pretrained(os.path.join(OUTPUT_DIR, "best_model"))

    print("\nDosyalar oluşturuldu:")
    print(metrics_path)
    print(os.path.join(FIGURE_DIR, f"{MODEL_SHORT_NAME}_confusion_matrix.png"))
    print(os.path.join(FIGURE_DIR, f"{MODEL_SHORT_NAME}_roc_curve.png"))
    print(os.path.join(FIGURE_DIR, f"{MODEL_SHORT_NAME}_loss_curve.png"))


if __name__ == "__main__":
    main()
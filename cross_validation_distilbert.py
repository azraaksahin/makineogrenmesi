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

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


MODEL_NAME = "distilbert-base-uncased"
MODEL_SHORT_NAME = "distilbert_5fold_cv"

DATA_PATH = "data/processed/resume_binary_dataset.csv"

OUTPUT_DIR = "outputs/cross_validation/distilbert"
FIGURE_DIR = "outputs/cross_validation/figures"
METRICS_DIR = "outputs/cross_validation/metrics"

MAX_LENGTH = 256
EPOCHS = 3
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
N_SPLITS = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    probs = torch.softmax(torch.tensor(logits), dim=1).numpy()[:, 1]

    return {
        "accuracy": accuracy_score(labels, preds),
        "precision": precision_score(labels, preds, zero_division=0),
        "recall": recall_score(labels, preds, zero_division=0),
        "f1": f1_score(labels, preds, zero_division=0),
        "auc": roc_auc_score(labels, probs)
    }


def tokenize_function(example, tokenizer):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH
    )


def plot_loss_curve(log_history, fold_no):
    train_loss = []
    eval_loss = []
    train_epochs = []
    eval_epochs = []

    for item in log_history:
        if "loss" in item and "epoch" in item:
            train_loss.append(item["loss"])
            train_epochs.append(item["epoch"])

        if "eval_loss" in item and "epoch" in item:
            eval_loss.append(item["eval_loss"])
            eval_epochs.append(item["epoch"])

    plt.figure(figsize=(7, 5))

    if train_loss:
        plt.plot(train_epochs, train_loss, label="Training Loss")

    if eval_loss:
        plt.plot(eval_epochs, eval_loss, label="Validation Loss")

    plt.title(f"DistilBERT Fold {fold_no} Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()

    save_path = os.path.join(FIGURE_DIR, f"distilbert_fold_{fold_no}_loss_curve.png")
    plt.savefig(save_path)
    plt.close()


def main():
    print("5-Fold Cross Validation başlıyor...")

    df = pd.read_csv(DATA_PATH)
    df = df[["text", "label"]].dropna()

    X = df["text"].values
    y = df["label"].values

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)

    fold_results = []

    for fold_no, (train_idx, val_idx) in enumerate(skf.split(X, y), start=1):
        print(f"\n===== Fold {fold_no}/{N_SPLITS} başlıyor =====")

        train_df = df.iloc[train_idx].reset_index(drop=True)
        val_df = df.iloc[val_idx].reset_index(drop=True)

        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)

        train_dataset = train_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)
        val_dataset = val_dataset.map(lambda x: tokenize_function(x, tokenizer), batched=True)

        train_dataset = train_dataset.rename_column("label", "labels")
        val_dataset = val_dataset.rename_column("label", "labels")

        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=2
        )

        fold_output_dir = os.path.join(OUTPUT_DIR, f"fold_{fold_no}")

        training_args = TrainingArguments(
            output_dir=fold_output_dir,
            eval_strategy="epoch",
            save_strategy="epoch",
            learning_rate=LEARNING_RATE,
            per_device_train_batch_size=BATCH_SIZE,
            per_device_eval_batch_size=BATCH_SIZE,
            num_train_epochs=EPOCHS,
            weight_decay=0.01,
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
            data_collator=data_collator,
            compute_metrics=compute_metrics
        )

        start_time = time.time()
        trainer.train()
        end_time = time.time()

        eval_result = trainer.evaluate()

        fold_results.append({
            "fold": fold_no,
            "accuracy": eval_result.get("eval_accuracy"),
            "precision": eval_result.get("eval_precision"),
            "recall": eval_result.get("eval_recall"),
            "f1": eval_result.get("eval_f1"),
            "auc": eval_result.get("eval_auc"),
            "training_time_sec": end_time - start_time
        })

        plot_loss_curve(trainer.state.log_history, fold_no)

        trainer.save_model(os.path.join(fold_output_dir, "best_model"))
        tokenizer.save_pretrained(os.path.join(fold_output_dir, "best_model"))

    results_df = pd.DataFrame(fold_results)

    results_path = os.path.join(METRICS_DIR, "distilbert_5fold_cv_results.csv")
    results_df.to_csv(results_path, index=False, encoding="utf-8-sig")

    mean_results = results_df.mean(numeric_only=True).to_frame().T
    mean_results["fold"] = "mean"

    final_df = pd.concat([results_df, mean_results], ignore_index=True)
    final_path = os.path.join(METRICS_DIR, "distilbert_5fold_cv_results_with_mean.csv")
    final_df.to_csv(final_path, index=False, encoding="utf-8-sig")

    print("\n5-Fold CV tamamlandı.")
    print(final_df)
    print("\nDosyalar oluşturuldu:")
    print(results_path)
    print(final_path)


if __name__ == "__main__":
    main()
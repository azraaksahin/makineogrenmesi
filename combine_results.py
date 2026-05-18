import os
import pandas as pd
import matplotlib.pyplot as plt


METRICS_DIR = "resume_ai_outputs/metrics"
FIGURE_DIR = "resume_ai_outputs/figures"
OUTPUT_PATH = "resume_ai_outputs/metrics/all_model_results.csv"


def normalize_columns(df):
    rename_map = {
        "f1": "f1_score",
        "recall": "recall_sensitivity",
        "training_time": "training_time_sec",
        "inference_time": "inference_time_sec"
    }

    df = df.rename(columns=rename_map)

    expected_columns = [
        "model",
        "accuracy",
        "precision",
        "recall_sensitivity",
        "specificity",
        "f1_score",
        "auc",
        "training_time_sec",
        "inference_time_sec"
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    return df[expected_columns]


def plot_metric_comparison(df, metric_name, save_path):
    plot_df = df.sort_values(by=metric_name, ascending=False)

    plt.figure(figsize=(10, 5))
    plt.bar(plot_df["model"], plot_df[metric_name])
    plt.title(f"Model Comparison by {metric_name}")
    plt.xlabel("Model")
    plt.ylabel(metric_name)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    os.makedirs(METRICS_DIR, exist_ok=True)
    os.makedirs(FIGURE_DIR, exist_ok=True)

    all_metrics = []

    for file_name in os.listdir(METRICS_DIR):
        if not file_name.endswith("_metrics.csv"):
            continue

        if file_name == "all_model_results.csv":
            continue

        path = os.path.join(METRICS_DIR, file_name)
        print(f"Okunuyor: {path}")

        df = pd.read_csv(path)
        df = normalize_columns(df)
        all_metrics.append(df)

    if not all_metrics:
        raise ValueError("resume_ai_results/metrics içinde *_metrics.csv dosyası bulunamadı.")

    results = pd.concat(all_metrics, ignore_index=True)

    # Aynı model birden fazla kez varsa sonuncuyu tut
    results = results.drop_duplicates(subset=["model"], keep="last")

    numeric_cols = [
        "accuracy",
        "precision",
        "recall_sensitivity",
        "specificity",
        "f1_score",
        "auc",
        "training_time_sec",
        "inference_time_sec"
    ]

    for col in numeric_cols:
        results[col] = pd.to_numeric(results[col], errors="coerce")

    results = results.sort_values(by="f1_score", ascending=False)

    results.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("\nBirleştirilmiş model sonuçları oluşturuldu:")
    print(OUTPUT_PATH)

    print("\nSonuç tablosu:")
    print(results)

    plot_metric_comparison(
        results,
        "accuracy",
        os.path.join(FIGURE_DIR, "model_accuracy_comparison.png")
    )

    plot_metric_comparison(
        results,
        "f1_score",
        os.path.join(FIGURE_DIR, "model_f1_comparison.png")
    )

    plot_metric_comparison(
        results,
        "auc",
        os.path.join(FIGURE_DIR, "model_auc_comparison.png")
    )

    plot_metric_comparison(
        results,
        "inference_time_sec",
        os.path.join(FIGURE_DIR, "model_inference_time_comparison.png")
    )

    print("\nKarşılaştırma grafikleri oluşturuldu:")
    print(os.path.join(FIGURE_DIR, "model_accuracy_comparison.png"))
    print(os.path.join(FIGURE_DIR, "model_f1_comparison.png"))
    print(os.path.join(FIGURE_DIR, "model_auc_comparison.png"))
    print(os.path.join(FIGURE_DIR, "model_inference_time_comparison.png"))


if __name__ == "__main__":
    main()
import argparse
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_PATH = "resume_ai_outputs/transformers/distilbert/best_model"

LABEL_MAP = {
    0: "not_suitable",
    1: "suitable"
}


def predict(text):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model klasörü bulunamadı: {MODEL_PATH}. "
            "DistilBERT best_model klasörünü bu konuma koymalısın."
        )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=256,
        return_tensors="pt"
    )

    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)[0]

    predicted_label = torch.argmax(probabilities).item()
    confidence = probabilities[predicted_label].item()

    return LABEL_MAP[predicted_label], confidence, probabilities.tolist()


def main():
    parser = argparse.ArgumentParser(
        description="Resume suitability prediction using the best trained DistilBERT model."
    )

    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="Resume text to classify."
    )

    args = parser.parse_args()

    label, confidence, probabilities = predict(args.text)

    print("Prediction:", label)
    print("Confidence:", round(confidence * 100, 2), "%")
    print("Probability not_suitable:", round(probabilities[0] * 100, 2), "%")
    print("Probability suitable:", round(probabilities[1] * 100, 2), "%")


if __name__ == "__main__":
    main()
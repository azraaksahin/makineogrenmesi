import os
import csv


TXT_FOLDER = "data/selenium_resumes"
CSV_PATH = "data/software_resumes.csv"


def prepare_folders():
    os.makedirs(TXT_FOLDER, exist_ok=True)
    os.makedirs("data", exist_ok=True)


def save_text(text, index):
    prepare_folders()

    path = f"{TXT_FOLDER}/resume_{index}.txt"

    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

    return path


def save_to_csv(rows):
    prepare_folders()

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["id", "url", "text"])

        for row in rows:
            writer.writerow(row)

    return CSV_PATH
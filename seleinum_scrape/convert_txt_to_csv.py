import os
import re
import pandas as pd


TXT_FOLDER = "data/selenium_resumes"
OUTPUT_CSV = "data/software_resumes_clean.csv"


def clean_text(text):
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def get_between(text, start_word, end_words):
    start = text.lower().find(start_word.lower())

    if start == -1:
        return ""

    start += len(start_word)

    end = len(text)

    for end_word in end_words:
        idx = text.lower().find(end_word.lower(), start)
        if idx != -1:
            end = min(end, idx)

    return text[start:end].strip()


def extract_name(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return lines[0] if lines else ""


def extract_summary(text):
    return get_between(
        text,
        "Summary",
        ["Education", "Skills", "Experience"]
    )


def extract_education(text):
    return get_between(
        text,
        "Education",
        ["Skills", "Experience"]
    )


def extract_skills(text):
    return get_between(
        text,
        "Skills",
        ["Experience", "Education"]
    )


def extract_experience(text):
    return get_between(
        text,
        "Experience",
        ["Skills", "Education"]
    )


def guess_job_title(text):
    job_titles = [
        "Software Engineer",
        "Software Developer",
        "Java Developer",
        "Web Developer",
        "Front End Developer",
        "Frontend Developer",
        "Data Analyst",
        "Data Scientist",
        "DevOps Engineer",
        "Development Operations Engineer",
        "IT Support",
        "Systems Administrator",
        "Quality Assurance Engineer",
        "QA Engineer",
        "Computer Scientist",
        "Business Analyst"
    ]

    lower_text = text.lower()

    for title in job_titles:
        if title.lower() in lower_text:
            return title

    return ""


def main():
    rows = []

    files = sorted(os.listdir(TXT_FOLDER))

    for file_name in files:
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(TXT_FOLDER, file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                full_text = clean_text(file.read())

            row = {
                "id": file_name.replace(".txt", ""),
                "source": "resume.com",
                "job_title": guess_job_title(full_text),
                "name": extract_name(full_text),
                "summary": extract_summary(full_text),
                "skills": extract_skills(full_text),
                "experience": extract_experience(full_text),
                "education": extract_education(full_text),
                "full_text": full_text
            }

            rows.append(row)
            print(f"Okundu: {file_name}")

        except Exception as e:
            print(f"Hata: {file_name} -> {e}")

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("\nCSV oluşturuldu:")
    print(OUTPUT_CSV)
    print(f"Toplam CV: {len(df)}")


if __name__ == "__main__":
    main()
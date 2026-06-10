import os
import re
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/processed/resume_binary_dataset.csv"
OUTPUT_PATH = "outputs/job_match_results.csv"

ENGINEER_KEYWORDS = [
    "engineer","engineering", "software engineer", "computer engineer",
    "developer", "programmer", "backend", "frontend", "full stack",
    "data engineer", "machine learning engineer"
]

SKILL_KEYWORDS = [
    "python","java", "sql", "c#", "c++", "javascript", "html", "css",
    "react", "node.js", "django", "flask", "machine learning",
    "deep learning", "tensorflow", "pytorch", "pandas", "numpy",
    "scikit-learn", "git", "github", "docker", "linux", "api"
]


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9#+.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_required_skills(job_text):
    job_text = clean_text(job_text)
    found_skills = []

    for skill in SKILL_KEYWORDS:
        if skill.lower() in job_text:
            found_skills.append(skill)

    return found_skills


def is_engineer_cv(cv_text):
    cv_text = clean_text(cv_text)

    for keyword in ENGINEER_KEYWORDS:
        if keyword in cv_text:
            return True

    return False


def find_matching_skills(cv_text, required_skills):
    cv_text = clean_text(cv_text)

    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in cv_text:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


def plot_pipeline_summary(total_candidates, engineer_count, matched_count):
    stages = ["Toplam CV", "Muhendis Aday", "Beceri Eslesen Aday"]
    values = [total_candidates, engineer_count, matched_count]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(stages, values)

    plt.title("Akilli Ise Alim Aday Eleme Sureci")
    plt.xlabel("Asama")
    plt.ylabel("Aday Sayisi")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom"
        )

    os.makedirs("outputs/figures", exist_ok=True)
    plt.tight_layout()
    plt.savefig("outputs/figures/job_matching_pipeline.png", dpi=300)
    plt.close()


def plot_top_candidates(results_df):
    top10 = results_df.head(10)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(
        top10["candidate_id"].astype(str),
        top10["match_score"]
    )

    plt.title("En Uygun 10 Aday")
    plt.xlabel("Aday ID")
    plt.ylabel("Uyum Skoru (%)")
    plt.ylim(0, 110)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.0f}%",
            ha="center",
            va="bottom"
        )

    os.makedirs("outputs/figures", exist_ok=True)
    plt.tight_layout()
    plt.savefig("outputs/figures/top10_candidates.png", dpi=300)
    plt.close()


def plot_skill_distribution(results_df, required_skills):
    skill_counts = {}

    for skill in required_skills:
        count = results_df["matched_skills"].apply(
            lambda x: skill in str(x).split(", ")
        ).sum()
        skill_counts[skill] = count

    plt.figure(figsize=(9, 5))
    bars = plt.bar(skill_counts.keys(), skill_counts.values())

    plt.title("Istenen Becerilere Gore Aday Dagilimi")
    plt.xlabel("Beceri")
    plt.ylabel("Eslesen Aday Sayisi")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom"
        )

    os.makedirs("outputs/figures", exist_ok=True)
    plt.tight_layout()
    plt.savefig("outputs/figures/skill_distribution.png", dpi=300)
    plt.close()


def main():
    print("Akıllı İşe Alım - İş İlanı Bazlı Aday Eşleştirme")
    print("-" * 60)

    job_text = input("İş ilanı gereksinimlerini yazınız: ")

    required_skills = extract_required_skills(job_text)

    if not required_skills:
        print("İş ilanından teknik beceri bulunamadı.")
        return

    print("\nİstenen teknik beceriler:", required_skills)

    df = pd.read_csv(DATA_PATH)
    df = df[["text", "label"]].dropna()

    total_candidates = len(df)
    engineer_count = 0
    matched_count = 0

    results = []

    for index, row in df.iterrows():
        cv_text = row["text"]

        if not is_engineer_cv(cv_text):
            continue

        engineer_count += 1

        matched, missing = find_matching_skills(cv_text, required_skills)

        match_score = len(matched) / len(required_skills) * 100

        if match_score > 0:
            matched_count += 1

            results.append({
                "candidate_id": index,
                "matched_skills": ", ".join(matched),
                "missing_skills": ", ".join(missing),
                "match_score": round(match_score, 2),
                "cv_preview": str(cv_text)[:250]
            })

    results_df = pd.DataFrame(results)

    plot_pipeline_summary(total_candidates, engineer_count, matched_count)

    if results_df.empty:
        print("\nUygun mühendis aday bulunamadı.")
        print("Gorsel olusturuldu: outputs/figures/job_matching_pipeline.png")
        return

    results_df = results_df.sort_values(by="match_score", ascending=False)

    os.makedirs("outputs", exist_ok=True)
    results_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    plot_top_candidates(results_df)
    plot_candidate_ranking(results_df)
    plot_skill_distribution(results_df, required_skills)

    print("\nEn uygun adaylar:")
    print(results_df[["candidate_id", "matched_skills", "missing_skills", "match_score"]].head(10))

    print(f"\nSonuç dosyası oluşturuldu: {OUTPUT_PATH}")
    print("Gorsel olusturuldu: outputs/figures/job_matching_pipeline.png")
    print("Gorsel olusturuldu: outputs/figures/top10_candidates.png")
    print("Gorsel olusturuldu: outputs/figures/skill_distribution.png")
def plot_candidate_ranking(results_df):

    top20 = results_df.head(20)

    plt.figure(figsize=(12,6))

    bars = plt.bar(
        top20["candidate_id"].astype(str),
        top20["match_score"]
    )

    plt.title("Aday Uygunluk Siralamasi")
    plt.xlabel("Aday ID")
    plt.ylabel("Uyumluluk Skoru (%)")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.0f}%",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    plt.savefig(
        "outputs/figures/candidate_ranking.png",
        dpi=300
    )

    plt.close()

if __name__ == "__main__":
    main()
import pandas as pd
import re
import html


INPUT_FILE = "data/reddit_software_resume_posts.csv"
OUTPUT_FILE = "data/clean_reddit_software_resume_posts.csv"

TECH_KEYWORDS = [
    "software", "developer", "programmer", "frontend", "backend",
    "full stack", "full-stack", "web developer", "software engineer",
    "data analyst", "data scientist", "data engineer",
    "machine learning", "ml engineer", "ai engineer",
    "devops", "cloud", "cybersecurity", "security analyst",
    "it support", "qa engineer", "test engineer",
    "python", "java", "javascript", "typescript", "react",
    "node", "sql", "html", "css", "git", "github",
    "aws", "azure", "docker", "linux"
]

RESUME_KEYWORDS = [
    "resume", "cv", "roast my resume", "review my resume",
    "resume review", "feedback", "ats", "interview",
    "internship", "entry level", "junior", "new grad"
]

BAD_KEYWORDS = [
    "marketing", "nurse", "teacher", "chef", "cook",
    "attorney", "lawyer", "banker", "accountant",
    "mechanical engineer", "civil engineer", "construction",
    "restaurant", "medical", "housekeeper", "retail only"
]


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = html.unescape(text)

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\.\S+", " ", text)
    text = re.sub(r"\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"&amp;#x200B;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_any(text, keywords):
    text = text.lower()
    return any(keyword in text for keyword in keywords)


def main():
    print("Dataset okunuyor...")

    df = pd.read_csv(INPUT_FILE)

    print("İlk satır sayısı:", len(df))

    df["title"] = df["title"].apply(clean_text)
    df["selftext"] = df["selftext"].apply(clean_text)

    df["combined_text"] = df["title"] + " " + df["selftext"]

    # boş title sil
    df = df[df["title"].str.len() > 10]

    # çok kısa içerikleri sil
    df = df[df["combined_text"].str.len() > 40]

    # duplicate sil
    df = df.drop_duplicates(subset=["id"])
    df = df.drop_duplicates(subset=["title"])

    # yazılım + resume alakası
    df = df[
        df["combined_text"].apply(lambda x: contains_any(x, TECH_KEYWORDS)) &
        df["combined_text"].apply(lambda x: contains_any(x, RESUME_KEYWORDS))
    ]

    # bariz alakasızları sil
    df = df[
        ~df["combined_text"].apply(lambda x: contains_any(x, BAD_KEYWORDS))
    ]

    # gereksiz kolon varsa sadeleştir
    keep_columns = [
        "id",
        "subreddit",
        "query",
        "title",
        "selftext",
        "combined_text",
        "score",
        "num_comments",
        "created_utc",
        "url"
    ]

    df = df[[col for col in keep_columns if col in df.columns]]

    print("Temizlenmiş satır sayısı:", len(df))

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("Temiz dataset kaydedildi:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
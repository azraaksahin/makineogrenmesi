import os
import re
import torch
import pandas as pd
import streamlit as st
import plotly.express as px
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_PATH = "resume_ai_outputs/transformers/distilbert/best_model"
DATA_PATH = "data/processed/resume_binary_dataset.csv"

LABEL_MAP = {
    0: "not_suitable",
    1: "suitable"
}

ENGINEER_KEYWORDS = [
    "engineer", "engineering", "software engineer", "computer engineer",
    "developer", "programmer", "backend", "frontend", "full stack",
    "data engineer", "machine learning engineer"
]

SKILL_KEYWORDS = [
    "python", "java", "sql", "c#", "c++", "javascript", "html", "css",
    "react", "node.js", "django", "flask", "machine learning",
    "deep learning", "tensorflow", "pytorch", "pandas", "numpy",
    "scikit-learn", "git", "github", "docker", "linux", "api"
]


st.set_page_config(
    page_title="AI Resume Suitability Analyzer",
    page_icon="🧠",
    layout="wide"
)


@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    return tokenizer, model, device


@st.cache_data
def load_dataset():
    return pd.read_csv(DATA_PATH)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9#+.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def predict_cv(text):
    tokenizer, model, device = load_model()

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


def match_candidates(job_text):
    required_skills = extract_required_skills(job_text)

    if not required_skills:
        return pd.DataFrame(), required_skills

    df = load_dataset()
    df = df[["text", "label"]].dropna()

    results = []

    for index, row in df.iterrows():
        cv_text = row["text"]

        if not is_engineer_cv(cv_text):
            continue

        matched, missing = find_matching_skills(cv_text, required_skills)
        match_score = len(matched) / len(required_skills) * 100

        if match_score > 0:
            results.append({
                "candidate_id": index,
                "matched_skills": ", ".join(matched),
                "missing_skills": ", ".join(missing),
                "match_score": round(match_score, 2),
                "cv_preview": str(cv_text)[:300]
            })

    results_df = pd.DataFrame(results)

    if not results_df.empty:
        results_df = results_df.sort_values(by="match_score", ascending=False)

    return results_df, required_skills


st.title("AI Resume Suitability Analyzer")
st.caption("Transformer tabanlı CV uygunluk analizi ve iş ilanı bazlı aday eşleştirme sistemi")

tab1, tab2 = st.tabs([
    "CV Uygunluk Analizi",
    "İş İlanı Bazlı Aday Eşleştirme"
])


with tab1:
    st.header("CV Uygunluk Analizi")

    cv_text = st.text_area(
        "CV metnini buraya yapıştır:",
        height=250,
        placeholder="Experienced software engineer with Python, Java, SQL..."
    )

    if st.button("CV'yi Analiz Et"):
        if not cv_text.strip():
            st.warning("Önce CV metni gir.")
        elif not os.path.exists(MODEL_PATH):
            st.error(f"Model klasörü bulunamadı: {MODEL_PATH}")
        else:
            label, confidence, probs = predict_cv(cv_text)

            col1, col2, col3 = st.columns(3)

            col1.metric("Tahmin", label)
            col2.metric("Güven", f"{confidence * 100:.2f}%")
            col3.metric("Suitable Olasılığı", f"{probs[1] * 100:.2f}%")

            prob_df = pd.DataFrame({
                "Label": ["not_suitable", "suitable"],
                "Probability": [probs[0], probs[1]]
            })

            fig = px.bar(
                prob_df,
                x="Label",
                y="Probability",
                title="Model Olasılık Dağılımı",
                text_auto=".2%"
            )

            st.plotly_chart(fig, use_container_width=True)

            if label == "suitable":
                st.success("Bu CV teknik/BT odaklı pozisyonlar için uygun görünüyor.")
            else:
                st.error("Bu CV teknik/BT odaklı pozisyonlar için düşük uygunluk gösteriyor.")


with tab2:
    st.header("İş İlanı Bazlı Aday Eşleştirme")

    job_text = st.text_area(
        "İş ilanı gereksinimlerini yaz:",
        height=160,
        placeholder="Python, SQL, Docker, machine learning..."
    )

    if st.button("Adayları Eşleştir"):
        if not job_text.strip():
            st.warning("Önce iş ilanı gereksinimlerini gir.")
        else:
            results_df, required_skills = match_candidates(job_text)

            st.subheader("Tespit Edilen Teknik Beceriler")
            st.write(required_skills)

            if results_df.empty:
                st.warning("Eşleşen aday bulunamadı.")
            else:
                st.subheader("En Uygun Adaylar")
                st.dataframe(
                    results_df[[
                        "candidate_id",
                        "matched_skills",
                        "missing_skills",
                        "match_score",
                        "cv_preview"
                    ]].head(20),
                    use_container_width=True
                )

                top10 = results_df.head(10)

                fig = px.bar(
                    top10,
                    x="candidate_id",
                    y="match_score",
                    title="En Uygun 10 Aday",
                    text="match_score"
                )

                st.plotly_chart(fig, use_container_width=True)

                os.makedirs("resume_ai_outputs/job_matching", exist_ok=True)
                output_path = "resume_ai_outputs/job_matching/job_match_results.csv"
                results_df.to_csv(output_path, index=False, encoding="utf-8-sig")

                st.success(f"Sonuç dosyası oluşturuldu: {output_path}")
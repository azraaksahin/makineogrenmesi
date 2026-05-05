SUBREDDITS = [
    "resumes",
    "EngineeringResumes",
    "cscareerquestions",
    "csMajors",
    "learnprogramming",
    "webdev",
    "datascience",
    "dataengineering",
    "devops",
    "ITCareerQuestions"
]

SEARCH_QUERIES = [
    "software engineer resume",
    "developer resume",
    "data analyst resume",
    "data scientist resume",
    "web developer resume",
    "internship resume",
    "junior developer resume",
    "resume review",
    "roast my resume",
    "cv review"
]

TECH_KEYWORDS = [
    "software", "developer", "programmer", "web developer",
    "frontend", "backend", "full stack", "data analyst",
    "data scientist", "data engineer", "machine learning",
    "devops", "qa", "it support", "cybersecurity",
    "python", "java", "javascript", "react", "node",
    "sql", "html", "css", "git", "linux", "aws", "azure"
]

RESUME_KEYWORDS = [
    "resume", "cv", "roast my resume", "review my resume",
    "resume review", "feedback", "internship", "entry level",
    "junior", "new grad"
]


def is_relevant_post(title, selftext):
    text = f"{title} {selftext}".lower()

    has_resume_context = any(word in text for word in RESUME_KEYWORDS)
    has_tech_context = any(word in text for word in TECH_KEYWORDS)

    return has_resume_context and has_tech_context
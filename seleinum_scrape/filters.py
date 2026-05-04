SOFTWARE_TITLES = [
    # Software
    "software engineer",
    "software developer",
    "web developer",
    "frontend developer",
    "front-end developer",
    "backend developer",
    "back-end developer",
    "full stack developer",
    "full-stack developer",
    "programmer",
    "developer",
    "application developer",
    "mobile developer",
    "android developer",
    "ios developer",

    # Data
    "data analyst",
    "data scientist",
    "data engineer",
    "business analyst",
    "business intelligence analyst",
    "bi analyst",
    "analytics analyst",
    "data analytics",

    # Advanced tech
    "machine learning engineer",
    "ai engineer",
    "devops engineer",
    "cloud engineer",

    # IT
    "qa engineer",
    "test engineer",
    "automation engineer",
    "it support",
    "it specialist",
    "system administrator",
    "systems administrator",
    "network engineer",
    "database administrator",
    "cybersecurity analyst",
    "security analyst"
]


SOFTWARE_SKILLS = [
    # Core dev
    "python", "java", "javascript", "typescript",
    "react", "angular", "vue",
    "node", "node.js",
    "django", "flask", "spring",

    # DB
    "sql", "mysql", "postgresql", "mongodb",

    # Web
    "html", "css",

    # Languages
    "php", "c++", "c#", ".net",

    # Tools
    "git", "github", "api", "rest",
    "linux", "docker", "kubernetes",
    "aws", "azure", "cloud",

    # ML
    "machine learning", "tensorflow", "pytorch",

    # IT
    "active directory", "computer networking", "windows server",

    # Data
    "excel", "power bi", "tableau",
    "statistics", "data visualization",
    "data analysis", "analytics", "reporting"
]


BAD_JOBS = [
    "nurse", "chef", "cook", "banker", "attorney",
    "law", "mechanical engineer", "civil engineer",
    "construction", "landscape", "journalist",
    "teacher", "graphic designer", "creative director",
    "accountant", "babysitter", "nanny", "police",
    "medical", "housekeeper", "caregiver",
    "public health", "clinical", "culinary",
    "restaurant", "investment", "banking"
]


def extract_real_resume_part(text):
    if not text:
        return ""

    end_markers = [
        "What skills help",
        "Is this helpful?",
        "Resume Tips",
        "Ready to get started?",
        "Create My Resume",
        "Similar Samples"
    ]

    end_index = len(text)

    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            end_index = min(end_index, idx)

    return text[:end_index].strip()


def is_software_link(url):
    if not url:
        return False

    url = url.lower().replace("-", " ")

    # ❌ kötü meslekleri URL’den ele
    for bad in BAD_JOBS:
        if bad in url:
            return False

    # 🎯 direkt eşleşme varsa al
    for title in SOFTWARE_TITLES:
        if title in url:
            return True

    # 🔎 genel yazılım kelimeleri
    useful_url_words = [
        "software",
        "developer",
        "programmer",
        "web",
        "data",
        "it",
        "computer",
        "network",
        "system",
        "cloud",
        "devops",
        "cyber",
        "security",
        "database",
        "qa",
        "analyst"
    ]

    return any(word in url for word in useful_url_words)


def is_software_cv(text):
    if not text:
        return False

    clean_text = extract_real_resume_part(text)
    lower_text = clean_text.lower()

    # ❌ kötü meslekleri ele
    for bad in BAD_JOBS:
        if bad in lower_text:
            return False

    # 🎯 title eşleşmesi
    title_match = any(title in lower_text for title in SOFTWARE_TITLES)

    # 🧠 skill skoru
    skill_score = sum(1 for skill in SOFTWARE_SKILLS if skill in lower_text)

    # ✅ karar
    return title_match or skill_score >= 4
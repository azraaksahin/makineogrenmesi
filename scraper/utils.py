import re

def is_real_cv(text):
    if not isinstance(text, str):
        return False

    text_lower = text.lower()


    if len(text.split()) < 30:
        return False

    score = 0


    if "experience" in text_lower:
        score += 1

    if "education" in text_lower:
        score += 1

    if "skills" in text_lower:
        score += 1


    if any(j in text_lower for j in ["engineer", "developer", "intern", "manager"]):
        score += 2

    # email varsa bonus
    if re.search(r"\S+@\S+\.\S+", text):
        score += 2

    
    if "linkedin" in text_lower or "github" in text_lower:
        score += 1

    return score >= 2
def is_real_cv(text):
    if not isinstance(text, str) or len(text.split()) < 100:
        return False
    
    # kesin sahte/alakasız işaretler
    fake_keywords = [
        "placeholder", "template", "this pdf should", "replace this",
        "project gutenberg", "end of document", "disciplinary",
        "<!doctype", "<html", "copyright", "license agreement",
        "terms of use", "all rights reserved", "navbar", "stylesheet",
        "which of the following", "correct answer", "no.", "select two",
        "select three", "devops engineer", "aws codedeploy", "cloudformation",
        "exam", "question", "answer:", "option a", "option b"
    ]
    text_lower = text.lower()
    for kw in fake_keywords:
        if kw in text_lower:
            return False
    
    # gerçek CV'de olması gereken kelimeler — en az 4 eşleşmeli
    real_keywords = [
        "experience", "education", "skills", "university",
        "worked", "bachelor", "master", "degree", "graduated",
        "position", "company", "developer", "engineer",
        "manager", "intern", "gpa", "certificate", "summary"
    ]
    matches = sum(1 for kw in real_keywords if kw in text_lower)
    
    return matches >= 4
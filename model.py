import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import temizle

# veri yükle
df = pd.read_csv("resume.csv")

# temizleme
df["resume_text"] = df["resume_text"].apply(temizle)

# giriş ve çıkış
X = df["resume_text"]
y = df["category"]   # şimdilik category kullan

# vektörleştirme
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# model
model = LogisticRegression()
model.fit(X_vec, y)

print("Model hazır!")

# test fonksiyonu
def tahmin_et(cv):
    cv = temizle(cv)
    vec = vectorizer.transform([cv])
    return model.predict(vec)

# canlı test
while True:
    cv = input("CV gir (çıkmak için q): ")
    if cv == "q":
        break
    print("Tahmin:", tahmin_et(cv))
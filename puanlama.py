import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# 1. İşlenmiş veriyi oku
df = pd.read_csv(r'C:\Users\lenovo\OneDrive\Desktop\cv_dataset_islenmis.csv')

# 2. Hayali bir İş İlanı oluştur
is_ilani = "Java Fullstack Developer Spring Boot SQL Angular Javascript Agile"

# 3. TF-IDF ve Benzerlik Hesabı
vectorizer = TfidfVectorizer()
tum_metinler = df['temiz_metin'].tolist() + [is_ilani]
tfidf_matrix = vectorizer.fit_transform(tum_metinler)
benzerlik_skorlari = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

# 4. Uygunluk Skorunu Ekle
df['uygunluk_skoru'] = (benzerlik_skorlari[0] * 100).round(2)

# --- YENİ EKLENEN RİSK ANALİZİ KISMI ---
def risk_analizi(metin):
    if not isinstance(metin, str):
        return "Veri Yok"
    
    kelime_sayisi = len(metin.split())
    # Örnek kural 1: Çok kısa CV bir risktir (yetersiz bilgi)
    if kelime_sayisi < 150:
        return "Yüksek (Yetersiz Detay)"
    # Örnek kural 2: Çok uzun ama alakasız metin (karmaşıklık riski)
    elif kelime_sayisi > 1500:
        return "Orta (Gereksiz Karmaşıklık)"
    else:
        return "Düşük"

df['risk_durumu'] = df['temiz_metin'].apply(risk_analizi)
# ---------------------------------------

# 5. Sonuçları Sırala ve Kaydet
df_sirali = df.sort_values(by='uygunluk_skoru', ascending=False)

# Masaüstüne rapor olarak kaydet
df_sirali.to_csv(r'C:\Users\lenovo\OneDrive\Desktop\aday_risk_ve_puan_analizi.csv', index=False)

# 6. Görselleştirme (Grafik)
top_10 = df_sirali.head(10)
plt.figure(figsize=(12, 6))
colors = ['green' if r == 'Düşük' else 'orange' for r in top_10['risk_durumu']]

plt.barh(top_10['dosya_adi'], top_10['uygunluk_skoru'], color=colors)
plt.xlabel('Uygunluk Skoru (%)')
plt.title('En İyi 10 Aday: Uygunluk Puanı ve Risk Durumu (Yeşil=Düşük Risk)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print("\nAnaliz tamamlandı! Grafiği kapatınca tabloyu CSV olarak görebilirsin.")
print(df_sirali[['dosya_adi', 'uygunluk_skoru', 'risk_durumu']].head(10))
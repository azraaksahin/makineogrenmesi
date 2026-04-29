import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Gerekli dil paketini indir
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def temizle(metin):
    # EĞER METİN BOŞSA VEYA STRİNG DEĞİLSE (Hata veren kısım burasıydı)
    if not isinstance(metin, str):
        return ""
    
    # 1. Küçük harfe çevir
    metin = metin.lower()
    # 2. Gereksiz karakterleri ve sayıları at
    metin = re.sub(r'[^a-z\s]', '', metin)
    # 3. Gereksiz kelimeleri çıkar
    kelimeler = metin.split()
    temiz_kelimeler = [w for w in kelimeler if w not in stop_words]
    return " ".join(temiz_kelimeler)

# CSV dosyasını oku
df = pd.read_csv("data/cv_dataset_hazir.csv")

# ÖNEMLİ: Boş satırları tamamen temizle veya stringe çevir
df['cv_metni'] = df['cv_metni'].fillna('') 

# Temizleme işlemini uygula
df['temiz_metin'] = df['cv_metni'].apply(temizle)

# Boş kalan satırları temizle (Eğer metin çıkarılamayan CV varsa)
df = df[df['temiz_metin'] != ""]

# Sonucu gör
print(df[['dosya_adi', 'temiz_metin']].head())

# Kaydet
df.to_csv("data/cv_dataset_islenmis.csv", index=False)
print("İşlem başarıyla tamamlandı!")
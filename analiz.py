import pandas as pd
import re
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def temizle(metin):
  
    if not isinstance(metin, str):
        return ""
    
   
    metin = metin.lower()
    metin = re.sub(r'[^a-z\s]', '', metin)
    kelimeler = metin.split()
    temiz_kelimeler = [w for w in kelimeler if w not in stop_words]
    return " ".join(temiz_kelimeler)

# CSV dosyasını oku
df = pd.read_csv("data/cv_dataset_hazir.csv")


df['cv_metni'] = df['cv_metni'].fillna('') 

# temizleme işlemini uygula
df['temiz_metin'] = df['cv_metni'].apply(temizle)


df = df[df['temiz_metin'] != ""]

print(df[['dosya_adi', 'temiz_metin']].head())

df.to_csv("data/cv_dataset_islenmis.csv", index=False)
print("İşlem başarıyla tamamlandı!")
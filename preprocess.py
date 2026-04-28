import re

def temizle(text):
    text = str(text)          
    text = text.lower()       
    text = re.sub(r'\W', ' ', text)  
    text = re.sub(r'\s+', ' ', text) 
    return text
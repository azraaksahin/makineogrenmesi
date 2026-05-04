import requests
import os

def download_file(url, folder="data_downloaded"):
    os.makedirs(folder, exist_ok=True)

    try:
        r = requests.get(url, timeout=15)
        content_type = r.headers.get("Content-Type", "").lower()

        # dosya adı
        filename = url.split("/")[-1]

        
        if "html" in content_type:
            filename = filename.replace(".pdf", ".html")

        path = os.path.join(folder, filename)

        with open(path, "wb") as f:
            f.write(r.content)

        return path

    except Exception as e:
        print(f"Download hata: {e}")
        return None
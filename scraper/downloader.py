import requests
import os

def download_file(url, folder="data_downloaded"):
    os.makedirs(folder, exist_ok=True)

    filename = url.split("/")[-1]
    path = os.path.join(folder, filename)

    try:
        r = requests.get(url, timeout=10)
        
        # content-type kontrolü
        content_type = r.headers.get("Content-Type", "")
        if "html" in content_type or "text" in content_type:
            return None  # HTML geliyorsa atla
        
        # ilk bytes'a bak, gerçek PDF mi?
        if not r.content[:4] == b'%PDF':
            return None  # PDF magic bytes yoksa atla
            
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    except:
        return None
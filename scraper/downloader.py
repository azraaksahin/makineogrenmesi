import requests
import os

def download_file(url, folder="data_downloaded"):
    os.makedirs(folder, exist_ok=True)

    filename = url.split("/")[-1]
    path = os.path.join(folder, filename)

    try:
        r = requests.get(url)
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    except:
        return None
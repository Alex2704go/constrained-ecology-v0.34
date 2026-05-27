# download_and_save_csvs.py
import urllib.request
import os

files = {
    "v0.5.4_gauss_boundary_real_vs_jitter.csv": "1npVA5vrWNNQ3eigsbCwuu9fcWQnJh8dG",
    "v0.5.4_lorentz_boundary_real_vs_jitter.csv": "1zRfZQAGTq22L0ML8FOaNwlPCb-EvHBT0"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

os.makedirs("outputs/physics_processed", exist_ok=True)

for name, file_id in files.items():
    url = f"https://docs.google.com/uc?export=download&id={file_id}"
    req = urllib.request.Request(url, headers=headers)
    try:
        dest = os.path.join("outputs/physics_processed", name)
        print(f"Downloading {name} to {dest}...")
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
        with open(dest, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print("Error:", e)

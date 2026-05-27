# download_and_inspect_csvs.py
import urllib.request
import pandas as pd
import io

files = {
    "gauss": "1npVA5vrWNNQ3eigsbCwuu9fcWQnJh8dG",
    "lorentz": "1zRfZQAGTq22L0ML8FOaNwlPCb-EvHBT0"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for name, file_id in files.items():
    url = f"https://docs.google.com/uc?export=download&id={file_id}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"\nDownloading {name} CSV with ID {file_id}...")
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
        
        print("Success! Reading into Pandas...")
        df = pd.read_csv(io.StringIO(content))
        print(f"Shape: {df.shape}")
        print("Columns:", list(df.columns))
        print("Head:")
        print(df.head(10))
        
    except Exception as e:
        print("Error:", e)

# scrape_two_topics.py
import urllib.request
import re

topics = {
    "Topic_1": "1egdq-2rCOFJYNpsNb4bJbTn23duH75tL",
    "Topic_2": "1w3pkEn0LeK9kEL9UMyBRVTroq-gCkhGQ"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for name, folder_id in topics.items():
    url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"\nFetching HTML for {name} ({folder_id})...")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        print(f"Successfully fetched HTML for {name}.")
        
        # Save HTML
        out_name = f"raw_html_{name}.html"
        with open(out_name, "w", encoding="utf-8") as out:
            out.write(html)
        print(f"Saved to {out_name}.")
        
        # Search for any file names, folder names or titles
        # Standard folder title pattern in Google Drive: <title>Folder Name - Google Drive</title>
        title_match = re.search(r"<title>(.*?)<\/title>", html, re.IGNORECASE)
        title = title_match.group(1) if title_match else "unknown"
        print("Folder Title:", title)
        
        # Search for interesting words and callbacks
        callbacks = re.findall(r"AF_initDataCallback\s*\(\s*({.*?})\s*\)\s*;", html, re.DOTALL)
        print(f"Found {len(callbacks)} AF_initDataCallback scripts.")
        
        # Search for filenames or sheet names inside callbacks
        for idx, cb in enumerate(callbacks):
            file_names = re.findall(r'"([^"\\]+\.(?:xlsx|pdf|csv|parquet|txt|png|jpg|ipynb|zip|tar|gz))"', cb)
            if file_names:
                print(f" -> Callback {idx} contains file list: {file_names}")
                
            # Search for folder name metadata in ds:1
            if "ds:1" in cb:
                # print first few lines of ds:1 to find folder name metadata
                meta_match = re.search(r'\["[a-zA-Z0-9_-]{33}",\s*null,\s*"([^"]+)"', cb)
                if meta_match:
                    print(" -> Folder Name from Metadata:", meta_match.group(1))

    except Exception as e:
        print(f"Error on {name}: {e}")

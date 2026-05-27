# get_manifest_id.py
import urllib.request
import re

folder_id = "1b6gATBnl9q-q_JXMPXjqtTFRkaKPJscU"
url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)

try:
    print(f"Fetching folder v0.5.4_export HTML...")
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    print("Success. Searching for MANIFEST...")
    
    # Search for MANIFEST_v0.5.4.md context
    for match in re.finditer(re.escape("MANIFEST_v0.5.4.md"), html):
        start = max(0, match.start() - 600)
        end = min(len(html), match.end() + 600)
        print("\n--- CONTEXT ---")
        context = html[start:end]
        print(context)
        
        # Find 33-character IDs
        ids = re.findall(r'"([a-zA-Z0-9_-]{33})"', context)
        print("Found IDs in context:", ids)
        
except Exception as e:
    print("Error:", e)

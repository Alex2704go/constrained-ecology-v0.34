# scrape_parent.py
import urllib.request
import re

url = "https://drive.google.com/drive/folders/1kx8u8mUAOfDO9tcgl9ix83W9uoQ4ZTbr?usp=sharing"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)

try:
    print("Fetching parent folder HTML...")
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    print("Successfully fetched parent folder HTML.")
    
    # Save it
    with open("parent_phase_scans.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    # Search for "v0.34" or "NMR" or "records"
    print("\nSearching for files/subfolders in parent_phase_scans.html...")
    for word in ["v0.34", "NMR", "records"]:
        matches = list(re.finditer(re.escape(word), html, re.IGNORECASE))
        if matches:
            print(f" - '{word}': {len(matches)} matches")
            m = matches[0]
            start = max(0, m.start() - 300)
            end = min(len(html), m.end() + 300)
            print("Context:")
            print(html[start:end])
            
            # Extract 33-char IDs in the context
            ids = re.findall(r'"([a-zA-Z0-9_-]{33})"', html[start:end])
            print("Found IDs in context:", ids)
            
except Exception as e:
    print("Error:", e)

# scrape_nmr_records.py
import urllib.request
import re

url = "https://drive.google.com/drive/folders/1zC-rlxHP1w8DXTpkbwh9GdFn21p48Nf9?usp=sharing"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)

try:
    print("Fetching folder HTML...")
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    print("Successfully fetched folder HTML.")
    
    # Save it
    with open("raw_html_NMR_records.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    title_match = re.search(r"<title>(.*?)<\/title>", html, re.IGNORECASE)
    title = title_match.group(1) if title_match else "unknown"
    print("Folder Title:", title)
    
    # Search for files inside this folder
    print("\nSearching for files listed in this folder...")
    # Extensions: xlsx, pdf, csv, parquet, txt, png, jpg, md, ipynb
    extensions = [r"\.xlsx", r"\.pdf", r"\.csv", r"\.parquet", r"\.docx", r"\.txt", r"\.png", r"\.jpg", r"\.md", r"\.ipynb"]
    found_files = []
    
    for ext in extensions:
        pattern = r'[^"\\,\[\]{}()]{1,80}' + ext
        matches = re.findall(pattern, html)
        for m in matches:
            clean_name = m.strip('"\\ ')
            if clean_name not in found_files:
                found_files.append(clean_name)
                
    print(f"Found {len(found_files)} files:")
    for f in found_files:
        print(" -", f)
        
except Exception as e:
    print("Error:", e)

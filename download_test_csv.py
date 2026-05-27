# download_test_csv.py
import urllib.request

file_id = "16r-PSAooFJfklnfQz9bLXDWYazO1gRtO"
url = f"https://docs.google.com/uc?export=download&id={file_id}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)

try:
    print(f"Downloading file with ID {file_id}...")
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    print("Download successful!")
    print("\n--- CSV FILE CONTENT ---")
    print(content)
    print("------------------------")
    
except Exception as e:
    print("Error downloading:", e)

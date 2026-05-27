# search_indigo_dirac.py
import re

for name, filename in [("Topic 1 (HP35_X_comp)", "raw_html_Topic_1.html"), ("Topic 2 (indigo_dirac)", "raw_html_Topic_2.html")]:
    print(f"\n========================================\nAnalyzing {name}...\n========================================")
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Search for files listed inside the JSON arrays of the folder contents
    # Google Drive folder items have a characteristic list format:
    # ["ID", "Name", "MimeType", ...]
    # Let's find entries in quotes that are right next to folder ID, e.g. "1egdq-2rCOFJYNpsNb4bJbTn23duH75tL"
    # Let's list all strings that appear as elements in a list, especially strings with extensions.
    
    # Let's extract any words containing dots or underscores that look like files
    items = re.findall(r'"([a-zA-Z0-9_\-\s\.]+\.[a-zA-Z0-9]{2,5})"', html)
    print("Files found via regex 1:", set([i for i in items if not any(x in i.lower() for x in ["js", "css", "png", "jpg", "gif", "html", "google", "gstatic", "schema", "w3", "latenode", "community", "pcrisk", "maxcoin", "github", "drive", "apps", "roboto", "woff2", "ico"])]))
    
    # Let's also look for any string that appears in list items
    # Google Drive structure has sub-arrays, e.g., ["id", "name", "mimeType", ...]
    # Let's extract all list sequences
    lists = re.findall(r'\["[a-zA-Z0-9_-]{28,35}",\s*"([^"]+)"', html)
    print("File names from metadata pattern 2:", set(lists))
    
    # Let's search for "test_" or "indigo" or "dirac" or "comp" or "HP35" in any quoted string
    quoted = re.findall(r'"([^"\\]+)"', html)
    matching_quotes = set([q for q in quoted if any(w in q.lower() for w in ["hp35", "indigo", "dirac", "test_"])])
    print("Specific matching quotes:", matching_quotes)

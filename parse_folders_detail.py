# parse_folders_detail.py
import re

for topic in ["Topic_1", "Topic_2"]:
    print(f"\n========================================\nParsing detail for {topic}...\n========================================")
    with open(f"raw_html_{topic}.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # Search for files/folders in the Google Drive payload
    # Typically, children files are listed in an array inside a script tag
    # Let's search for entries containing standard files or identifiers
    # We can extract any strings inside double quotes that look like names of files or folders
    # Let's look for anything with dots, or uppercase names, or specific formats
    
    # In public view, let's find all matches for file names with typical endings or look at strings
    # Let's search for filenames of interest. What files are in HP35_X_comp?
    # Let's find matches for: '"[^"]+"' inside the scripts
    # Let's write a regex that extracts potential file entries.
    # Google drive initial data callback format for files:
    # ["file_id", "file_name", "mimeType", ...]
    # We can find patterns like: ["ID", "Name", ...
    matches = re.findall(r'\["[a-zA-Z0-9_-]{28,35}",\s*null,\s*"([^"]+)"', html)
    print("Folder/File names from metadata:", set(matches))
    
    # Let's search for any strings that have file extensions (case insensitive)
    ext_matches = set(re.findall(r'[^"\\,\s\[\]{}()]{1,80}\.[a-zA-Z0-9]{2,5}', html))
    # Filter out static JS/CSS assets or web domains
    clean_ext = [e for e in ext_matches if not any(x in e.lower() for x in ["js", "css", "png", "jpg", "gif", "html", "google", "gstatic", "schema", "w3", "latenode", "community", "pcrisk", "maxcoin", "github", "drive", "apps"])]
    print("Other files found with extensions:", clean_ext)
    
    # Let's search for any other files in ds:3 or other callbacks
    callbacks = re.findall(r"AF_initDataCallback\s*\(\s*({.*?})\s*\)\s*;", html, re.DOTALL)
    for i, cb in enumerate(callbacks):
        # Find any text that looks like a file/folder name
        # Let's search for strings in quotes
        quoted = re.findall(r'"([^"\\]+)"', cb)
        # Find any names containing specific words like "HP35" or "indigo" or "dirac" or "test"
        matches_specific = [q for q in quoted if any(w in q.lower() for w in ["hp35", "indigo", "dirac", "test", "comp", "xlsx", "csv", "pdf", "txt", "dat"])]
        if matches_specific:
            print(f" -> Callback {i} specific matches: {set(matches_specific)}")
            
        # Let's write a quick loop to print all strings of length between 5 and 60 inside quotes in this callback
        # to find if there are hidden filenames
        long_quotes = [q for q in quoted if 5 <= len(q) <= 60 and not any(x in q.lower() for x in ["http", "google", "drive", "application", "image", "logo", "icon", "theme", "class", "font", "style", "web"])]
        if len(long_quotes) > 0 and len(long_quotes) < 20:
            print(f" -> Callback {i} other quoted strings: {set(long_quotes)}")

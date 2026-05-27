# find_nmr_records_folder.py
import os
import re

fname = "folder_source.html"
if os.path.exists(fname):
    with open(fname, "r", encoding="utf-8") as f:
        html = f.read()

    print("Searching for 'v0.34' or 'NMR' in folder_source.html...")
    # Search for "v0.34" or "NMR" or "records"
    for word in ["v0.34", "NMR", "records", "villin", "HP35"]:
        matches = list(re.finditer(re.escape(word), html, re.IGNORECASE))
        if matches:
            print(f"\nFound {len(matches)} matches for '{word}'!")
            m = matches[0]
            start = max(0, m.start() - 250)
            end = min(len(html), m.end() + 250)
            print("Context:")
            print(html[start:end])
            
            # Extract 33-char IDs in the context
            ids = re.findall(r'"([a-zA-Z0-9_-]{33})"', html[start:end])
            print("Found IDs in context:", ids)

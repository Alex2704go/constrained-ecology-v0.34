# list_all_parent_ids.py
import re

with open("parent_phase_scans.html", "r", encoding="utf-8") as f:
    html = f.read()

# Regular expression to extract typical 33-character Google Drive IDs
# Let's extract any 33-char ID
ids = set(re.findall(r'"([a-zA-Z0-9_-]{33})"', html))
print(f"Found {len(ids)} unique 33-character IDs in parent_phase_scans.html:")
for iid in sorted(ids):
    print(" -", iid)
    
# Let's search for any strings that look like folder/file names or words
print("\nSearching for any quoted words that look like filenames or subfolders:")
quoted = set(re.findall(r'"([^"\\]{4,60})"', html))
suspicious = [q for q in quoted if any(x in q.lower() for x in ["v0.", "v1.", "phase", "scan", "uru", "bili", "nickel", "la3", "la4", "graphene", "nmr", "record", "af2", "sidechain", "x6b"])]
for s in sorted(suspicious):
    print(" -", s)

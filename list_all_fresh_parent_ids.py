# list_all_fresh_parent_ids.py
import re

with open("parent_phase_scans_fresh.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract any 33-character Google Drive IDs
ids = set(re.findall(r'"([a-zA-Z0-9_-]{33})"', html))
print(f"Found {len(ids)} unique 33-character IDs in parent_phase_scans_fresh.html:")

# Search for any quoted words that look like folder/file names
quoted = set(re.findall(r'"([^"\\]{4,60})"', html))
print("\nUnique folder/file names in parent_phase_scans_fresh.html:")
for q in sorted(quoted):
    if any(x in q.lower() for x in ["v0.", "v1.", "phase", "scan", "uru", "bili", "nickel", "la3", "la4", "graphene", "nmr", "record", "af2", "sidechain", "x6b"]):
        print(" -", q)

# find_file_id.py
import re

with open("raw_html_Topic_1.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for "test_66cd0.csv" and look around it for a 33-char ID
# Usually, folder items appear as an array where the ID is first, then the name:
# e.g., ["id", "test_66cd0.csv", ...] or similar
# Let's search for any matches and print the preceding 500 characters and succeeding 500 characters
print("Searching for 'test_66cd0.csv' contexts...")
for match in re.finditer(re.escape("test_66cd0.csv"), html):
    start = max(0, match.start() - 600)
    end = min(len(html), match.end() + 600)
    print("\n--- CONTEXT ---")
    context = html[start:end]
    print(context)
    
    # Try finding typical 33-character Google Drive IDs inside this context using regex
    ids = re.findall(r'"([a-zA-Z0-9_-]{33})"', context)
    print("Found IDs in this context:", ids)

import urllib.request
import re

SOURCE_URL = "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u"
OUTPUT_FILE = "otv-clean.m3u"

ALLOWED_GROUPS = {
    "INDIAN | MUSIC",
    "INDIAN | 4K ULTRA HD",
    "INDIAN | SPORTS 4K (ULTRA HD)",
    "INDIAN | ENTERTAINMENT",
    "INDIAN | MOVIES",
    "INDIAN | ENGLISH MOVIES",
    "INDIAN | D2H ACTIVE"
}

req = urllib.request.Request(
    SOURCE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=120) as response:
    content = response.read().decode("utf-8", errors="ignore")

lines = content.splitlines()

output = []
current_entry = []
current_allowed = False

for line in lines:

    if line.startswith("#EXTINF"):
        # Save previous channel
        if current_entry and current_allowed:
            output.extend(current_entry)

        # Start new channel
        current_entry = [line]
        current_allowed = False

        match = re.search(r'group-title="([^"]*)"', line)

        if match:
            group = match.group(1).strip()

            if group in ALLOWED_GROUPS:
                current_allowed = True

    elif line.startswith("#EXTVLCOPT"):
        if current_entry:
            current_entry.append(line)

    elif line.startswith("#KODIPROP"):
        if current_entry:
            current_entry.append(line)

    elif line.strip() and not line.startswith("#"):
        if current_entry:
            current_entry.append(line)

    elif line.startswith("#"):
        if current_entry:
            current_entry.append(line)

# Save final channel
if current_entry and current_allowed:
    output.extend(current_entry)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output) + "\n")

print("Clean playlist updated successfully.")
print("Allowed groups:")

for group in sorted(ALLOWED_GROUPS):
    print(" - " + group)
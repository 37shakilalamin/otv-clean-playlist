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
    "INDIAN | D2H ACTIVE",
}

# Download the original playlist
request = urllib.request.Request(
    SOURCE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=120) as response:
    content = response.read().decode("utf-8", errors="ignore")

lines = content.splitlines()

output = ["#EXTM3U"]
current_entry = []
current_group = None
kept_channels = 0
skipped_channels = 0


def save_current_entry():
    global kept_channels, skipped_channels

    if not current_entry:
        return

    if current_group in ALLOWED_GROUPS:
        output.extend(current_entry)
        kept_channels += 1
    else:
        skipped_channels += 1


for line in lines:
    line = line.rstrip("\r")

    # Start of a new channel
    if line.startswith("#EXTINF"):
        save_current_entry()

        current_entry = [line]
        current_group = None

        # Read group-title
        match = re.search(r'group-title\s*=\s*"([^"]*)"', line, re.IGNORECASE)

        if match:
            current_group = match.group(1).strip()

    else:
        # Add all lines belonging to the current channel
        if current_entry:
            current_entry.append(line)

# Save the last channel
save_current_entry()

# Write the filtered playlist
with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as file:
    file.write("\n".join(output))
    file.write("\n")

print("========================================")
print("Clean playlist updated successfully")
print("========================================")
print(f"Kept channels   : {kept_channels}")
print(f"Skipped channels: {skipped_channels}")
print(f"Output file     : {OUTPUT_FILE}")
print("")
print("Allowed groups:")
for group in sorted(ALLOWED_GROUPS):
    print(f" - {group}")
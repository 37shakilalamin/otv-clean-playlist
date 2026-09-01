import re
import urllib.request

SOURCE_URL = "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u"
OUTPUT_FILE = "otv-clean.m3u"

BLOCKED_WORDS = [
    "adult",
    "xxx",
    "porn",
    "18+",
    "18 plus",
    "18plus",
    "sex",
    "erotic",
    "playboy",
    "blue",
    "uncensored"
]

def is_blocked(line):
    text = line.lower()
    return any(word in text for word in BLOCKED_WORDS)

req = urllib.request.Request(
    SOURCE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=60) as response:
    content = response.read().decode("utf-8", errors="ignore")

lines = content.splitlines()
output = []
skip_next = False

for line in lines:
    if line.startswith("#EXTINF"):
        skip_next = is_blocked(line)

    if skip_next:
        continue

    output.append(line)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output) + "\n")

print(f"Created {OUTPUT_FILE}")
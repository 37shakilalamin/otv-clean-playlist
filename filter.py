import urllib.request

SOURCE_URL = "https://raw.githubusercontent.com/johirxofficial/otv-auto-updated-playlist/main/otv.m3u"
OUTPUT_FILE = "otv-clean.m3u"

BLOCKED_WORDS = [
    "adult",
    "xxx",
    "porn",
    "porno",
    "18+",
    "18 plus",
    "18plus",
    "sex",
    "erotic",
    "erotica",
    "playboy",
    "brazzers",
    "redtube",
    "xvideos",
    "xnxx",
    "onlyfans",
    "hustler",
    "penthouse",
    "private",
    "babes",
    "naughty",
    "milf",
    "fetish",
    "anal",
    "lesbian",
    "gay porn",
    "hardcore",
    "softcore",
    "uncensored"
]

def is_blocked(text):
    text = text.lower()
    return any(word in text for word in BLOCKED_WORDS)

# Download original playlist
req = urllib.request.Request(
    SOURCE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=120) as response:
    content = response.read().decode("utf-8", errors="ignore")

lines = content.splitlines()

output = []
i = 0
blocked_count = 0

while i < len(lines):
    line = lines[i].strip()

    # Keep playlist header
    if line.startswith("#EXTM3U"):
        output.append(line)
        i += 1
        continue

    # Process channel entry
    if line.startswith("#EXTINF"):
        extinf_line = line
        url_line = ""

        # Find the channel URL
        j = i + 1
        extra_lines = []

        while j < len(lines):
            next_line = lines[j].strip()

            if next_line.startswith("#EXTINF"):
                break

            extra_lines.append(next_line)

            if next_line and not next_line.startswith("#"):
                url_line = next_line
                break

            j += 1

        # Check EXTINF metadata + URL
        full_text = extinf_line + " " + url_line

        if is_blocked(full_text):
            blocked_count += 1
        else:
            output.append(extinf_line)

            for extra in extra_lines:
                if extra:
                    output.append(extra)

        i = j + 1
        continue

    i += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output) + "\n")

print(f"Created {OUTPUT_FILE}")
print(f"Blocked {blocked_count} adult channels")
print(f"Remaining lines: {len(output)}")
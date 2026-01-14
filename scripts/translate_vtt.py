import sys
import subprocess
import json
import urllib.parse

auth_key = "52309bee-147b-4575-8ab7-6309fb9608a0"

# Read the VTT file
with open(sys.argv[1], "r") as f:
    content = f.read()

# Parse VTT
lines = content.split("\n")
# Find start of cues
start = 0
for i, line in enumerate(lines):
    if "-->" in line:
        start = i
        break

header = lines[:start]
cues = []
current_cue = None
for line in lines[start:]:
    if "-->" in line:
        if current_cue:
            cues.append(current_cue)
        current_cue = {"time": line, "text": []}
    elif current_cue and line.strip():
        current_cue["text"].append(line.strip())
if current_cue:
    cues.append(current_cue)

# Collect all texts
texts = []
cue_indices = []
for i, cue in enumerate(cues):
    text = "\n".join(cue["text"])
    if text:
        texts.append(text)
        cue_indices.append(i)

# Translate in batches respecting size limit
max_size = 120 * 1024  # 120 KiB
translated_texts = []
i = 0
while i < len(texts):
    batch = []
    data_parts = [f"auth_key={auth_key}&target_lang=HE"]
    current_size = len("&".join(data_parts).encode())
    while i < len(texts):
        t = texts[i]
        new_part = f"text={urllib.parse.quote(t)}"
        temp_data = "&".join(data_parts + [new_part])
        new_size = len(temp_data.encode())
        if new_size > max_size:
            break
        batch.append(t)
        data_parts.append(new_part)
        current_size = new_size
        i += 1
    if batch:
        data = "&".join(data_parts)
        cmd = [
            "curl",
            "-s",
            "-X",
            "POST",
            "https://api.deepl.com/v2/translate",
            "-H",
            "Content-Type: application/x-www-form-urlencoded",
            "-d",
            data,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                for trans in response["translations"]:
                    translated_texts.append(trans["text"])
            except Exception as e:
                print(f"Error parsing batch: {e}")
                translated_texts.extend([""] * len(batch))
        else:
            print(f"Error in batch: {result.stderr}")
            translated_texts.extend([""] * len(batch))
    else:
        # If even one text is too big, skip
        i += 1

# Assign back
translated_cues = []
trans_idx = 0
for i, cue in enumerate(cues):
    if i in cue_indices:
        translated_text = translated_texts[trans_idx]
        trans_idx += 1
        translated_cues.append(
            {"time": cue["time"], "text": translated_text.split("\n")}
        )
    else:
        translated_cues.append({"time": cue["time"], "text": []})

# Reconstruct VTT
output_lines = header + [""]
for cue in translated_cues:
    output_lines.append(cue["time"])
    for t in cue["text"]:
        output_lines.append(t)
    output_lines.append("")

output = "\n".join(output_lines)

# Write to output file
with open(sys.argv[2], "w") as f:
    f.write(output)

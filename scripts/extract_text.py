import os
import re
import logging
from tqdm import tqdm

logging.basicConfig(
    filename="logs/extract.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def extract_text_from_vtt(vtt_file):
    with open(vtt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text_lines = []
    in_cue = False
    for line in lines:
        line = line.strip()
        if "-->" in line:
            in_cue = True
        elif line == "":
            in_cue = False
        elif in_cue and line:
            text_lines.append(line)
    return " ".join(text_lines)


# Combine all .en.vtt in channel dir
channel_dir = "Thinking According to Alan Watts"
english_subs = []

logging.info("Starting text extraction from VTT files")

vtt_files = [f for f in os.listdir(channel_dir) if f.endswith(".en.vtt")]
for file in tqdm(vtt_files, desc="Extracting text from VTT files"):
    full_path = os.path.join(channel_dir, file)
    logging.info(f"Processing {full_path}")
    text = extract_text_from_vtt(full_path)
    english_subs.append(text)

combined_text = "\n\n".join(english_subs)

with open("data/english_subs.txt", "w", encoding="utf-8") as f:
    f.write(combined_text)

logging.info("Text extraction completed")

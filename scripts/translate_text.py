import deepl
import nltk
import sqlite3
import hashlib
import time
import os
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

# Download punkt if needed
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

auth_key = os.getenv("DEEPL_API_KEY")
if not auth_key:
    raise ValueError("DEEPL_API_KEY environment variable not set")
translator = deepl.Translator(auth_key)

input_file = "data/english_subs.txt"
output_file = "data/english_translated_hebrew.txt"

# Setup cache
cache_db = "data/translation_cache.db"
conn = sqlite3.connect(cache_db)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS translations (hash TEXT PRIMARY KEY, translation TEXT)"""
)
conn.commit()


def get_cached_translation(chunk):
    chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
    c.execute("SELECT translation FROM translations WHERE hash=?", (chunk_hash,))
    result = c.fetchone()
    return result[0] if result else None


def cache_translation(chunk, translation):
    chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
    c.execute(
        "INSERT OR REPLACE INTO translations (hash, translation) VALUES (?, ?)",
        (chunk_hash, translation),
    )
    conn.commit()


with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Tokenize into sentences
sentences = sent_tokenize(text)

# Group sentences into chunks of ~4000 characters
chunks = []
current_chunk = ""
for sentence in sentences:
    if len(current_chunk) + len(sentence) + 1 > 4000:  # +1 for space
        if current_chunk:
            chunks.append(current_chunk)
        current_chunk = sentence
    else:
        if current_chunk:
            current_chunk += " " + sentence
        else:
            current_chunk = sentence

if current_chunk:
    chunks.append(current_chunk)

translated_chunks = []
for chunk in tqdm(chunks, desc="Translating chunks"):
    cached = get_cached_translation(chunk)
    if cached:
        translated_chunks.append(cached)
        print("Using cached translation")
    else:
        try:
            result = translator.translate_text(chunk, target_lang="HE")
            if isinstance(result, list):
                translation = result[0].text
            else:
                translation = result.text
            translated_chunks.append(translation)
            cache_translation(chunk, translation)
        except Exception as e:
            print(f"Error translating chunk: {e}")
            translated_chunks.append(chunk)  # Keep original if error
        time.sleep(1)  # Rate limiting to avoid API blocks

combined_translated = " ".join(translated_chunks)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(combined_translated)

conn.close()

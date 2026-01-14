import streamlit as st
import subprocess
import os

st.title("yt-knowledge GUI")

st.header("Configuration")
channel_url = st.text_input(
    "YouTube Channel URL", "https://www.youtube.com/@ThinkingAccordingToAlanWatts"
)
batch_size = st.slider("Batch Size", 1, 10, 5)
use_translation = st.checkbox("Enable Translation", value=False)
deepl_key = st.text_input("DeepL API Key", type="password") if use_translation else ""

st.header("Actions")

if st.button("Download Subtitles"):
    with st.spinner("Downloading subtitles..."):
        result = subprocess.run(
            ["bash", "scripts/download_subs.sh"], capture_output=True, text=True
        )
        st.text_area("Download Output", result.stdout + result.stderr, height=200)

if st.button("Extract Text"):
    with st.spinner("Extracting text..."):
        result = subprocess.run(
            ["python3", "scripts/extract_text.py"], capture_output=True, text=True
        )
        st.text_area("Extract Output", result.stdout + result.stderr, height=200)

if use_translation and st.button("Translate Text"):
    # Set environment variable for key if needed
    env = os.environ.copy()
    if deepl_key:
        env["DEEPL_KEY"] = deepl_key
    with st.spinner("Translating text..."):
        result = subprocess.run(
            ["python3", "scripts/translate_text.py"],
            capture_output=True,
            text=True,
            env=env,
        )
        st.text_area("Translate Output", result.stdout + result.stderr, height=200)

st.header("Files")
if st.button("List Downloaded Subtitles"):
    try:
        channel_dir = "Thinking According to Alan Watts"
        files = os.listdir(channel_dir)
        st.write(files)
    except:
        st.write("No files found")

if st.button("View Combined Text"):
    try:
        with open("data/english_subs.txt", "r") as f:
            text = f.read()
        st.text_area(
            "Combined English Text",
            text[:1000] + "..." if len(text) > 1000 else text,
            height=300,
        )
    except:
        st.write("File not found")

st.header("Search")
search_query = st.text_input("Search Query")
if st.button("Search Text"):
    if search_query:
        result = subprocess.run(
            ["python3", "scripts/search.py", search_query],
            capture_output=True,
            text=True,
        )
        st.text_area("Search Results", result.stdout + result.stderr, height=300)
    else:
        st.write("Enter a search query")

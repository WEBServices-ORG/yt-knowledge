# yt-knowledge Project

## Disclaimer

This tool is provided for personal and educational use only. Users must comply with YouTube's Terms of Service and all applicable laws. Automated downloading of content may violate YouTube's policies. The authors are not responsible for misuse. Do not redistribute copyrighted content.

## Overview

The yt-knowledge project is an open-source research tool for automated extraction, linguistic analysis, and multilingual processing of YouTube subtitle content. It enables researchers to build comprehensive text corpora from video platforms, supporting studies in natural language processing, content analysis, cross-cultural communication, and digital humanities.

Key research applications:
- **Corpus Linguistics**: Create large-scale text datasets from multimedia content
- **Multilingual Studies**: Analyze translation quality and cultural adaptation
- **Content Analysis**: Study thematic patterns and discourse in online media
- **Educational Technology**: Develop tools for language learning and accessibility

This project was initially developed for analyzing philosophical content from the "Thinking According to Alan Watts" channel, but can be extended to other channels and platforms. It provides a framework for ethical, compliant research on digital media content.

## About webservices-org

Learn more about our research initiatives at [webservicesdev.com](https://webservicesdev.com)

## Donations

If you find yt-knowledge helpful for your research, consider supporting development:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/webservices-org)

Or donate via PayPal: [paypal.me/webservices-org](https://paypal.me/webservices-org)

## Project Structure

- `scripts/`: Contains Python and Bash scripts for downloading, extracting, and translating subtitles.
- `data/`: Contains output data files, including combined English text and translated Hebrew text.
- Channel-named directories (e.g., "Thinking According to Alan Watts"): Contain individual downloaded subtitle files (.vtt), video files (.mp4), and audio files (.webm) organized by channel.

## Requirements

### System Requirements
- Python 3.8 or higher
- Bash shell
- Internet connection for downloads and API calls

### Dependencies
- yt-dlp: For YouTube subtitle downloading
- deepl: For translation services (`pip install deepl`)
- streamlit: For GUI (`pip install streamlit`)
- nltk: For text processing (`pip install nltk`)
- transformers: For AI summarization (`pip install transformers torch`)
- reportlab: For PDF export (`pip install reportlab`)
- ebooklib: For EPUB export (`pip install ebooklib`)
- scikit-learn: For text comparison (`pip install scikit-learn`)
- sqlite3: For caching (built-in)
- fastapi: For REST API (`pip install fastapi uvicorn`)
- sphinx: For documentation generation (`pip install sphinx`)
- mlx-whisper: For audio transcription on macOS (`pip install mlx-whisper`)
- tqdm: For progress bars (`pip install tqdm`)
- deno: Required by yt-dlp for some operations

### API Keys and Authentication
- DeepL API key (from https://www.deepl.com/pro-api)
- YouTube cookies in Netscape format (exported from logged-in browser)

## Setup

1. Install dependencies:
   ```
   pip install deepl
   ```

2. Obtain a DeepL API key from https://www.deepl.com/pro-api. Set it as an environment variable: `export DEEPL_API_KEY=your_key_here`

3. Export cookies from your browser (logged into YouTube) in Netscape format. Save as `cookies.txt` in the project directory.
   - Use extensions like "Get cookies.txt" or "ExportCookies".

4. Clone or ensure yt-dlp is installed.

## Usage

### Step-by-Step Guide

1. **Prepare Authentication**
   - Export YouTube cookies from your browser in Netscape format
   - Save as `data/cookies.txt`
   - Ensure cookies are fresh (export after logging into YouTube)

2. **Download Subtitles**
   ```
   bash scripts/download_subs.sh
   ```
   This downloads English (and Hebrew if available) subtitles for all videos in the configured channel. The script resumes from previous runs and downloads in batches to avoid timeouts.

3. **Extract and Combine Text**
   ```
   python3 scripts/extract_text.py
   ```
   Extracts plain text from all downloaded VTT files and combines them into a single document at `data/english_subs.txt`.

4. **Translate Text (Optional)**
   ```
   python3 scripts/translate_text.py
   ```
   Translates the combined English text to Hebrew using DeepL API, saving the result as `data/english_translated_hebrew.txt`. Due to API limits, large texts are processed in chunks.

### Configuration

- Edit `scripts/download_subs.sh` to change the channel URL, batch size, or enable media download (set DOWNLOAD_MEDIA=1)
- Update API key in translation scripts if needed
- Modify cookie path if stored elsewhere

### Examples

- To download from a different channel, change the `channel_url` in `download_subs.sh`
- To process only specific videos, modify the script to accept video ID lists

### Summarization
```
python3 scripts/summarize.py [input_file] [output_file]
```
Generates an AI summary of the text.

### Export
```
python3 scripts/export.py <format> [input_file] [output_file]
```
Exports text to PDF, EPUB, or Markdown. Formats: pdf, epub, markdown.

### API Mode
For remote access, run the FastAPI server:
```
uvicorn api:app --reload
```
Access the API documentation at http://localhost:8000/docs

### GUI Mode
For a user-friendly interface, run the Streamlit app:
```
streamlit run app.py
```
This opens a web browser where you can configure and execute tasks without command line.

## Scripts

- `api.py`: FastAPI REST API for remote access.
- `app.py`: Streamlit GUI for easy configuration and execution.
- `download_subs.sh`: Downloads subtitles from the channel, with fallback to transcription.
- `extract_text.py`: Extracts text from VTT files.
- `translate_text.py`: Translates text using DeepL with smart chunking and caching.
- `translate_vtt.py`: Translates individual VTT files (used for original video).
- `search.py`: Provides full-text search capabilities on combined text files.
- `summarize.py`: Generates AI-powered summaries of text files.
- `export.py`: Exports text to PDF, EPUB, or Markdown formats.
- `transcribe.py`: Transcribes audio to text using MLX Whisper.

## Data Files

- `english_subs.txt`: Combined English text from subtitles.
- `english_translated_hebrew.txt`: Translated Hebrew text.
- `he.vtt`: Translated Hebrew subtitles for the original video.
- `cookies.txt`: Browser cookies for authentication.

## Best Practices

### API and Rate Limits
- DeepL API has monthly limits; monitor usage on their dashboard
- YouTube may temporarily block IPs; use VPN if needed
- Run downloads in off-peak hours to avoid congestion

### Data Management
- Always backup important data before processing
- Keep original subtitle files for reference
- Use version control for scripts and configurations

## Rules

- Rule: Always download all available English subtitles from channel videos.
- Rule: Subtitle file names should match the video title for easy identification.
- Rule: Add '_he' suffix to Hebrew subtitle file names for distinction (e.g., video_title_he.vtt).
- Rule: Support both SRT and VTT subtitle formats; prefer VTT, but download SRT if VTT unavailable.
- Rule: Do not stop until all subtitles are fetched. If there's a problem, notify the user.
- Rule: Use MCP or web agent if needed for additional data fetching or processing.
- Rule: If no subtitles available, transcribe to English using OpenAI Whisper. Preferred model: Whisper Large v3 or Turbo. On macOS, always prefer MLX models for better performance.
- Rule: When English subs/transcription is ready, translate to Hebrew with DeepL API.
- Rule: Always show progress and status during operations.
- Rule: Always notify the total number of videos in the channel.
- Rule: Always notify the channel subscribers number.
- Rule: When finished with video/audio transcription, delete the file to save space.
- YouTube may block downloads due to bot detection; use fresh cookies.
- Not all videos may have subtitles; only available ones are downloaded.
- Translation accuracy depends on subtitle quality and API performance.

## Troubleshooting

- If downloads fail, refresh cookies.
- For translation errors, check API key and network.
- Run scripts individually if issues arise.
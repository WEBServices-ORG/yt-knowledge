import pytest
import os
import tempfile
from scripts.extract_text import extract_text_from_vtt


def test_extract_text_from_vtt():
    vtt_content = """WEBVTT

00:00:01.000 --> 00:00:04.000
This is a test subtitle.

00:00:05.000 --> 00:00:08.000
Another line of text.
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".vtt", delete=False) as f:
        f.write(vtt_content)
        temp_file = f.name

    try:
        extracted = extract_text_from_vtt(temp_file)
        expected = "This is a test subtitle. Another line of text."
        assert extracted.strip() == expected
    finally:
        os.unlink(temp_file)

#!/usr/bin/env python3
"""
Transcribe MP4 file to Hebrew using MLX Whisper Large V3
"""

import os
import sys
import subprocess
from pathlib import Path


def extract_audio(mp4_file, audio_file, duration_minutes=None):
    """Extract audio from MP4 file using ffmpeg"""
    cmd = [
        "ffmpeg",
        "-i",
        mp4_file,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
    ]

    # Only add time limit if duration_minutes is specified
    if duration_minutes is not None:
        cmd.extend(["-t", str(duration_minutes * 60)])  # Convert minutes to seconds
        duration_text = f"first {duration_minutes} minutes"
    else:
        duration_text = "full"

    cmd.extend([audio_file, "-y"])
    print(f"Extracting {duration_text} of audio from {mp4_file}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error extracting audio: {result.stderr}")
        return False
    return True


def transcribe_audio(audio_file, output_file):
    """Transcribe audio using MLX Whisper models"""
    import mlx_whisper

    print("Attempting MLX Whisper transcription...")

    # Try different MLX models in order of preference
    models_to_try = [
        "mlx-community/whisper-large-v3-turbo-4bit",
        "mlx-community/whisper-medium-4bit",
        "mlx-community/whisper-base-4bit",
    ]

    for model_name in models_to_try:
        try:
            print(f"Trying MLX model: {model_name}")
            result = mlx_whisper.transcribe(
                audio_file, path_or_hf_repo=model_name, language="he", verbose=True
            )

            # Save transcription
            text = str(result["text"])
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ MLX transcription successful with {model_name}")
            print(f"Transcription saved to {output_file}")
            return result

        except Exception as e:
            print(f"❌ MLX model {model_name} failed: {e}")
            continue

    # If all MLX models fail, fallback to OpenAI whisper
    print("All MLX models failed, falling back to OpenAI whisper...")
    import whisper

    print("Loading medium model for high-quality Hebrew transcription...")
    model = whisper.load_model("medium")  # Use medium for best quality
    print("Starting full transcription (this may take 30-60 minutes)...")
    result = model.transcribe(audio_file, language="he", verbose=True, fp16=False)
    text = str(result["text"])
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Full transcription completed and saved to {output_file}")
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <mp4_file>")
        sys.exit(1)

    mp4_file = sys.argv[1]
    if not os.path.exists(mp4_file):
        print(f"File not found: {mp4_file}")
        sys.exit(1)

    # Setup file paths
    base_name = Path(mp4_file).stem
    audio_file = f"{base_name}_audio.wav"
    output_file = f"{base_name}_transcription_he.txt"

    try:
        # Extract full audio (no time limit)
        if not extract_audio(mp4_file, audio_file):
            sys.exit(1)

        # Transcribe
        result = transcribe_audio(audio_file, output_file)

        print("\nTranscription completed!")
        print(f"Text: {result['text'][:200]}...")

        # Clean up audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Cleaned up temporary audio file: {audio_file}")

    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

import mlx_whisper
import sys
import os


def transcribe_audio(
    audio_file, output_file=None, model="mlx-community/whisper-large-v3"
):
    if not os.path.exists(audio_file):
        print(f"Audio file {audio_file} not found.")
        return

    print(f"Transcribing {audio_file} with {model}...")
    result = mlx_whisper.transcribe(audio_file, path_or_hf_repo=model)

    transcription = result["text"]

    if output_file is None:
        output_file = audio_file.replace(".webm", ".txt").replace(".mp3", ".txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcription)

    print(f"Transcription saved to {output_file}")
    return transcription


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <audio_file> [output_file]")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    transcribe_audio(audio_file, output_file)

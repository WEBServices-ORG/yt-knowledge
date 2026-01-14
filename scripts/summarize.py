import sys
from transformers import pipeline


def summarize_text(
    input_file="data/english_subs.txt",
    output_file="data/summary.txt",
    max_length=150,
    min_length=50,
):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("Input file not found.")
        return

    # Initialize summarizer
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    # Summarize in chunks if text is too long
    chunk_size = 1024  # Model limit
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []
    for chunk in chunks:
        if len(chunk.strip()) > 10:  # Skip very short chunks
            summary = summarizer(
                chunk, max_length=max_length, min_length=min_length, do_sample=False
            )
            summaries.append(summary[0]["summary_text"])

    combined_summary = " ".join(summaries)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_summary)

    print(f"Summary saved to {output_file}")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/english_subs.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/summary.txt"
    summarize_text(input_file, output_file)

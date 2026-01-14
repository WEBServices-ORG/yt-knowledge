import sys
import re
from collections import defaultdict


def search_text(query, file_path="data/english_subs.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("Text file not found. Run extract_text.py first.")
        return

    # Split into sections (assuming separated by \n\n)
    sections = text.split("\n\n")

    results = []
    for i, section in enumerate(sections):
        if query.lower() in section.lower():
            # Find context
            lines = section.split("\n")
            for j, line in enumerate(lines):
                if query.lower() in line.lower():
                    start = max(0, j - 2)
                    end = min(len(lines), j + 3)
                    context = "\n".join(lines[start:end])
                    results.append(f"Section {i + 1}, Line {j + 1}:\n{context}\n---")

    if results:
        print(f"Found {len(results)} matches for '{query}':")
        for result in results:
            print(result)
    else:
        print(f"No matches found for '{query}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search.py <query>")
        sys.exit(1)
    query = sys.argv[1]
    search_text(query)

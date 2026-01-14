import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from ebooklib import epub


def export_to_pdf(text, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    y = height - 50
    for line in text.split("\n"):
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(50, y, line[:80])  # Truncate long lines
        y -= 15
    c.save()


def export_to_epub(text, output_file, title="yt-knowledge Export"):
    book = epub.EpubBook()
    book.set_identifier("yt-knowledge")
    book.set_title(title)
    book.set_language("en")

    chapter = epub.EpubHtml(title="Content", file_name="chap_01.xhtml", lang="en")
    chapter.content = f"<h1>{title}</h1><p>" + text.replace("\n", "</p><p>") + "</p>"

    book.add_item(chapter)
    book.toc = (epub.Link("chap_01.xhtml", "Content", "content"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ["nav", chapter]
    epub.write_epub(output_file, book, {})


def export_to_markdown(text, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# yt-knowledge Export\n\n" + text)


def export_file(
    input_file="data/english_subs.txt", format="markdown", output_file=None
):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("Input file not found.")
        return

    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}.{format}"

    if format.lower() == "pdf":
        export_to_pdf(text, output_file)
    elif format.lower() == "epub":
        export_to_epub(text, output_file)
    elif format.lower() == "markdown":
        export_to_markdown(text, output_file)
    else:
        print("Unsupported format. Use pdf, epub, or markdown.")

    print(f"Exported to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 export.py <format> [input_file] [output_file]")
        print("Formats: pdf, epub, markdown")
        sys.exit(1)

    format = sys.argv[1]
    input_file = sys.argv[2] if len(sys.argv) > 2 else "data/english_subs.txt"
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    export_file(input_file, format, output_file)

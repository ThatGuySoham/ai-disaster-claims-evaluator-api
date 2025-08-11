def parse_doc(content: bytes):
    """
    A very basic document parser.
    In real life, you'd use PyPDF2 or python-docx.
    Here, we just decode to text and split into chunks.
    """
    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    if not text.strip():
        return []
    chunk_size = 500
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

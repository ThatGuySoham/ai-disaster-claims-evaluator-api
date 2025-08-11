def parse_doc(content: bytes):
    """
    Minimal placeholder parser:
    - tries to decode bytes to text and chunk it
    - real parser should extract text from PDF/DOCX properly
    """
    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    if not text:
        return ["[binary content - no text extracted]"]
    chunk_size = 2000
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
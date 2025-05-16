from enum import Enum
from pathlib import Path

class DocumentType(str, Enum):
    pdf = "pdf"
    csv = "csv"
    excel = "excel"
    word = "word"
    text = "text"
    markdown = "markdown"
    unknown = "unknown"

ext_to_type = {
    "pdf": DocumentType.pdf,
    "csv": DocumentType.csv,
    "xlsx": DocumentType.excel,
    "xls": DocumentType.excel,
    "docx": DocumentType.word,
    "txt": DocumentType.text,
    "md": DocumentType.markdown,
}

def get_file_type(file_path: str) -> DocumentType:
    ext = Path(file_path).suffix[1:].lower()
    return ext_to_type.get(ext, DocumentType.unknown)
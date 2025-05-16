import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader, CSVLoader, TextLoader,
    UnstructuredExcelLoader, UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
)

from .common import DocumentType, get_file_type  # enum + 판별함수 필요


def load_documents_from_folder(folder_path: str) -> List[Document]:
    all_docs: List[Document] = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if not os.path.isfile(file_path):
            continue

        file_type = get_file_type(file_path)  # 자동 추론

        try:
            if file_type == DocumentType.pdf:
                loader = PyPDFLoader(file_path)
            elif file_type == DocumentType.csv:
                loader = CSVLoader(file_path, encoding="utf-8", autodetect_encoding=True)
            elif file_type == DocumentType.text:
                loader = TextLoader(file_path, encoding="utf-8")
            elif file_type == DocumentType.word:
                loader = UnstructuredWordDocumentLoader(file_path)
            elif file_type == DocumentType.markdown:
                loader = UnstructuredMarkdownLoader(file_path)
            elif file_type == DocumentType.excel:
                loader = UnstructuredExcelLoader(file_path)
            else:
                print(f"❌ 지원하지 않는 형식: {file}")
                continue

            docs = loader.load()
            all_docs.extend(docs)

        except Exception as e:
            print(f"⚠️ 파일 {file} 로드 실패: {e}")
    return all_docs
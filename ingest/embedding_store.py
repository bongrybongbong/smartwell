from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def build_vectorstore(docs: List[Document], save_path: str = "faiss_index"):
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embedding)
    vectorstore.save_local(save_path)
    return vectorstore
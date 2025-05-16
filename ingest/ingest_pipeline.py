import os
from dotenv import load_dotenv

from document_loaders.utils import load_documents_from_folder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# 환경변수 불러오기
load_dotenv()

# 문서 폴더 경로
input_dir = os.getenv("PDF_DIR", "docs")

# 전체 파일 목록 확인
all_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
print(f"✅ 총 {len(all_files)}개의 파일을 감지했습니다.")

# 1. 문서 로딩
print("📥 문서 로딩 중...")
docs = load_documents_from_folder(input_dir)
print(f"🔍 총 {len(docs)}개의 페이지를 로드했습니다.")

# 2. 텍스트 분할
print("✂️ 텍스트 분할 중...")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)
print(f"📄 총 {len(split_docs)}개의 청크로 분할했습니다.")

# 3. 임베딩 및 벡터 저장
print("🔗 임베딩 및 벡터 저장 중...")
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(split_docs, embedding)
vectorstore.save_local("faiss_index")

print("✅ FAISS 벡터 저장 완료!")
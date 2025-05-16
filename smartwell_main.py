import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ✅ Gemini LLM 클라이언트 래퍼 임포트
from llm_client import GeminiLLMClient

# 환경변수 불러오기
load_dotenv()

def load_smartwell_chain():
    # 임베딩 모델 설정
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # FAISS 벡터스토어 불러오기
    vectorstore = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever()

    # ✅ Gemini LLM 클라이언트를 통해 모델 불러오기
    llm = GeminiLLMClient(model="models/gemini-1.5-flash", temperature=0).get_llm()

    # 커스텀 프롬프트 설정
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""너는 전문 건강 리포트를 작성하는 의사이자, 사용자 데이터를 바탕으로 맞춤형 건강 피드백을 제공하는 데이터 분석 전문가야.  
아래 문서(context)를 바탕으로 사용자의 건강 상태를 평가하고, 지정된 형식에 따라 **의학적 근거에 기반한 리포트**를 생성해줘.

---

[건강 점수 안내]
사용자에게 부여된 건강 점수(Health Score, 0~100)는  
- 웨어러블 시계열 데이터로 측정한 심박데이터와  
-정적 신체 측정값(예: 혈압, BMI, 키, 체중, 걸음수, 수면 시간 등)을 기반으로 AI 기반 이상 탐지 모델에 의해 계산된 종합 지표야.

이 점수는 단순한 평균이 아니라, 정상적인 건강 패턴으로부터의 거리를 반영하는 지표로,  
점수가 낮을수록 특정 이상 징후가 있을 가능성이 높다는 뜻이야.  
따라서 리포트 작성 시, 이 점수를 반드시 참고해 분석의 핵심 방향을 잡아야 해.

---

### 📌 꼭 지켜야 할 원칙:

- 반드시 `context` 내 논문 내용을 기반으로 사용자의 건강을 분석하고 조언할 것  
- context 내용을 전문가가 환자에게 스스로 판단해서 설명하는 것처럼 자연스럽게 설명할 것  
- context에서 사용된 근거가 되는 정보는 리포트 내용 안에 자연스럽게 포함할 것
- 리포트는 **Markdown 형식**으로 작성할 것 (굵은 제목, 리스트, 강조 등 적극 활용)

---

### 📄 출력 리포트 형식

---

## 👤 건강 리포트

### 1️⃣ 개요  
- 사용자 기본 정보 요약 (이름, 키, 몸무게, BMI, 혈압, 건강 점수 포함)  
- 분석 목적과 평가 범위 설명 (예: “이 리포트는 최근 웨어러블 데이터와 신체 측정값을 바탕으로...")

### 2️⃣ 현재 건강 상태 분석  
- 심박수, 걸음 수, 혈압 등 주요 데이터 기반 평가  
- 정상 범위와의 차이 설명  
- 건강 점수를 분석 방향의 기준으로 삼아 중립적으로 해석

### 3️⃣ 건강 위험 요인 및 관리 방안  
- 체중, 혈압, 스트레스, 수면 등 주요 건강 요소별 위험 요인 지적  
- 각 위험 요인별 **근거와 수치**를 제시한 후, 관리 방법을 구체적으로 제안  
- 너무 일반적인 조언은 금지. 반드시 사용자 데이터와 연결된 조언만 쓸 것

### 4️⃣ 실천 계획 제안 (3개월, 6개월, 1년)  
- 시기별 목표 설정  
- 각 시기별로 **측정 가능한 실천 항목**을 구체적으로 제시 

### 5️⃣ 결론 및 전문가 조언  
- 전체 분석 내용을 요약  
- 가장 주의해야 할 건강 요소와 그 이유를 명확히 강조  
- “데이터 기반 조언” + “실현 가능한 조치”를 결합한 조언 작성  
- 마지막에는 **감정적 동기 부여가 포함된 문장**으로 사용자의 실천을 독려할 것

---

문서 내용:  
{context}

학생 질문:  
{question} """
    )

    # QA 체인 구성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt}
    )

    return qa_chain
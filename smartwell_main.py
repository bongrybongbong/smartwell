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
        template="""
당신은 전문 건강 리포트를 작성하는 의사이자, 사용자 데이터를 바탕으로 맞춤형 건강 피드백을 제공하는 데이터 분석 전문가입니다.
아래 문서(context)를 기반으로 사용자의 건강 상태를 평가하고, 지정된 형식에 따라 **의학적 근거에 기반한 리포트**를 생성해주세요.

[건강 점수 안내]
사용자에게 부여된 건강 점수(Health Score, 0~100)는
- 웨어러블 시계열 데이터로 측정한 심박데이터와
- 정적 신체 측정값(예: 혈압, BMI, 키, 체중, 걸음수, 수면 시간 등)을 기반으로
AI 기반 이상 탐지 모델에 의해 계산된 종합 지표입니다.

이 점수는 단순한 평균이 아니라, 정상적인 건강 패턴으로부터의 거리를 반영하는 지표이며,
점수가 낮을수록 특정 이상 징후가 있을 가능성이 높다는 의미입니다.
리포트 작성 시, 이 점수를 반드시 참고하여 분석의 핵심 방향을 설정해야 합니다.

시스템은 다음과 같은 사전 정의된 논리 블록 및 조건 기반 분기 구조(if-then 방식)를 따릅니다.

- If 건강 점수 < 60 then 이상 징후 중심의 주의 강조
- If 60 ≤ 점수 < 80 → 주의 항목과 개선 방안 병행
- If 점수 ≥ 80 → 양호한 상태 중심의 유지 및 예방 조언

- If 걸음 수 < 5,000보 → 활동량 부족 강조 및 수치 제안
- If 수면 시간 < 6시간 → 회복 부족 지적 및 개선 권고
- If 혈압 ≥ 130 → 고혈압 전단계 이상 조기 관리 조언

[작성 가이드라인]
- 모든 리포트는 전문가가 환자에게 설명하듯 자연스럽고 중립적인 문장으로 작성합니다.
- 조언은 반드시 사용자 수치와 연결합니다.
- 실천 계획은 수치 기반 목표 + 확인 가능한 측정 수단을 포함해야 합니다.
- 마지막은 감정적 동기를 유도하는 마무리 문장으로 사용자의 실천을 격려합니다.

[리포트 형식: Markdown으로 작성]

## 👤 건강 리포트

### 1️⃣ 개요
- 이름, 키, 몸무게, BMI, 혈압, 건강 점수 포함
- 분석 목적 및 범위 설명

### 2️⃣ 현재 건강 상태 분석
- 심박수, 걸음 수, 혈압 등 주요 데이터 기반 평가
- 정상 범위와의 차이 해석 포함
- 건강 점수를 중심 기준으로 삼아 중립적으로 해석

### 3️⃣ 건강 위험 요인 및 관리 방안
- 각 건강 요소별 위험 요인 식별 및 수치 기반 진단
- 데이터 기반 관리 방안 구체적으로 제시
- 개인 수치와 연결된 조언만 허용

### 4️⃣ 실천 계획 제안 (3개월, 6개월, 1년)
- 시기별 실천 목표 + 측정 가능한 항목 제시

### 5️⃣ 결론 및 전문가 조언
- 전체 요약 및 주의 요소 재강조
- 데이터 기반 실천 항목 정리
- 마지막은 감정적 동기 부여 문장 포함

문서 내용: {context}

학생 질문: {question}
"""
    )

    # QA 체인 구성
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt}
    )

    return qa_chain



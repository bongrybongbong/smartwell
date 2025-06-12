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
You are a professional medical doctor and a data analysis expert who writes personalized health reports based on user data.
Based on the following document (context), evaluate the user's health status and generate a medically grounded report according to the specified format.

[Health Score Information]
The user's Health Score (0~100) is a comprehensive index calculated by an AI-based anomaly detection model using:
- Time-series heart rate data measured via wearable devices, and
- Static physical metrics (e.g., blood pressure, BMI, height, weight, step count, sleep duration).

This score is not a simple average but reflects the deviation from normal health patterns.
A lower score indicates a higher likelihood of potential anomalies.
When writing the report, this score must be referenced as a key factor guiding the analysis.

The system follows predefined logical blocks and conditional branching (if-then logic) as below:

- If Health Score < 60 → Emphasize potential anomalies and caution
- If 60 ≤ Score < 80 → Address cautionary points and suggest improvement strategies
- If Score ≥ 80 → Focus on maintaining a good state and providing preventive advice

- If Step Count < 5,000 → Emphasize insufficient activity and suggest target values
- If Sleep Duration < 6 hours → Highlight recovery insufficiency and recommend improvements
- If Blood Pressure ≥ 130 → Provide early management advice for pre-hypertensive states

[Writing Guidelines]
- The report must be written in a natural and neutral tone, as if a professional is explaining to a patient.
- Advice must always be directly linked to the user's actual data.
- Action plans should include measurable goals and methods to track progress.
- The conclusion should encourage the user with a motivational closing statement.

[Report Format: Please write in Markdown]

## 👤 Health Report

### 1️⃣ Overview
- Include Name, Height, Weight, BMI, Blood Pressure, Health Score
- Explain the purpose and scope of the analysis
- Do not include BMI calculation logic.

### 2️⃣ Current Health Status Analysis
- Evaluate major metrics such as heart rate, step count, blood pressure
- Interpret deviations from normal ranges
- Use the Health Score as the central reference point for the interpretation

### 3️⃣ Health Risk Factors and Management Strategies
- Identify risk factors per health metric and provide data-driven assessments
- Provide specific management strategies based on the user's data
- Only provide advice connected to the user’s actual numbers

### 4️⃣ Action Plan Proposal (3 months, 6 months, 1 year)
- Propose actionable goals per time period, with measurable indicators

### 5️⃣ Conclusion and Expert Advice
- Summarize the overall findings and re-emphasize key caution points
- Organize actionable items based on data insights
- Conclude with an emotionally supportive statement to motivate the user

Document content: {context}
question: {question}
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



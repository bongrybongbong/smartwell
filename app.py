import streamlit as st
from smartwell_main import load_smartwell_chain
from streamlit.components.v1 import html

st.set_page_config(
    page_title="SmartWell 건강 리포트",
    layout="wide",
    page_icon="🩺"
)

# --- 헤더 영역 ---
st.markdown("""
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #2F80ED;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #6B7280;
        margin-bottom: 30px;
    }
    .st-emotion-cache-1v0mbdj p {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🩺 SmartWell 건강 리포트</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>성균관대학교 스마트팩토리캡스톤디자인 · 7팀 진태헌 외</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>당신의 건강 데이터를 기반으로 한 맞춤형 분석 리포트를 받아보세요</div>", unsafe_allow_html=True)


# --- 폼 입력 ---
with st.form("health_form"):
    st.markdown("### 👤 사용자 정보 입력")

    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("이름", value="홍길동")
        height = st.number_input("키 (cm)", value=175)
        bmi = st.selectbox("BMI 범주", ["정상", "과체중", "비만"], index=1)

    with col2:
        weight = st.number_input("몸무게 (kg)", value=70)
        bp = st.text_input("혈압 (예: 128/83)", value="128/83")
        score = st.slider("건강 점수 (0~100)", min_value=0, max_value=100, value=90)

    with col3:
        hr = st.number_input("하루 평균 심박수", value=75)
        steps = st.number_input("하루 평균 걸음 수", value=7000)

    submitted = st.form_submit_button("🔍 리포트 생성하기")

# --- 리포트 생성 ---
if submitted:
    question_text = (
        f"나는 {name}, 건강점수는 {score}점이래 키 {height}센치 이고 몸무게는 {weight}키로, "
        f"bmi {bmi}, 혈압 {bp}, 하루 평균 심박수 {hr} 데일리 걸음수 {steps}이야"
    )

    with st.spinner("🧠 리포트 생성 중입니다. 잠시만 기다려주세요..."):
        qa_chain = load_smartwell_chain()
        result = qa_chain.invoke({
            "query": str(question_text),
            "name": name
        })

        report = result["result"]

    st.markdown("---")
    st.markdown("## 📋 건강 리포트 결과")
    st.markdown("""
        <div style='padding: 20px; background-color: #F9FAFB; border-radius: 12px;'>
    """ + report + """
        </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="📥 리포트 다운로드 (TXT)",
        data=report,
        file_name=f"{name}_건강리포트.txt",
        mime="text/plain",
        use_container_width=True
    )

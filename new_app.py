import streamlit as st
import requests
import json
import re
from smartwell_main import load_smartwell_chain
import html

st.set_page_config(layout="centered")

# FastAPI 서버 endpoint
url = "https://89ce-203-252-33-5.ngrok-free.app/get_latest_result"

sample_user_profile = {
    "name": "홍길동",
    "height": 170,
    "weight": 80,
    "bmi": "과체중",
    "blood_pressure": "120/80",
    "heart_rate": 82,
    "daily_steps": 3000,
    "sleep_duration": 4,
    "health_score": 60,
}

# 리포트 Section 파서
def parse_report_sections(report_text):
    section_pattern = r"(### \d️⃣ .+?)(?=\n### |\Z)"
    sections = re.findall(section_pattern, report_text, flags=re.DOTALL)
    parsed_sections = {}
    for section in sections:
        lines = section.strip().split("\n")
        title_line = lines[0].replace("###", "").strip()
        content = "\n".join(lines[1:]).strip()
        parsed_sections[title_line] = content
    return parsed_sections

# 상단 타이틀
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>Welcome to SmartWell </h1>
""", unsafe_allow_html=True)

# 사이드바 구성
with st.sidebar:
    st.image("logo.png", width=200)

    # 버튼 스타일
    st.markdown("""
        <style>
        .styled-button {
            display: block;
            width: 100%;
            padding: 14px 0;
            margin-bottom: 16px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            text-align: center;
            color: #fff !important;
            background-color: #4CAF50;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: background-color 0.2s ease, transform 0.05s ease;
        }
        .styled-button.secondary {
            background-color: #2196F3;
        }
        div[data-testid="stForm"] {
            border: none !important;
            background-color: transparent !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 리포트 가져오기 버튼
    with st.form(key="get_report_form"):
        submitted = st.form_submit_button("📥 리포트 가져오기", use_container_width=True)
        if submitted:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                st.session_state["user_profile"] = data
                st.session_state["status_msg"] = ("success", "리포트 데이터를 성공적으로 가져왔습니다!")
            except requests.exceptions.RequestException as e:
                st.session_state["status_msg"] = ("error", f"데이터 요청 실패: {e}")

    # 샘플 데이터 로드 버튼
    with st.form(key="sample_report_form"):
        submitted_sample = st.form_submit_button("📄 샘플 레포트 확인하기", use_container_width=True)
        if submitted_sample:
            st.session_state["user_profile"] = sample_user_profile
            st.session_state["status_msg"] = ("success", "샘플 리포트가 로드되었습니다!")

    # 버튼 하단 구분선
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: none; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)

# 메인 화면에 메시지 출력
msg_type, msg_text = st.session_state.get("status_msg", (None, None))
if msg_type == "success":
    st.success(msg_text)
elif msg_type == "error":
    st.error(msg_text)
st.session_state["status_msg"] = (None, None)

# 사용자 프로필 확인 및 리포트 생성
if "user_profile" in st.session_state:
    user_profile = st.session_state["user_profile"]

    # 사이드바 사용자 프로필
    st.sidebar.markdown("### 🧑‍⚕️ 사용자 프로필")
    st.sidebar.markdown(
        f"""
        <div style='padding: 15px; background-color: #FFFFFF; border-radius: 12px; border: 2px solid #4CAF50;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-size: 15px; line-height: 1.8;'>
        <table style='width: 100%; border-collapse: collapse;'>
            <tr><td style='font-weight: bold;'>이름</td><td>{user_profile['name']}</td></tr>
            <tr><td style='font-weight: bold;'>키</td><td>{user_profile['height']} cm</td></tr>
            <tr><td style='font-weight: bold;'>몸무게</td><td>{user_profile['weight']} kg</td></tr>
            <tr><td style='font-weight: bold;'>BMI</td><td>{user_profile['bmi']}</td></tr>
            <tr><td style='font-weight: bold;'>혈압</td><td>{user_profile['blood_pressure']}</td></tr>
            <tr><td style='font-weight: bold;'>심박수</td><td>{user_profile['heart_rate']} 회/분</td></tr>
            <tr><td style='font-weight: bold;'>걸음 수</td><td>{user_profile['daily_steps']} 보</td></tr>
            <tr><td style='font-weight: bold;'>수면 시간</td><td>{user_profile['sleep_duration']} 시간</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True
    )

    # 건강 점수
    score = user_profile['health_score']
    if score >= 70:
        color, bg, emoji = "#2E7D32", "#E8F5E9", "✅😄"
    elif score >= 50:
        color, bg, emoji = "#FF8F00", "#FFF3E0", "⚠️🙂"
    else:
        color, bg, emoji = "#E53935", "#FFEBEE", "🚨😟"
    
    st.sidebar.markdown(f"### {emoji} 건강 점수")
    st.sidebar.markdown(
        f"""
        <div style='padding: 15px; background-color: {bg}; border-radius: 12px; border: 2px solid {color};
                    text-align: center; font-size: 24px; font-weight: bold; color: {color};'>
        {score} / 100
        </div>
        """, unsafe_allow_html=True
    )

    # 리포트 생성
    question_text = f"""
    Name: {user_profile['name']}
    Height: {user_profile['height']} cm
    Weight: {user_profile['weight']} kg
    BMI: {user_profile['bmi']}
    Blood Pressure: {user_profile['blood_pressure']}
    Heart Rate: {user_profile['heart_rate']} bpm
    Daily Steps: {user_profile['daily_steps']} steps
    Sleep Duration: {user_profile['sleep_duration']} hours
    Health Score: {user_profile['health_score']}

    Please analyze this user's health status based on the provided data and generate the full Health Report according to the given format.
    """

    with st.spinner("🧠 리포트 생성 중입니다. 잠시만 기다려주세요..."):
        qa_chain, retriever = load_smartwell_chain()
        docs = retriever.get_relevant_documents(question_text)
        result = qa_chain.combine_documents_chain.run({
            "input_documents": docs,
            "question": question_text
        })
        report = result  # 바로 사용

    # 리포트 섹션 파싱 및 출력
    parsed_report = parse_report_sections(report)
    st.markdown("---")
    st.markdown("## 📋 건강 리포트 결과")
    for section_title, section_content in parsed_report.items():
        st.markdown(
            f"""
            <div style='padding: 10px 15px; margin-bottom: 5px; border-left: 5px solid #4F8DF9;
                        background-color: #F0F4FF; font-size: 22px; font-weight: bold; color: #2c3e50;
                        border-radius: 5px;'>
                {section_title}
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(section_content)
        
    # 📄 텍스트 파일로 다운로드 버튼
    st.markdown("### ⬇️ 리포트 저장하기")

    st.download_button(
        label="📝 텍스트 파일로 다운로드",
        data=report,
        file_name=f"{user_profile['name']}_health_report.txt",
        mime="text/plain",
        use_container_width=True
    )

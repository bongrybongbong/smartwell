import streamlit as st
import requests
import json
import datetime
import re
from smartwell_main import load_smartwell_chain

# FastAPI 서버 endpoint
url = "https://89ce-203-252-33-5.ngrok-free.app/get_latest_result"

sample_user_profile = {
    "name": "홍길동",
    "height": 170,
    "weight": 90,
    "bmi": "과체중",
    "blood_pressure": "120/80",
    "heart_rate": 72,
    "daily_steps": 3000,
    "sleep_duration": 4,
    "health_score": 40,
}

# 리포트 Section 파서 (미리 준비)
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

# user_profile 초기 None (아직 없음)
user_profile = None

# 상단 타이틀
st.title("스마트팩토리캡스톤디자인 · 7팀 진태현 외")

# 학교 로고 + 설명만 기본 표시

st.markdown(
    """
    ### 📚 프로젝트 소개
    본 서비스는 개인 건강 데이터를 분석하여 **맞춤형 건강 리포트**를 제공하는 솔루션입니다.
    사용자의 웨어러블 기기 데이터를 기반으로 AI가 건강 상태를 평가하고,
    **개인화된 건강 관리 방안**을 제시합니다.
    """
)

with st.sidebar:
    st.image("logo.jpg", width=300)
    st.sidebar.title("⚙️ 리포트 메뉴")

    # 버튼 클릭 시 서버에서 데이터 가져오기
    if st.button("📥 리포트 가져오기"):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # 받아온 데이터 세션 상태에 저장 (Streamlit 추천 패턴)
            st.session_state["user_profile"] = data
            st.success("리포트 데이터를 성공적으로 가져왔습니다!")

        except requests.exceptions.RequestException as e:
            st.error(f"데이터 요청 실패: {e}")
            
    if st.button("📝 샘플 레포트 확인하기"):
            st.session_state["user_profile"] = sample_user_profile
            st.success("샘플 리포트가 로드되었습니다!")


# user_profile 존재 여부 확인 → 있으면 표시
if "user_profile" in st.session_state:
    user_profile = st.session_state["user_profile"]

    # 프로필 표시
    st.sidebar.markdown("### 🧑‍⚕️ 사용자 프로필")
    st.sidebar.markdown(
    f"""
    <div style='padding: 15px; background-color: #FFFFFF; border-radius: 12px; border: 2px solid #4CAF50;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-size: 15px; line-height: 1.8;'>
    <table style='width: 100%; border-collapse: collapse; color: #333;'>  <!-- 여기 color 추가됨 -->
        <tr>
            <td style='font-weight: bold; padding: 8px;'>이름</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['name']}</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>키</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['height']} cm</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>몸무게</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['weight']} kg</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>BMI</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['bmi']}</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>혈압</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['blood_pressure']}</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>평균 심박수</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['heart_rate']} 회/분</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>하루 평균 걸음 수</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['daily_steps']} 보</td>
        </tr>
        <tr>
            <td style='font-weight: bold; padding: 8px;'>수면 시간</td>
            <td style='padding: 8px; word-break: break-word; white-space: normal; overflow: visible;'>{user_profile['sleep_duration']} 시간</td>
        </tr>
    </table>
    </div>
    """,
        unsafe_allow_html=True
    )
    # 건강 점수 표시
    score = user_profile['health_score']
    if score >= 70:
        color = "#2E7D32"
        bg_color = "#E8F5E9"
        emoji = "✅😄"
    elif 50 <= score < 70:
        color = "#FF8F00"
        bg_color = "#FFF3E0"
        emoji = "⚠️🙂"
    else:
        color = "#E53935"
        bg_color = "#FFEBEE"
        emoji = "🚨😟"

    st.sidebar.markdown(f"### {emoji} 건강 점수")
    st.sidebar.markdown(
        f"""
        <div style='padding: 15px; background-color: {bg_color}; border-radius: 12px; border: 2px solid {color};
                    text-align: center; font-size: 24px; font-weight: bold; color: {color};'>
        {score} / 100
        </div>
        """,
        unsafe_allow_html=True
    )

    # 📝 리포트 자동 생성 + 출력
    question_text = (
        f"나는 {user_profile['name']}, "
        f"건강점수는 {user_profile['health_score']}점이래. "
        f"키 {user_profile['height']}cm이고 몸무게는 {user_profile['weight']}kg야. "
        f"BMI는 {user_profile['bmi']}, 혈압은 {user_profile['blood_pressure']}야. "
        f"평균 심박수는 {user_profile['heart_rate']}회/분이고, "
        f"하루 평균 걸음 수는 {user_profile['daily_steps']}보, "
        f"수면 시간은 {user_profile['sleep_duration']}시간이야."
    )

    with st.spinner("🧠 리포트 생성 중입니다. 잠시만 기다려주세요..."):
        qa_chain = load_smartwell_chain()
        result = qa_chain.invoke({
            "query": str(question_text),
            "name": user_profile['name']
        })
        report = result["result"]

    parsed_report = parse_report_sections(report)

    # Streamlit 출력
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
            """,
            unsafe_allow_html=True
        )
        st.markdown(section_content)

    # 📄 리포트 다운로드 버튼
    st.markdown("---")
    st.markdown("### 📄 리포트 다운로드")
    st.download_button(
        label="📥 리포트 TXT 다운로드",
        data=report.encode('utf-8'),
        file_name=f"{user_profile['name']}_health_report.txt",
        mime="text/plain"
    )

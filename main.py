import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (귀여운 타이틀과 아이콘)
st.set_page_config(
    page_title="말랑말랑 MBTI 진로 탐험대",
    page_icon="🎒",
    layout="centered"
)

# 데이터 베이스 (예시 데이터 - 확장 가능)
mbti_data = {
    "INFP (열정적인 중재자 🧚)": {
        "desc": "마음이 따뜻하고 조용하며, 자신만의 가치관과 이상을 중요하게 생각해요. 창의적이고 공감 능력이 아주 뛰어나답니다!",
        "jobs": ["작가 📝", "심리상담사 🧠", "일러스트레이터 🎨", "환경운동가 🌱"],
        "scores": {"창의성": 9, "공감능력": 10, "분석력": 4, "리더십": 5, "자율성": 9}
    },
    "ESTJ (경영자 👔)": {
        "desc": "구체적이고 현실적이며 사실적이에요. 일을 조직화하고 이끌어나가는 능력이 탁월한 타고난 대장님 스타일입니다!",
        "jobs": ["프로젝트 매니저 📊", "경찰관 👮", "재무 분석가 💵", "기업 경영자 🏢"],
        "scores": {"창의성": 4, "공감능력": 5, "분석력": 9, "리더십": 10, "자율성": 6}
    },
    "ENFJ (정의로운 사회운동가 ☀️)": {
        "desc": "따뜻하고 적극적이며 책임감이 강해요. 다른 사람들의 생각과 올바른 성장에 깊은 관심을 가지고 이끌어주는 멋진 멘토예요!",
        "jobs": ["교사 🧑‍🏫", "인사담당자(HR) 🤝", "시민단체 활동가 🌍", "동기부여 강사 🎤"],
        "scores": {"창의성": 8, "공감능력": 10, "분석력": 6, "리더십": 9, "자율성": 7}
    },
    "INTP (논리적인 사색가 🦉)": {
        "desc": "조용하고 신중하며, 논리적인 분석과 문제를 해결하는 것을 좋아해요. 호기심이 많고 자신만의 지적 세계가 뚜렷합니다!",
        "jobs": ["데이터 과학자 💻", "연구원 🔬", "게임 개발자 🎮", "철학자 📚"],
        "scores": {"창의성": 9, "공감능력": 4, "분석력": 10, "리더십": 5, "자율성": 9}
    }
}

# 2. 웹앱 타이틀 및 소개
st.title("🎒 말랑말랑 MBTI 진로 탐험대")
st.caption("✨ 내 MBTI에 꼭 맞는 찰떡 직업은 무엇일까? 쉽고 재미있게 알아보아요! ✨")

st.markdown("---")

# 3. 사용자 편의성을 고려한 입력부 (Select Box)
st.subheader("🧐 나의 MBTI는 무엇인가요?")
selected_mbti = st.selectbox(
    "아래 목록에서 MBTI를 콕 집어 선택해주세요!",
    options=list(mbti_data.keys()),
    index=0
)

# 선택된 데이터 가져오기
data = mbti_data[selected_mbti]

st.markdown("---")

# 4. 결과 출력 섹션
st.header(f"✨ {selected_mbti} 탐험 결과")

# (1) MBTI 특징 (Callout 스타일로 가독성 높임)
st.subheader("💭 어떤 특징을 가지고 있나요?")
st.info(data["desc"])

# (2) 직업군 특성 점수 (차트와 수치로 시각화)
st.subheader("📊 직업군 특성 점수 (0 ~ 10점)")

# 딕셔너리 데이터를 판다스 데이터프레임으로 변환
score_df = pd.DataFrame(list(data["scores"].items()), columns=["특성", "점수"])

# 스트림릿 내장 바 차트로 시각화
st.bar_chart(score_df.set_index("특성"))

# 세부 점수 표기 (사용자가 정확한 숫자를 볼 수 있도록)
cols = st.columns(len(data["scores"]))
for i, (trait, score) in enumerate(data["scores"].items()):
    with cols[i]:
        st.metric(label=trait, value=f"{score}점")

st.markdown("---")

# (3) 추천 직업 (귀여운 카드 형태로 배치)
st.subheader("🚀 이런 직업을 추천해요!")
job_cols = st.columns(2)

for idx, job in enumerate(data["jobs"]):
    # 2열로 나누어 이쁘게 배치
    with job_cols[idx % 2]:
        st.markdown(
            f"""
            <div style="
                background-color: #f0f2f6; 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 10px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            ">
                {job}
            </div>
            """, 
            unsafe_allow_html=True
        )

# 5. 하단 안내 멘트
st.markdown("---")
st.caption("💡 본 결과는 진로 교육을 위한 참고용 자료입니다. 여러분의 가능성은 무궁무진해요! 💪")

import streamlit as st
import datetime
import time

# ==========================================
# 1. 신비로운 사주 & 운세 더미 데이터 정의
# ==========================================

# 사주 10가지 천간(일간)과 신비로운 별칭
ELEMENTS = [
    {"이름": "갑목(甲木)", "수식어": "🌲 하늘을 향해 곧게 뻗은 낙락장송"},
    {"이름": "을목(乙木)", "수식어": "🌱 바위 틈에서도 피어나는 강인한 넝쿨"},
    {"이름": "병화(丙火)", "수식어": "☀️ 세상을 구석구석 비추는 강렬한 태양"},
    {"이름": "정화(丁火)", "수식어": "🕯️ 어둠을 은은하게 밝히는 따뜻한 등불"},
    {"이름": "무토(戊土)", "수식어": "⛰️ 모든 것을 포용하는 거대하고 신비로운 명산"},
    {"이름": "기토(己土)", "수식어": "🌾 생명을 키워내는 어머니처럼 따뜻한 대지"},
    {"이름": "경금(庚金)", "수식어": "⚔️ 단단하고 날카로운 원석과 정의로운 검"},
    {"이름": "신금(辛金)", "수식어": "💎 은은한 달빛 아래 빛나는 아름다운 보석"},
    {"이름": "임수(壬水)", "수식어": "🌊 모든 것을 품고 흘러가는 깊고 넓은 바다"},
    {"이름": "계수(癸水)", "수식어": "🌧️ 대지를 촉촉하게 적시는 지혜로운 봄비"}
]

# 오늘의 운세 신비로운 풀이 데이터
DUMMY_FORTUNES = [
    {
        "총평": "🌌 천기의 흐름이 당신의 편으로 흐르는 날입니다. 막혔던 운로가 열리고 귀인이 문을 두드리니, 망설이던 일이 있다면 오늘 과감히 나아가십시오.",
        "재물": 95, "애정": 85, "건강": 75, "조언": "🍀 동쪽에서 길한 기운이 오니 산책을 하며 기운을 정화해보세요."
    },
    {
        "총평": "✨ 밤하늘의 별들이 당신의 앞길을 은은하게 비추고 있습니다. 새로운 인연이나 기회가 찾아올 신호가 보이니 마음을 열고 변화를 맞이하세요.",
        "재물": 75, "애정": 95, "건강": 85, "조언": "🤫 비밀스러운 계획은 오늘 발설하지 않는 것이 이롭습니다."
    },
    {
        "총평": "🌊 흐르는 물처럼 때를 기다려야 하는 날입니다. 무리한 전진보다는 스스로를 돌아보고 내실을 다질 때, 조만간 더 큰 파도를 탈 수 있습니다.",
        "재물": 50, "애정": 65, "건강": 90, "조언": " 가벼운 명상이나 따뜻한 차 한 잔이 오늘의 액운을 막아줍니다."
    },
    {
        "총평": "🔥 가슴속의 열정이 현실의 결실로 맺히는 강렬한 하루입니다. 당신의 매력이 최고조에 달하니 대인 관계에서 중심적인 역할을 하게 됩니다.",
        "재물": 90, "애정": 80, "건강": 85, "조언": "☀️ 붉은색 계열의 아이템이 행운의 에너지를 증폭시켜 줍니다."
    },
    {
        "총평": "🧘 신중함이 최고의 무기가 되는 날입니다. 구름에 달이 가려진 형국이니 중요한 계약이나 지출은 잠시 보류하고 호흡을 가다듬는 것이 현명합니다.",
        "재물": 60, "애정": 70, "건강": 60, "조언": " 말을 아끼고 경청할 때 예상치 못한 행운의 열쇠를 얻습니다."
    }
]

def get_mystic_fortune(birth_date, birth_time):
    """생년월일과 태어난 시간을 조합해 신비로운 운세를 계산하는 함수"""
    today = datetime.date.today()
    
    # 시간(시)을 숫자로 매핑하여 시드 계산에 포함
    time_score = len(birth_time) * 7
    seed_number = birth_date.year + birth_date.month + birth_date.day + today.year + today.month + today.day + time_score
    
    # 인덱스 추출
    element_idx = seed_number % len(ELEMENTS)
    fortune_idx = seed_number % len(DUMMY_FORTUNES)
    
    return {
        "기운": ELEMENTS[element_idx],
        "운세": DUMMY_FORTUNES[fortune_idx]
    }

# ==========================================
# 2. 스트림릿 UI 레이아웃 (사용자 편의성 강화)
# ==========================================

st.set_page_config(page_title="방구석 만세력 & 운세", page_icon="🔮", layout="centered")

# 상단 헤더 및 타이틀
st.markdown("<h1 style='text-align: center; color: #8A2BE2;'>🔮 신비로운 방구석 사주</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em;'>우주의 기운과 오늘의 일진을 분석하여 당신의 숨겨진 운명을 속삭여 드립니다.</p>", unsafe_allow_html=True)
st.caption("<p style='text-align: center; color: gray;'>※ 현재는 신비로운 테스트용 더미 데이터가 흐르고 있습니다.</p>", unsafe_allow_html=True)

st.write("")

# 입력 섹션 (카드 스타일로 시각적 분리)
with st.container(border=True):
    st.markdown("### 📝 당신의 명조(命造) 입력하기")
    
    # 생년월일 선택 (달력 형태)
    birth_date = st.date_input(
        "📅 태어난 날짜를 선택해 주세요",
        value=datetime.date(2000, 1, 1),
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date.today()
    )
    
    # 사용자 편의를 위한 시간 선택 추가
    birth_time = st.selectbox(
        "⏳ 태어난 시간을 아시나요?",
        ["모름 (일주 중심으로 분석)", "자시 (23:30 ~ 01:30)", "축시 (01:30 ~ 03:30)", "인시 (03:30 ~ 05:30)", 
         "묘시 (05:30 ~ 07:30)", "진시 (07:30 ~ 09:30)", "사시 (09:30 ~ 11:30)", "오시 (11:30 ~ 13:30)", 
         "미시 (13:30 ~ 15:30)", "신시 (15:30 ~ 17:30)", "유시 (17:30 ~ 19:30)", "술시 (19:30 ~ 21:30)", "해시 (21:30 ~ 23:30)"]
    )

st.write("")

# 운세 보기 버튼 (강조 효과)
if st.button("🌌 나의 운명 실시간 통찰하기", use_container_width=True):
    # 몰입감을 주는 스피너 문구
    with st.spinner("🔮 은하의 별자리를 정렬하고 만세력을 조율하는 중... 잠시만 기다려주세요."):
        time.sleep(1.5)  # 신비로운 느낌을 주기 위한 고의적 연산 지연 효과
        result = get_mystic_fortune(birth_date, birth_time)
        
    st.balloons() # 축하 효과로 사용자 재미 극대화
    
    # ----------------------------
    # 결과 화면 1: 타고난 사주 성향
    # ----------------------------
    st.markdown("## 🪐 당신이 타고난 천상의 기운")
    
    with st.container(border=True):
        st.markdown(f"### 🧬 당신의 일간 영혼: **<span style='color: #9370DB;'>{result['기운']['이름']}</span>**", unsafe_allow_html=True)
        st.markdown(f"> **{result['기운']['수식어']}**")
        st.info("💡 명리학 풀이: 이 기운을 가진 사람은 대체로 영감이 뛰어나며 자신만의 독창적인 서사를 만들어내는 힘이 있습니다. (본 해설은 더미 데이터입니다.)")

    st.write("")
    
    # ----------------------------
    # 결과 화면 2: 오늘의 운세 총평
    # ----------------------------
    st.markdown(f"## 📅 오늘의 운세 서사 ({datetime.date.today().strftime('%Y년 %m월 %d일')})")
    
    with st.container(border=True):
        st.markdown("### 💬 운명의 총평")
        st.markdown(f"{result['운세']['총평']}")
        
        st.write("")
        st.markdown("### 🗝️ 오늘의 행운 비책 (Tip)")
        st.warning(f"{result['운세']['조언']}")
        
        st.write("")
        st.markdown("### 📊 오늘의 기운 지수")
        
        # 지수 시각화 (깔끔한 3열 레이아웃)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="💰 재물 흐름", value=f"{result['운세']['재물']}%")
        col2.metric(label="❤️ 인연/애정", value=f"{result['운세']['애정']}%")
        col3.metric(label="💪 건강/활력", value=f"{result['운세']['건강']}%")

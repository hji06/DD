import streamlit as st
import datetime

# ==========================================
# 1. 더미 데이터 및 로직 정의
# ==========================================

# 사주 일간(태어난 날의 천간) 10가지
ELEMENTS = ["갑(甲)", "을(乙)", "병(丙)", "정(丁)", "무(戊)", "기(己)", "경(庚)", "신(辛)", "임(壬)", "계(癸)"]

# 오늘의 운세 더미 데이터 문장들
DUMMY_FORTUNES = [
    {"총평": "귀인을 만나 어려운 일이 순조롭게 풀리는 하루입니다. 주변의 조언에 귀를 기울이세요.", "재물": 90, "애정": 85, "건강": 70},
    {"총평": "새로운 시작에 좋은 날입니다. 망설이던 일이 있다면 오늘 과감하게 도전해보세요.", "재물": 75, "애정": 95, "건강": 80},
    {"총평": "말과 행동을 조심해야 하는 날입니다. 중요한 결정은 내일로 미루는 것이 좋습니다.", "재물": 50, "애정": 60, "건강": 90},
    {"총평": "노력한 만큼 결실이 맺히는 날이니 끝까지 최선을 다하세요. 뜻밖의 소식이 있습니다.", "재물": 95, "애정": 70, "건강": 85},
    {"총평": "마음이 다소 조급해질 수 있으니 명상이나 휴식이 필요합니다. 무리한 지출은 피하세요.", "재물": 60, "애정": 80, "건강": 65},
]

def get_today_fortune(birth_date):
    """사용자 생년월일과 오늘 날짜를 조합해 일정한 더미 운세를 반환하는 함수"""
    today = datetime.date.today()
    
    # 생일과 오늘 날짜를 조합한 고유 숫자 생성 (매일 결과가 달라짐)
    seed_number = birth_date.year + birth_date.month + birth_date.day + today.year + today.month + today.day
    
    # 고유 번호를 기반으로 데이터 매칭 (나머지 연산)
    user_element = ELEMENTS[seed_number % len(ELEMENTS)]
    fortune_index = seed_number % len(DUMMY_FORTUNES)
    
    return {
        "일간": user_element,
        "운세": DUMMY_FORTUNES[fortune_index]
    }

# ==========================================
# 2. 스트림릿 UI 레이아웃
# ==========================================

# 페이지 설정
st.set_page_config(page_title="방구석 사주 & 운세", page_icon="🔮", layout="centered")

# 제목 및 소개
st.title("🔮 방구석 사주 & 오늘의 운세")
st.write("당신의 생년월일을 입력하시면 타고난 기운과 오늘의 운세를 분석해 드립니다.")
st.caption("※ 본 앱은 개발 테스트용 더미 데이터로 작동하고 있습니다.")

st.divider()

# 사용자 입력 UI
st.subheader("📅 정보를 입력해주세요")
birth_date = st.date_input(
    "생년월일 선택",
    value=datetime.date(2000, 1, 1),
    min_value=datetime.date(1950, 1, 1),
    max_value=datetime.date.today()
)

st.divider()

# 분석 및 결과 출력
if st.button("내 운세 보기", use_container_width=True):
    with st.spinner("오늘의 기운을 분석하는 중..."):
        # 로직 계산
        result = get_today_fortune(birth_date)
        
    st.success("분석이 완료되었습니다!")
    
    # 1. 사주 분석 결과
    st.subheader("🧑‍💻 당신의 사주 성향")
    st.info(f"당신은 타고난 오행 중 **[{result['일간']}]**의 성향을 가지고 계시네요! (주관이 뚜렷하고 총명한 타입입니다.)")
    
    st.divider()
    
    # 2. 오늘의 운세 결과
    st.subheader(f"📅 오늘의 운세 ({datetime.date.today().strftime('%Y년 %m월 %d일')})")
    st.markdown(f"> ### \"{result['운세']['총평']}\"")
    
    # 점수 시각화
    col1, col2, col3 = st.columns(3)
    col1.metric(label="💰 재물운", value=f"{result['운세']['재물']}%")
    col2.metric(label="❤️ 애정운", value=f"{result['運세'] if '運세' in result['운세'] else result['운세']['애정']}%") 
    col3.metric(label="💪 건강운", value=f"{result['운세']['건강']}%")

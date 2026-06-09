import streamlit as st
import yfinance as tf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="글로벌 TOP 10 주식 대시보드",
    page_icon="📈",
    layout="wide"
)

st.title("📈 글로벌 시가총액 TOP 10 주식 대시보드")
st.markdown("야후 파이낸스(yfinance) 데이터와 Plotly를 활용한 최근 1년 주가 변화 추적 대시보드입니다.")
st.markdown("---")

# 2. 글로벌 TOP 10 주식 데이터 정의 (티커 및 기업명)
# * 시가총액 순위는 시장 상황에 따라 변동될 수 있습니다.
TOP10_STOCKS = {
    "MSFT": "Microsoft",
    "AAPL": "Apple",
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet (Google)",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "BRK-B": "Berkshire Hathaway",
    "LLY": "Eli Lilly",
    "TSM": "TSMC",
    "TSLA": "Tesla"
}

# 3. 사이드바 - 사용자 입력 받아오기
st.sidebar.header("⚙️ 설정 변경")
selected_tickers = st.sidebar.multiselect(
    "조회할 기업을 선택하세요 (기본 전체)",
    options=list(TOP10_STOCKS.keys()),
    default=list(TOP10_STOCKS.keys()),
    format_func=lambda x: f"{TOP10_STOCKS[x]} ({x})"
)

# 날짜 계산 (최근 1년)
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 4. 데이터 로드 함수 (캐싱 처리로 속도 향상)
@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def load_stock_data(tickers):
    if not tickers:
        return pd.DataFrame()
    
    # 데이터 다운로드
    data = tf.download(tickers, start=start_date, end=end_date)
    
    # 단일 티커일 경우 컬럼 구조가 다를 수 있어 예외 처리
    if len(tickers) == 1:
        df = data['Close'].to_frame()
        df.columns = tickers
    else:
        # MultiIndex 컬럼에서 'Close' 가격만 추출
        df = data['Close']
    return df

# 데이터 가져오기
with st.spinner('야후 파이낸스에서 데이터를 불러오는 중입니다...'):
    df_close = load_stock_data(selected_tickers)

# 5. 메인 화면 시각화
if df_close.empty:
    st.warning("⚠️ 선택된 기업이 없거나 데이터를 불러올 수 없습니다. 사이드바에서 기업을 선택해 주세요.")
else:
    # 5-1. 수익률 비교 차트 (누적 수익률 % 계산)
    st.subheader("📊 최근 1년 누적 수익률 (%) 비교")
    st.caption("시작일 기준 주가를 100으로 맞추어 어느 주식이 가장 많이 올랐는지 비교합니다.")
    
    # 누적 수익률 계산: (현재가격 / 시작가격 - 1) * 100
    df_return = (df_close / df_close.iloc[0] - 1) * 100
    
    fig_return = go.Figure()
    for ticker in df_return.columns:
        fig_return.add_trace(go.Scatter(
            x=df_return.index, 
            y=df_return[ticker], 
            mode='lines', 
            name=f"{TOP10_STOCKS[ticker]} ({ticker})"
        ))
        
    fig_return.update_layout(
        xaxis_title="날짜",
        yaxis_title="수익률 (%)",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig_return, use_container_width=True)
    
    st.markdown("---")
    
    # 5-2. 개별 주가 및 요약 정보 개츠(Metric) 표시
    st.subheader("🏢 기업별 상세 요약 (최근 영업일 기준)")
    
    # 3열 레이아웃으로 메트릭 배치
    cols = st.columns(3)
    
    for i, ticker in enumerate(selected_tickers):
        if ticker in df_close.columns:
            series = df_close[ticker].dropna()
            if len(series) >= 2:
                current_val = series.iloc[-1]
                prev_val = series.iloc[-2]
                delta_val = current_val - prev_val
                delta_pct = (delta_val / prev_val) * 100
                
                # 3개 열에 순차적으로 분배
                with cols[i % 3]:
                    st.metric(
                        label=f"{TOP10_STOCKS[ticker]} ({ticker})",
                        value=f"${current_val:,.2f}",
                        delta=f"${delta_val:,.2f} ({delta_pct:+.2f}%)"
                    )

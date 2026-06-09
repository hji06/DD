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
st.markdown("야후 파이낸스(yfinance) 데이터를 활용한 주가 변화 및 투자 정보 대시보드입니다.")
st.markdown("---")

# 2. 글로벌 TOP 10 주식 데이터 정의
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

# 3. 사이드바 - 기본 설정
st.sidebar.header("⚙️ 전체 설정")
selected_tickers = st.sidebar.multiselect(
    "메인 차트에 표시할 기업들을 선택하세요",
    options=list(TOP10_STOCKS.keys()),
    default=list(TOP10_STOCKS.keys()),
    format_func=lambda x: f"{TOP10_STOCKS[x]} ({x})"
)

# 데이터 로드 (최근 1년치 기본)
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data(ttl=3600)
def load_stock_data(tickers):
    if not tickers:
        return pd.DataFrame()
    data = tf.download(tickers, start=start_date, end=end_date)
    if len(tickers) == 1:
        df = data['Close'].to_frame()
        df.columns = tickers
    else:
        df = data['Close']
    return df

with st.spinner('데이터를 불러오는 중입니다...'):
    df_close = load_stock_data(selected_tickers)

# --- 메인 화면: 1년 비교 차트 ---
if df_close.empty:
    st.warning("⚠️ 사이드바에서 기업을 선택해 주세요.")
else:
    st.subheader("📊 최근 1년 누적 수익률 (%) 비교")
    df_return = (df_close / df_close.iloc[0] - 1) * 100
    
    fig_return = go.Figure()
    for ticker in df_return.columns:
        fig_return.add_trace(go.Scatter(
            x=df_return.index, y=df_return[ticker], mode='lines', name=f"{TOP10_STOCKS[ticker]}"
        ))
    fig_return.update_layout(xaxis_title="날짜", yaxis_title="수익률 (%)", hovermode="x unified", template="plotly_white", height=400)
    st.plotly_chart(fig_return, use_container_width=True)

st.markdown("---")

# --- 🔥 핵심 추가 기능: 특정 회사 1달 투자 자료 상세 보기 ---
st.subheader("🔍 기업별 최근 1달 투자 자료 상세보기")
st.markdown("자세히 보고 싶은 기업을 선택하면 **최근 1달 주가(캔들차트), 거래량, 뉴스**를 보여줍니다.")

# 유저가 집중 분석할 기업 1개 선택
detail_ticker = st.selectbox(
    "분석할 기업을 선택하세요:",
    options=list(TOP10_STOCKS.keys()),
    format_func=lambda x: f"{TOP10_STOCKS[x]} ({x})"
)

if detail_ticker:
    # yfinance Ticker 객체 생성 (뉴스 및 세부 데이터 추출용)
    ticker_obj = tf.Ticker(detail_ticker)
    
    # 최근 1달 데이터만 따로 가져오기
    one_month_ago = end_date - timedelta(days=30)
    df_month = ticker_obj.history(start=one_month_ago, end=end_date)
    
    if not df_month.empty:
        # 레이아웃 분할: 왼쪽은 차트, 오른쪽은 뉴스
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(### f"📈 {TOP10_STOCKS[detail_ticker]} 최근 1달 주가 변동")
            
            # 주식 거래용 캔들차트 그리기
            fig_candle = go.Figure()
            fig_candle.add_trace(go.Candlestick(
                x=df_month.index,
                open=df_month['Open'],
                high=df_month['High'],
                low=df_month['Low'],
                close=df_month['Close'],
                name="주가"
            ))
            fig_candle.update_layout(
                template="plotly_white",
                xaxis_rangeslider_visible=False,
                height=350,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_candle, use_container_width=True)
            
            # 거래량 차트 추가
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(x=df_month.index, y=df_month['Volume'], name='거래량', marker_color='orange'))
            fig_vol.update_layout(template="plotly_white", height=150, margin=dict(l=20, r=20, t=10, b=20))
            st.plotly_chart(fig_vol, use_container_width=True)
            
        with col2:
            st.markdown(### f"📰 {TOP10_STOCKS[detail_ticker]} 관련 최신 뉴스")
            
            # yfinance가 무료로 제공하는 최신 뉴스 긁어오기
            news_list = ticker_obj.news
            
            if news_list:
                # 최대 5개까지만 노출
                for news in news_list[:5]:
                    title = news.get('title', '제목 없음')
                    link = news.get('link', '#')
                    publisher = news.get('publisher', '알 수 없음')
                    
                    # 🔴 뉴스 시각화 디자인 수정: 2026년 야후 파이낸스 뉴스 구조에 맞춤 복구
                    st.markdown(f"**[{title}]({link})**")
                    st.caption(f"출처: {publisher}")
                    st.markdown("---")
            else:
                st.info("현재 가져올 수 있는 최신 뉴스가 없습니다.")
    else:
        st.error("데이터를 불러오지 못했습니다. 티커를 확인해 주세요.")

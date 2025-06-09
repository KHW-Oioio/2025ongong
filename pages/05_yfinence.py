import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌐 글로벌 시가총액 Top 10 기업 주가 및 누적 수익률 시각화")

# 글로벌 시가총액 Top 10 기업 (예시)
top10_tickers = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "Alphabet Class A (GOOGL)": "GOOGL",
    "Alphabet Class C (GOOG)": "GOOG",
    "Tesla (TSLA)": "TSLA",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "NVIDIA (NVDA)": "NVDA",
    "Meta Platforms (META)": "META",
    "Visa (V)": "V",
}

# 사용자에게 종목 선택 받기 (최소 1개 이상)
selected_companies = st.multiselect(
    "관심 있는 기업을 선택하세요 (최소 1개 이상)",
    options=list(top10_tickers.keys()),
    default=["Apple (AAPL)", "Microsoft (MSFT)"]
)

if not selected_companies:
    st.warning("최소 한 개 이상의 기업을 선택해주세요.")
    st.stop()

# 데이터 가져올 기간 (최근 1년)
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# yfinance로 주가 데이터 불러오기
@st.cache_data(ttl=3600)
def fetch_data(tickers, start, end):
    data = yf.download(
        tickers=tickers,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        progress=False,
        group_by='ticker'
    )
    return data

tickers = [top10_tickers[c] for c in selected_companies]
data = fetch_data(tickers, start_date, end_date)

# 데이터 전처리
price_dfs = {}
for ticker in tickers:
    if len(tickers) == 1:
        # yfinance는 단일 ticker 선택시 DataFrame이 다르게 나옴
        df = data.copy()
    else:
        df = data[ticker]
    price_dfs[ticker] = df['Adj Close'].dropna()

# 1) 주가 선 그래프 그리기
fig_price = go.Figure()

for ticker in tickers:
    fig_price.add_trace(
        go.Scatter(
            x=price_dfs[ticker].index,
            y=price_dfs[ticker].values,
            mode='lines',
            name=ticker
        )
    )

fig_price.update_layout(
    title="최근 1년 주가 추이 (Adjusted Close)",
    xaxis_title="날짜",
    yaxis_title="주가(USD)",
    hovermode="x unified"
)

st.plotly_chart(fig_price, use_container_width=True)

# 2) 누적 수익률 계산 및 그래프
cumulative_returns = pd.DataFrame()

for ticker in tickers:
    prices = price_dfs[ticker]
    returns = prices.pct_change().fillna(0)
    cumulative_returns[ticker] = (1 + returns).cumprod() - 1

fig_return = go.Figure()

for ticker in tickers:
    fig_return.add_trace(
        go.Scatter(
            x=cumulative_returns.index,
            y=cumulative_returns[ticker],
            mode='lines',
            name=ticker
        )
    )

fig_return.update_layout(
    title="최근 1년 누적 수익률",
    xaxis_title="날짜",
    yaxis_title="누적 수익률",
    hovermode="x unified",
    yaxis_tickformat=".2%"
)

st.plotly_chart(fig_return, use_container_width=True)

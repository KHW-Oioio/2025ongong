
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rc('font', family='Malgun Gothic')  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False 
# 가상의 반도체 기업 데이터 생성
data = {
    '기업명': ['삼성전자', 'SK하이닉스', '마이크론', '인텔', 'TSMC'],
    '매출(조원)': [250, 100, 90, 80, 120],
    '영업이익(조원)': [50, 20, 15, 10, 25],
    '주가(USD)': [75, 85, 70, 60, 90]
}
df = pd.DataFrame(data)

st.title("반도체 관련 기업 산업 경제 상황")

# 기업별 매출과 영업이익 시각화
fig, ax1 = plt.subplots(figsize=(10,6))

bar_width = 0.35
index = np.arange(len(df['기업명']))

bar1 = ax1.bar(index, df['매출(조원)'], bar_width, label='매출(조원)', color='b')
bar2 = ax1.bar(index + bar_width, df['영업이익(조원)'], bar_width, label='영업이익(조원)', color='g')

ax1.set_xlabel('기업명')
ax1.set_ylabel('조원')
ax1.set_title('기업별 매출 및 영업이익')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels(df['기업명'])
ax1.legend()

st.pyplot(fig)

# 주가 변동 그래프
st.subheader("기업별 주가(USD)")

fig2, ax2 = plt.subplots()
ax2.plot(df['기업명'], df['주가(USD)'], marker='o', linestyle='-', color='r')
ax2.set_xlabel('기업명')
ax2.set_ylabel('주가(USD)')
ax2.set_title('기업별 주가 변동')

st.pyplot(fig2)

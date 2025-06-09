# 03_folium.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
gender_df = pd.read_csv("people_gender.csv", encoding="cp949")

st.set_page_config(layout="wide")
st.title("📊 인구 통계 시각화 대시보드")

# 지역 선택
regions = gender_df["행정구역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 연령 범위 선택
age_range = st.slider("연령대 범위 선택", 0, 100, (0, 100), step=5)

# 데이터 필터링
row = gender_df[gender_df["행정구역"] == selected_region].iloc[0]
male_data = row.filter(like="남_").drop(labels=["2025년05월_남_총인구수", "2025년05월_남_연령구간인구수"])
female_data = row.filter(like="여_").drop(labels=["2025년05월_여_총인구수", "2025년05월_여_연령구간인구수"])

# 연령과 인구수 추출
ages = [int(col.split("_")[-1].replace("세", "").replace("이상", "100")) for col in male_data.index]
male_counts = [int(str(x).replace(",", "")) * -1 for x in male_data.values]
female_counts = [int(str(x).replace(",", "")) for x in female_data.values]

# 슬라이더 필터 적용
filtered = [(a, m, f) for a, m, f in zip(ages, male_counts, female_counts) if age_range[0] <= a <= age_range[1]]
filtered_ages, filtered_male, filtered_female = zip(*filtered)

# 데이터프레임 생성
df_plot = pd.DataFrame({
    "연령": list(filtered_ages) * 2,
    "인구수": list(filtered_male) + list(filtered_female),
    "성별": ["남"] * len(filtered_ages) + ["여"] * len(filtered_ages)
})

# 시각화
fig = px.bar(
    df_plot, 
    x="인구수", y="연령", color="성별", orientation='h',
    title=f"{selected_region}의 연령별 성별 인구 분포",
    height=600,
    color_discrete_map={"남": "blue", "여": "crimson"}
)
fig.update_layout(yaxis=dict(dtick=5), xaxis_title="인구수", yaxis_title="연령(세)")
st.plotly_chart(fig, use_container_width=True)


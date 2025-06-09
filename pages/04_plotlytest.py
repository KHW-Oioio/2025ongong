# 04_plotlytest.py
import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 한글 출력용 페이지 설정
st.set_page_config(layout="wide")
st.title("👥 지역별 인구 피라미드 시각화")

# 데이터 불러오기 (CP949)
gender_df = pd.read_csv("people_gender.csv", encoding="cp949")

# 지역 선택
regions = gender_df["행정구역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 연령 범위 슬라이더
age_range = st.slider("연령대 범위 선택", 0, 100, (0, 100), step=5)

# 선택한 지역의 행 추출
row = gender_df[gender_df["행정구역"] == selected_region].iloc[0]

# 남성/여성 연령별 컬럼만 필터링
male_data = row.filter(like="남_")
female_data = row.filter(like="여_")

# 제외할 열 제거
drop_cols = ["2025년05월_남_총인구수", "2025년05월_남_연령구간인구수"]
male_data = male_data.drop(labels=[col for col in drop_cols if col in male_data])
drop_cols = ["2025년05월_여_총인구수", "2025년05월_여_연령구간인구수"]
female_data = female_data.drop(labels=[col for col in drop_cols if col in female_data])

# 정규식 기반 연령 추출 함수
def extract_age(col_name):
    match = re.search(r"(\d+)(세|세 이상)?", col_name)
    if match:
        return int(match.group(1))
    return None

# 나이/인구수 추출 및 정리
valid_cols = [col for col in male_data.index if extract_age(col) is not None]
ages = [extract_age(col) for col in valid_cols]
male_counts = [int(str(male_data[col]).replace(",", "")) * -1 for col in valid_cols]
female_counts = [int(str(female_data[col]).replace(",", "")) for col in valid_cols]

# 연령 필터 적용
filtered = [(a, m, f) for a, m, f in zip(ages, male_counts, female_counts) if age_range[0] <= a <= age_range[1]]
filtered_ages, filtered_male, filtered_female = zip(*filtered)

# 시각화용 데이터프레임 생성
df_plot = pd.DataFrame({
    "연령": list(filtered_ages) * 2,
    "인구수": list(filtered_male) + list(filtered_female),
    "성별": ["남"] * len(filtered_ages) + ["여"] * len(filtered_ages)
})

# 인구 피라미드 시각화
fig = px.bar(
    df_plot,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title=f"{selected_region}의 연령별 성별 인구 분포",
    height=600,
    color_discrete_map={"남": "blue", "여": "crimson"}
)
fig.update_layout(yaxis=dict(dtick=5), xaxis_title="인구수", yaxis_title="연령(세)")
st.plotly_chart(fig, use_container_width=True)

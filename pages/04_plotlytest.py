import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 앱 기본 설정
st.set_page_config(layout="wide")
st.title("👥 지역별 인구 피라미드 시각화")

# 데이터 불러오기 (CP949 인코딩)
gender_df = pd.read_csv("people_gender.csv", encoding="cp949")

# 지역 선택
regions = gender_df["행정구역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 연령 슬라이더
age_range = st.slider("연령대 범위 선택", 0, 100, (0, 100), step=5)

# 선택한 지역의 데이터 추출
row = gender_df[gender_df["행정구역"] == selected_region].iloc[0]

# 남녀 연령별 컬럼만 추출
male_data = row.filter(like="남_")
female_data = row.filter(like="여_")

# 총인구수 등 제외할 컬럼
drop_male = ["2025년05월_남_총인구수", "2025년05월_남_연령구간인구수"]
drop_female = ["2025년05월_여_총인구수", "2025년05월_여_연령구간인구수"]

male_data = male_data.drop([col for col in drop_male if col in male_data.index])
female_data = female_data.drop([col for col in drop_female if col in female_data.index])

# 연령 추출 함수 (정규표현식)
def extract_age(col_name):
    match = re.search(r"(\d+)(세|세 이상)?", col_name)
    if match:
        return int(match.group(1))
    return None

# 공통적으로 존재하는 유효한 컬럼만 사용
valid_cols = [
    col for col in male_data.index
    if extract_age(col) is not None and col in female_data.index
]

# 나이와 인구수 데이터 정리
ages = [extract_age(col) for col in valid_cols]
male_counts = [int(str(male_data[col]).replace(",", "")) * -1 for col in valid_cols]
female_counts = [int(str(female_data[col]).replace(",", "")) for col in valid_cols]

# 연령 필터 적용
filtered = [
    (a, m, f)
    for a, m, f in zip(ages, male_counts, female_counts)
    if age_range[0] <= a <= age_range[1]
]

if not filtered:
    st.warning("선택한 연령대에는 데이터가 없습니다. 다른 범위를 선택해주세요.")
else:
    filtered_ages, filtered_male, filtered_female = zip(*filtered)

    # 시각화용 데이터프레임 생성
    df_plot = pd.DataFrame({
        "연령": list(filtered_ages) * 2,
        "인구수": list(filtered_male) + list(filtered_female),
        "성별": ["남"] * len(filtered_ages) + ["여"] * len(filtered_ages)
    })

    # plotly 인구 피라미드 그래프
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


st.write("유효한 컬럼들:", valid_cols)
st.write("추출한 연령들:", [extract_age(col) for col in valid_cols])
st.write("선택한 연령대:", age_range)
st.write("연령별 남성 인구수:", male_counts)
st.write("연령별 여성 인구수:", female_counts)

filtered = [
    (a, m, f)
    for a, m, f in zip(ages, male_counts, female_counts)
    if age_range[0] <= a <= age_range[1]
]

st.write("필터링된 데이터:", filtered)
def extract_age(col_name):
    # 컬럼명 중 연령 정보 추출할 부분만 가져오기 (맨 뒤에 '_0세' 혹은 '_5세 이상' 같은 형태 가정)
    age_part = col_name.split('_')[-1]  # 예: "0세", "5세 이상"
    match = re.search(r"(\d+)(세|세 이상)?", age_part)
    if match:
        return int(match.group(1))
    return None
st.write("남성 컬럼명 예시:", list(male_data.index)[:5])
st.write("여성 컬럼명 예시:", list(female_data.index)[:5])

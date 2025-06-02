import streamlit as st

# 전체 MBTI 데이터 (예시 일부만 수록, 필요시 전체 16유형 추가 가능)
mbti_profiles = {
    'INTJ': {
        'summary': '전략가형 - 깊이 있는 사고와 장기적 비전을 지닌 혁신가입니다.',
        'strengths': ['분석적 사고', '높은 자기 통제력', '계획력 뛰어남'],
        'weaknesses': ['감정 표현 부족', '완벽주의 경향'],
        'career': ['전략기획자', 'AI 연구원', '데이터 과학자']
    },
    'ENFP': {
        'summary': '활동가형 - 에너지 넘치고 창의적인 아이디어 뱅크입니다.',
        'strengths': ['공감 능력', '창의성', '다양한 인간관계'],
        'weaknesses': ['계획 부족', '쉽게 싫증냄'],
        'career': ['마케팅 전문가', '작가', '디자이너']
    },
    'ISTJ': {
        'summary': '청렴결백한 논리주의자 - 책임감 강하고 신뢰할 수 있는 현실주의자입니다.',
        'strengths': ['조직력', '정확성', '책임감'],
        'weaknesses': ['융통성 부족', '감정 표현 어려움'],
        'career': ['회계사', '행정공무원', '데이터 관리자']
    },
    # 필요시 추가 유형 삽입
}

st.set_page_config(page_title="MBTI 분석기", layout="centered")
st.title("🧠 MBTI 성격유형 분석기")

with st.expander("📌 MBTI는 무엇인가요?", expanded=False):
    st.markdown("""
    MBTI(Myers-Briggs Type Indicator)는 사람들의 성격을 **16가지 유형**으로 구분하는 성격 유형 검사입니다.  
    아래 4가지 지표를 선택하면 당신의 MBTI 성격 유형과 분석 결과를 알려드릴게요!
    """)

st.header("1️⃣ 성격 지표 선택")

col1, col2 = st.columns(2)

with col1:
    ei = st.radio("에너지 방향 (E / I)", ["E (외향적)", "I (내향적)"])
    tf = st.radio("판단 방식 (T / F)", ["T (논리 중심)", "F (감정 중심)"])
with col2:
    sn = st.radio("정보 인식 (S / N)", ["S (현실적)", "N (직관적)"])
    jp = st.radio("생활 양식 (J / P)", ["J (계획적)", "P (즉흥적)"])

# 유형 생성
mbti_type = ei[0] + sn[0] + tf[0] + jp[0]

st.markdown(f"### 📇 당신의 MBTI 유형은 **:blue[{mbti_type}]**입니다!")

if mbti_type in mbti_profiles:
    profile = mbti_profiles[mbti_type]
    
    tab1, tab2, tab3 = st.tabs(["🔍 요약", "💪 강점과 약점", "🎯 추천 진로"])

    with tab1:
        st.subheader("🔍 성격 요약")
        st.write(profile['summary'])

    with tab2:
        st.subheader("💪 강점")
        for s in profile['strengths']:
            st.markdown(f"- ✅ {s}")
        st.subheader("⚠️ 약점")
        for w in profile['weaknesses']:
            st.markdown(f"- ❌ {w}")

    with tab3:
        st.subheader("🎯 추천 직업")
        for c in profile['career']:
            st.markdown(f"- 👨‍💼 {c}")
else:
    st.error("이 유형에 대한 데이터가 아직 준비되지 않았습니다. 다른 조합을 시도해보세요.")

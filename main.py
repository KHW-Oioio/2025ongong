import streamlit as st
st.title('나의 첫 웹 서비스 만들기!!')
name = st.text_input('이름을 입력하세요 : ')
menu = st.selectbox('좋아하는 음식을 선택해주세요 :', ['비빔면', '탕후루'])
if st.button('인사말 생성'):
  st.write(name + '님! 당신잉 좋아하는 음식은' + menu + '이군요 저도 좋습니다')

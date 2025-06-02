import streamlit as st
import plotly.graph_objects as go

# 세션 상태 초기화
if "stack" not in st.session_state:
    st.session_state.stack = []
if "queue" not in st.session_state:
    st.session_state.queue = []

# 시각화 함수
def draw_boxes(data, title):
    fig = go.Figure()
    for i, val in enumerate(data):
        fig.add_shape(
            type="rect",
            x0=i, y0=0, x1=i+1, y1=1,
            line=dict(color="RoyalBlue"),
            fillcolor="lightblue"
        )
        fig.add_trace(go.Scatter(
            x=[i+0.5], y=[0.5],
            text=[val], mode="text", textfont=dict(size=20)
        ))
    fig.update_layout(
        title=title,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=200, margin=dict(t=50, l=20, r=20, b=20)
    )
    return fig

# 앱 제목
st.title("📚 자료구조 시각화: 스택(Stack)과 큐(Queue)")

# 탭 구성
tab1, tab2 = st.tabs(["📦 스택 (Stack)", "🚶 큐 (Queue)"])

# ------------------------- 스택 -------------------------
with tab1:
    st.subheader("📦 스택이란?")
    st.markdown("""
    - **후입선출 (LIFO)** 구조입니다.
    - 마지막에 넣은 데이터가 가장 먼저 나갑니다.
    - 대표적인 연산: `push`, `pop`
    """)
    
    st.markdown("#### 🔧 스택 조작")
    col1, col2 = st.columns(2)
    with col1:
        new_val = st.text_input("Push할 값:", key="stack_input")
        if st.button("📥 Push", key="push_btn"):
            if new_val:
                st.session_state.stack.append(new_val)
    with col2:
        if st.button("📤 Pop", key="pop_btn"):
            if st.session_state.stack:
                st.session_state.stack.pop()
    
    st.plotly_chart(draw_boxes(list(reversed(st.session_state.stack)), "🧱 Stack (Top이 오른쪽)"))

# ------------------------- 큐 -------------------------
with tab2:
    st.subheader("🚶 큐란?")
    st.markdown("""
    - **선입선출 (FIFO)** 구조입니다.
    - 먼저 들어온 데이터가 먼저 나갑니다.
    - 대표적인 연산: `enqueue`, `dequeue`
    """)

    st.markdown("#### 🔧 큐 조작")
    col3, col4 = st.columns(2)
    with col3:
        new_val = st.text_input("Enqueue할 값:", key="queue_input")
        if st.button("📥 Enqueue", key="enqueue_btn"):
            if new_val:
                st.session_state.queue.append(new_val)
    with col4:
        if st.button("📤 Dequeue", key="dequeue_btn"):
            if st.session_state.queue:
                st.session_state.queue.pop(0)
    
    st.plotly_chart(draw_boxes(st.session_state.queue, "🚚 Queue (Front이 왼쪽)"))

import streamlit as st

st.set_page_config(
    page_title="アルゴリズム学習ノート",
    page_icon="📒",
    layout="wide",
)

st.title("📒 アルゴリズム学習ノート")
st.markdown("paiza Aランク・AtCoder を目指すためのインタラクティブ学習サイト。")

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🔍 BFS（幅優先探索）")
    st.markdown("グラフ・迷路の最短経路探索")
    st.page_link("pages/1_BFS.py", label="BFSを学ぶ →", icon="🔍")
with col2:
    st.markdown("### 🔢 二分探索")
    st.markdown("*近日追加予定*")
with col3:
    st.markdown("### 📊 DP（動的計画法）")
    st.markdown("*近日追加予定*")

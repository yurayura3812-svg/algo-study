import streamlit as st

st.set_page_config(
    page_title="アルゴリズム学習ノート",
    page_icon="📒",
    layout="wide",
)

st.title("📒 アルゴリズム学習ノート")
st.markdown("左のサイドバーからアルゴリズムを選んでください。")

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🔍 BFS")
    st.markdown("グラフ・迷路の最短経路探索")
    st.markdown("→ サイドバー: `BFS（幅優先探索）`")
with col2:
    st.markdown("### 🔢 二分探索")
    st.markdown("*近日追加予定*")
with col3:
    st.markdown("### 📊 DP")
    st.markdown("*近日追加予定*")

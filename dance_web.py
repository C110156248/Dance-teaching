import streamlit as st

st.title("舞蹈動作辨識應用")

# 定義頁面選項

if st.button("開始"):
    st.switch_page("pages/dance_selection.py")



#streamlit run dance_web.py
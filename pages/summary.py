import streamlit as st

st.title("結算")

if 'frames' in st.session_state and 'dance_sequence' in st.session_state and 'image_sequence' in st.session_state:
    frames = st.session_state['frames']
    dance_sequence = st.session_state['dance_sequence']
    image_sequence = st.session_state['image_sequence']  # 確保取得圖片序列

    st.write("完成的動作:")

    for i, (frame, movement, image_name) in enumerate(zip(frames, dance_sequence, image_sequence)):
        cols = st.columns(2)
        with cols[0]:
            st.image(frame, channels="BGR", caption=f"你的動作: {movement}")
        with cols[1]:
            st.image(f'images/{image_name}', caption=f"正確動作: {movement}")


    if st.button("返回舞蹈選取頁面"):
        st.switch_page("pages/dance_selection.py")
else:
    st.write("請先進行舞蹈動作辨識")


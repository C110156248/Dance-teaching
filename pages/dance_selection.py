# dance_selection.py
import streamlit as st

st.title("舞蹈選擇")

# 定義可供選擇的舞蹈動作
available_dances = {
    '舞蹈 1': {
        'sequence': ['A', 'B', 'C', 'A', 'B','C'],
        'images': ['a1.jpg', 'b1.jpg', 'c1.jpg', 'a2.jpg', 'b2.jpg','c1.jpg']
    },
    '舞蹈 2': {
        'sequence': ['B', 'A', 'C'],
        'images': ['b1.jpg', 'a1.jpg', 'c1.jpg']
    }
    # 可以添加更多的舞蹈
}

st.write("請選擇一個舞蹈：")
st.write("---")
# 為每個舞蹈建立一行
for dance_name, dance_info in available_dances.items():
    dance_sequence = dance_info['sequence']
    image_sequence = dance_info['images']

    # 使用 columns 佈局，每行包含三個列
    row = st.columns([1, 4, 1])
    
    with row[0]:
        st.write(f"**{dance_name}**")
    
    with row[1]:
        # 顯示舞蹈的圖片序列
        images = [f'images/{image_name}' for image_name in image_sequence]
        captions = [f"動作: {movement}" for movement in dance_sequence]
        st.image(images, width=100, caption=captions)
    
    with row[2]:
        # 為每個舞蹈添加一個開始按鈕
        if st.button(f"開始舞蹈", key=dance_name):
            # 保存選擇的舞蹈到 session_state
            st.session_state['dance_sequence'] = dance_sequence
            st.session_state['image_sequence'] = image_sequence
            st.session_state['current_step'] = 0  # 初始化當前步驟
            # 跳轉到舞蹈辨識頁面
            st.switch_page("pages/recognition.py")
    st.write("---")
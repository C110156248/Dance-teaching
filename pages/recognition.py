import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import time
from point_to_picture import keypoints_to_image
import pandas as pd

# 載入模型
model = load_model('C:/Users/user/anaconda3/envs/dance/dance/cnn_test2.keras')

# 初始化 Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 定義類別名稱
class_names = ['A', 'B', 'C']  # 根據您的模型類別數進行修改

# 從 session_state 獲取舞蹈順序
dance_sequence = st.session_state.get('dance_sequence', [])
image_sequence = st.session_state.get('image_sequence', [])

if not dance_sequence:
    st.error("未選擇舞蹈序列。請返回選擇舞蹈。")
    st.stop()

current_step = 0

# 初始化 session_state 變數
if 'frames' not in st.session_state:
    st.session_state['frames'] = []

# Streamlit 介面
st.title("舞蹈動作辨識")

def recognize_action(model, keypoints, class_names):
    keypoints_image = keypoints_to_image(keypoints)
    keypoints_image = np.expand_dims(keypoints_image, axis=0)

    preds = model.predict(keypoints_image)
    if preds.shape[1] != len(class_names):
        st.error(f"模型輸出類別數 ({preds.shape[1]}) 與 class_names 列表長度 ({len(class_names)}) 不匹配")
        return None, None

    class_index = np.argmax(preds[0])
    predicted_class = class_names[class_index]
    confidence = preds[0][class_index]
    return predicted_class, confidence
# 初始化狀態
if 'app_state' not in st.session_state:
    st.session_state['app_state'] = 'initial'  # 可能的狀態: initial, video_playing, recognition

# 建立主容器
main_container = st.empty()

# 根據狀態顯示不同內容
if st.session_state['app_state'] == 'initial':
    if main_container.button("開始播放影片"):
        st.session_state['app_state'] = 'video_playing'
        st.rerun()

elif st.session_state['app_state'] == 'video_playing':
    # 播放影片
    video_container = main_container.container()
    video_container.video("images/dance_video.mp4", start_time=0)
    
    if st.button("開始辨識"):
        st.session_state['app_state'] = 'recognition'
        video_container.empty()
        st.rerun()

elif st.session_state['app_state'] == 'recognition':
    # 開始辨識流程
    countdown_placeholder = main_container.empty()
    # 開始辨識
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("無法開啟攝影機")
    else:
        frame_placeholder = st.empty()
        status_placeholder = st.empty()
        start_time = time.time()
        wait_time = time.time()  # 初始化等待時間
        frames = []  # 用於保存每個動作的影像
        while current_step < len(dance_sequence):
            ret, frame = cap.read()
            if not ret:
                st.error("無法讀取影像")
                break   
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)   
            if results.pose_landmarks:
                keypoints = [
                    [landmark.x * frame.shape[1], landmark.y * frame.shape[0], landmark.z]
                    for landmark in results.pose_landmarks.landmark
                ]
                keypoints = np.array(keypoints) 
                elapsed_time = time.time() - wait_time
                countdown_time = 2 - int(elapsed_time)
                if elapsed_time < 2:
                    # 顯示倒數計時
                    status_placeholder.write(f"辨識即將開始，剩餘時間: {countdown_time} 秒")
                else:
                    predicted_class, confidence = recognize_action(model, keypoints, class_names)
                    if predicted_class is not None and confidence > 0.8:
                        if predicted_class == dance_sequence[current_step]:
                            current_step += 1
                            frames.append(frame)  # 保存當前動作的影像
                            status_placeholder.write(f"正確! 下一個動作: {dance_sequence[current_step] if current_step < len(dance_sequence) else '完成'}")  
                            wait_time = time.time()  # 重置等待時間
                            time.sleep(1)
                        else:
                            status_placeholder.write(f"請做出動作: {dance_sequence[current_step]}")
            # 顯示攝像頭畫面
            frame_placeholder.image(frame, channels="BGR")  
        cap.release()
        cv2.destroyAllWindows()
        st.write("舞蹈動作辨識完成")
        st.write(f"花費時間: {time.time() - start_time:.2f} 秒")
        time.sleep(2)
        # 保存影像數據到 session state
        st.session_state['frames'] = frames
        st.session_state['dance_sequence'] = dance_sequence
        st.switch_page("pages/summary.py")  
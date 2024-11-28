import numpy as np
import cv2

def keypoints_to_image(keypoints, image_size=(256, 256), point_radius=5):
    body_keypoints = keypoints[11:]  # 排除前11個臉部關鍵點 
    # 計算縮放比例
    x_min = np.min(body_keypoints[:, 0])
    x_max = np.max(body_keypoints[:, 0])
    y_min = np.min(body_keypoints[:, 1])
    y_max = np.max(body_keypoints[:, 1])
    scale_x = image_size[0] / (x_max - x_min)
    scale_y = image_size[1] / (y_max - y_min)
    # 將座標縮放到圖片大小範圍內
    body_keypoints[:, 0] = (body_keypoints[:, 0] - x_min) * scale_x
    body_keypoints[:, 1] = (body_keypoints[:, 1] - y_min) * scale_y
    # 獲取 z 值的最小值和最大值
    z_min = np.min(body_keypoints[:, 2])
    z_max = np.max(body_keypoints[:, 2])
    # 創建空白圖片
    image = np.zeros(image_size, dtype=np.uint8)
    # 繪製關鍵點
    for (x, y, z) in body_keypoints:
        intensity = int(255 * (z - z_min) / (z_max - z_min))  # 將 z 值縮放到 0-255 範圍內
        cv2.circle(image, (int(x), int(y)), point_radius, intensity, -1)
    return image

X = np.load("X3t.npy")
px = []
print(X.shape)
for i in range(X.shape[0]):
    image = keypoints_to_image(X[i])
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    px.append(image)
px = np.array(px)
print(px.shape)
np.save("X22point_picture.npy", px)
# # cv2.destroyAllWindows()



# def keypoints_to_image(keypoints, image_size=(256, 256), point_radius=5):
#     x_min, y_min = np.min(keypoints[:, :2], axis=0)
#     x_max, y_max = np.max(keypoints[:, :2], axis=0)
#     # 計算縮放比例
#     scale_x = image_size[0] / (x_max - x_min)
#     scale_y = image_size[1] / (y_max - y_min)
#     # 將座標縮放到圖片大小範圍內
#     keypoints[:, 0] = (keypoints[:, 0] - x_min) * scale_x
#     keypoints[:, 1] = (keypoints[:, 1] - y_min) * scale_y
#     # 獲取 z 值的最小值和最大值
#     z_min = np.min(keypoints[:, 2])
#     z_max = np.max(keypoints[:, 2])
#     # 創建空白圖片
#     image = np.zeros(image_size, dtype=np.uint8)
#     # 繪製關鍵點
#     for (x, y, z) in keypoints:
#         intensity = int(255 * (z - z_min) / (z_max - z_min))  # 將 z 值縮放到 0-255 範圍內
#         cv2.circle(image, (int(x), int(y)), point_radius, intensity, -1)
#     return image
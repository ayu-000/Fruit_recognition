# -*- coding: utf-8 -*-
# @Time    : 2024/5/8 13:45
# @Author  : lpy
# @File    : test_base64.py
# @Description :
import cv2
import base64
import numpy as np

def img_to_base64(img_array):
    # 转换为base64
    base64_str = (base64.b64encode(img_array)
                  .decode("ascii")
                )
    return base64_str

def base64_to_img(base64_str):
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)  # 将base64转换为二进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")  # 二进制转换为一维数组
    return encode_image

if __name__ == '__main__':
    img = cv2.imread(r'../static/image/chengzi.jpg')
    img_base64 = img_to_base64(img)
    print(img_base64)
    mask = base64_to_img(img_base64)
    mask = mask.reshape(img.shape)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)


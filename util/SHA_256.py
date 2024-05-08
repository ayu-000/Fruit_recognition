# -*- coding: utf-8 -*-
# @Time    : 2024/4/9 12:11
# @Author  : lpy
# @File    : SHA_256.py
# @Description :数据库加密算法----SHA_256加密

import hashlib

def hash_password(password):
    # 使用 SHA-256 进行密码哈希
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# 原始密码
password = "mysecretpassword"

# 加密密码
hashed_password = hash_password(password)
print(hashed_password)

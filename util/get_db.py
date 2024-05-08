# -*- coding: utf-8 -*-
# @Time    : 2024/4/9 9:59
# @Author  : lpy
# @File    : get_db.py
# @Description :
from DataBase import SessionLocal


def get_db():
    def db_callable():
        # 这里放置获取数据库会话的逻辑
        db = SessionLocal()
        return db
    return db_callable
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/8 19:36
# @Author  : lpy
# @File    : crud.py
# @Description :数据库的CRUD操作


from sqlalchemy.orm import Session
from util import model, schemas


def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.is_del==0).filter(model.User.user_id == user_id).first()

def get_user_By_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.is_del==0).filter(model.User.email == email).first()


def get_user_By_name(db: Session, name: str):
    return db.query(model.User).filter(model.User.is_del==0).filter(model.User.username == name).first()

def create_user(db: Session, user: schemas.CreateUser):
    db_user = model.User(**user.model_dump())
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def create_his(db: Session, his: schemas.CreateHistory):
    db_his = model.History(**his.model_dump())
    print(db_his)
    db.add(db_his)
    db.commit()
    db.refresh(db_his)
    return db_his


def get_history_By_id(db: Session, user_id: int):
    return db.query(model.History).filter(model.History.is_del==0).filter(model.History.user_id == user_id ).all()

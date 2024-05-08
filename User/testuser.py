#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/8 19:57
# @Author  : lpy
# @File    : testuser.py
# @Description :测试API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from util import schemas, crud
from util.DataBase import engine, Base
from util.get_db import get_db

testapp=APIRouter()
Base.metadata.create_all(bind=engine)

@testapp.post("/getuser/{user_id}", response_model=schemas.ReadUser)
def get_user(user_id:int,db:Session=Depends(get_db())):
    db_user= crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_user

@testapp.post("/createuser", response_model=schemas.CreateUser)
def createUser(user: schemas.CreateUser, db:Session=Depends(get_db())):
    return crud.create_user(db=db, user=user)
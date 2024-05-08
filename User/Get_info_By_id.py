# -*- coding: utf-8 -*-
# @Time    : 2024/4/9 12:41
# @Author  : lpy
# @File    : Get_info_By_id.py
# @Description :根据id获取用户信息
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter
from util import crud, schemas
from util.get_db import get_db
user_2=APIRouter()
@user_2.get('/getuser/{user_id}', response_model=schemas.ReadUser)
def get_user(user_id:int,db:Session=Depends(get_db())):
    db_user= crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

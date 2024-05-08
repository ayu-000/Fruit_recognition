# -*- coding: utf-8 -*-
# @Time    : 2024/4/27 8:26
# @Author  : lpy
# @File    : history.py
# @Description :
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter
from util import crud, schemas
from util.get_db import get_db
history=APIRouter()
@history.get('/gethistory/{user_id}', response_model=List[schemas.ReadHistory])
def get_user(user_id:int,db:Session=Depends(get_db())):
    db_history= crud.get_history_By_id(db, user_id=user_id)
    if db_history is None:
        raise HTTPException(status_code=404, detail="User not found")
    reversed_history = list(reversed(db_history))  # 创建一个新的倒序排列的历史记录列表
    print(reversed_history)

    return reversed_history

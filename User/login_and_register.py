import random,re,uuid,string
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from util import schemas, crud
from util.get_db import get_db
from util.SHA_256 import hash_password
user=APIRouter()
def generate_random_username(length=16):
    # 定义可用于生成用户名的字符集合
    characters = string.ascii_letters + string.digits

    # 从字符集合中随机选择字符来生成用户名
    username = ''.join(random.choice(characters) for _ in range(length))

    return username
def reg_validate(mode:str, user: schemas.CreateUser, db:Session):#注册信息校验
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # 邮箱校验
    password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d).+$'
    if not re.match(password_pattern, user.password):  # 密码校验
        return 422, "密码格式错误"
    if user.email != '' and not re.match(email_pattern, user.email):
        return 422, "邮箱格式错误"

    if mode=='register':
        if user.email !='' and crud.get_user_By_email(db=db, email=user.email) is not None:
            return 422,"邮箱已绑定其他账号"
        if crud.get_user_By_name(db=db, name=user.username) is not None:
            return 422,"用户名已存在"
        return 200,"注册成功！"
    else:
        user_1= crud.get_user_By_name(db=db, name=user.username)
        user_2= crud.get_user_By_email(db=db, email=user.email)
        user.password = hash_password(user.password)
        if user_1 is None and user_2 is None:
            return 422,"用户名或邮箱未注册"
        if user.username!='' :
            if user.password==user_1.password:
                return 200,"登录成功！/"+str(user_1.user_id)
            else:
                return 422,"密码错误"
        if user.email!='':
            if user.password==user_2.password:
                return 200,"登录成功！/"+str(user_2.user_id)
            else:
                return 422, "密码错误"

@user.post("/register")#注册
def register(user: schemas.CreateUser, db:Session=Depends(get_db())):
    #随机生成uuid
    user.uuid=uuid.uuid4()
    # 如果没有填写用户名，则随机生成用户名
    if user.username=='':
        user.username='user_' + generate_random_username()
    #用户名，邮箱，密码校验
    code,detail=reg_validate("register",user,db)
    print(code,detail)
    #注册失败，发送失败代码和详情
    if code != 200:
        return {
            "code":code,
            "detail":detail
        }
    #注册成功，发送用户user_id和username
    else :
        user.password=hash_password(user.password)
        new_user= crud.create_user(db=db, user=user)
        return {
                "code":code,
                'detail':detail,
                'user_id':new_user.user_id,
                'username':new_user.username
                }
@user.post("/login")
def get_user(user: schemas.CreateUser, db:Session=Depends(get_db())):
    #数据校验
    code, detail = reg_validate("login",user, db)
    if code != 200:
        return {
            "code":code,
            "detail":detail
        }
    else:
        new_user = detail.split('/')[1]
        detail = detail.split('/')[0]
        return {
            "code": code,
            'detail': detail,
            'user_id':new_user
        }
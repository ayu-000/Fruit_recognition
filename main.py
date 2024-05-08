from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from User import testapp,user,user_2
from eval import evl
from history import history
from fastapi.staticfiles import StaticFiles
app = FastAPI()
# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user,prefix='/user',tags=['登陆注册模块'])
app.include_router(user_2,prefix='/user',tags=['用户模块'])
app.include_router(testapp,prefix='/usertest',tags=['用户测试模块'])
app.include_router(evl,prefix='/evl',tags=['图片预测模块'])
app.include_router(history,prefix='/history',tags=['历史记录模块'])
# Dependency
@app.get("/")
async def root():
    return {"message": "100 World"}

#
# @app.get("/hello/{name}")
# async def say_hello(name: str,query: Optional[str]=None):
#     return {"message": f"Hello {name}{query}"}
#
# @app.put("/{city}")
# def put_city(city:str):
#     return {"message":f"{city}"}
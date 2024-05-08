from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库引擎
engine = create_engine("mysql://root:111111@localhost:3306/fruit")

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine)

# 创建会话
session = SessionLocal()
# 创建基本映射类
Base = declarative_base()

# 定义查询语句
# stmt = text('SELECT user_id FROM user')
#
# # 使用数据库引擎执行查询
# with engine.connect() as connection:
#     result = connection.execute(stmt)
#
#     # 获取查询结果
#     for row in result:
#         user_id = row[0]
#         print(user_id)
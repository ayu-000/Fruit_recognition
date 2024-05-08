# -*- coding: utf-8 -*-
# @Time    : 2024/4/8 17:37
# @Author  : lpy
# @File    : model.py
# @Description :创建模型类
from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from DataBase import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(225), unique=True, nullable=False, comment='唯一id')
    user_type = Column(Boolean, nullable=False, comment="用户类型")
    username = Column(String(225), nullable=False, comment="用户名")
    email = Column(String(225), nullable=False, comment="邮箱")
    password = Column(String(225), nullable=False, comment="密码")
    history = relationship('History', back_populates='user')  # 'Data'是关联的类名；back_populates来指定反向访问的属性名称
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_del = Column(Boolean, default=0, comment="是否删除")


class History(Base):
    __tablename__ = 'history'
    record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    image_url = Column(String(225), nullable=False, comment="图片url")
    result_type = Column(String(225), nullable=False, comment="图片类别")
    result = Column(String(225), nullable=False, comment="识别结果（详细）")
    device = Column(String(225), nullable=False, comment="设备")
    algorithm_used = Column(String(225), nullable=False, comment="使用算法")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_del = Column(Boolean, default=0, comment="是否删除")
    user = relationship('User', back_populates='history')  # 'Data'是关联的类名；back_populates来指定反向访问的属性名称

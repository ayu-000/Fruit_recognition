from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class CreateHistory(BaseModel):  # 定义历史数据类
    user_id: int
    image_url: str
    result_type: str
    result: str
    device: str
    algorithm_used: Optional[str] = 'resnet50'


class CreateUser(BaseModel):  # 定义用户数据类
    uuid: Optional[str] = ''
    user_type: Optional[bool] = False
    username: Optional[str] = ''
    email: Optional[str] = ''
    password: str


class ReadUser(CreateUser):
    user_id: int
    uuid: str
    user_type: int
    username: str
    email: str
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


class ReadHistory(BaseModel):
    record_id: int
    user_id: int
    image_url: str
    result_type: str
    result: str
    device: str
    algorithm_used: str
    create_time: Optional[datetime]
    update_time: Optional[datetime]

    class Config:
        from_attributes = True


class ImageData(BaseModel):
    base64_data: str
    user_id: int
    device: str
    algorithm_used: str

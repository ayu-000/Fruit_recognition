import io
import os
import torch
import torchvision.transforms as transforms
import timm
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
from util import schemas, crud
from util.get_db import get_db
import cv2
import base64
import numpy as np

from util.schemas import ImageData

# 设置保存图片的目录
UPLOAD_FOLDER = 'static/image'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
infer_path = ['./output_dir_pretrained/modelA.pth',
              './output_dir_pretrained/modelA_Augmentation.pth',
              './output_dir_pretrained/modelB.pth',
              './output_dir_pretrained/modelB_Augmentation.pth'
              ]
evl = APIRouter()


def infer_image(image_data, model, image_path):
    image = cv2.imread(image_path)
    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_LANCZOS4)
        image = transforms.ToTensor()(image)
        image = image.unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(image)

        class_names = ['苹果', '牛油果', '香蕉', '樱桃', '火龙果',
                       '葡萄', '柠檬', '芒果', '荔枝', '橙子',
                       '梨', '凤梨', '草莓', '橘子', '西瓜']

        output = torch.nn.functional.softmax(output, dim=-1)
        class_idx = torch.argmax(output, dim=1)[0]
        score = torch.max(output, dim=1)[0][0]
        predicted_class = class_names[class_idx.item()]
        accuracy = round(score.item() * 100, 2)  # 保留两位小数
        return {
            'code': 200,
            "user_id": image_data.user_id,
            "image_url": image_path,
            "result": f'准确率: {accuracy}%',
            "result_type": predicted_class,
            "device": image_data.device,
            "algorithm_used": image_data.algorithm_used
        }
    else:
        return {"code": 400, "message": "Error: Unable to load the image."}


@evl.post('/')
def evl_img(image_data: ImageData, db: Session = Depends(get_db())):
    print(image_data.user_id)
    # 检查是否有前缀
    base64_data = image_data.base64_data
    if base64_data.startswith("data:"):
        # 去除前缀`
        _, _, base64_data = base64_data.partition(",")
    # 将二进制数据保存为图像文件
    # 解码 base64 编码的图片
    image_bytes = base64.b64decode(base64_data)
    # 生成图片文件名
    filename = f'img+{len(os.listdir(UPLOAD_FOLDER)) + 1}.jpg'
    file_path = UPLOAD_FOLDER + '/' + filename
    # 将图片数据保存到文件
    with open(file_path, 'wb') as f:
        f.write(image_bytes)

    model = timm.create_model('resnet50', pretrained=False, num_classes=15)
    if image_data.algorithm_used == 'ModelA':
        model_path = infer_path[0]
    else:
        if image_data.algorithm_used == 'ModelA_Augmentation':
            model_path = infer_path[1]
        else:
            if image_data.algorithm_used == 'ModelB':
                model_path = infer_path[2]
            else:
                model_path = infer_path[3]
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint.state_dict())
    model.eval()

    res = infer_image(image_data, model, file_path)
    evl_save_history(res, db)

    return res


def evl_save_history(res, db: Session):
    # 实现保存推理历史的具体功能，例如将推理结果存储到数据库或文件中
    history = schemas.CreateHistory(user_id=res["user_id"],
                                    image_url=res["image_url"],
                                    result_type=res["result_type"],
                                    result=res["result"],
                                    device=res["device"],
                                    algorithm_used=res["algorithm_used"])
    new_history = crud.create_his(db=db, his=history)
    print("新增历史记录")

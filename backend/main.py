from typing import Annotated
import time
import os
import uuid
import shutil

from fastapi import FastAPI, Form, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from backend.schemas import (UploadCodeResponse, ClearCodeRequest, CheckCodeRequest,
                             CheckersResponse)
from backend.config import STATIC_DIR, FILES_DIR


app = FastAPI()
# 后端API
api = FastAPI(root_path="/api/v1")


@api.get("/code/checkers", response_model=CheckersResponse, summary="获取指定编程语言支持的检查器")
def get_checkers(language: str):
    if language != "C++":
        raise HTTPException(status_code=404, detail=f"不支持{language}的检查器")
    return {
        "data": [{
            "name": "全部",
            "value": "all"
        }, {
            "name": "函数禁用",
            "value": "forbidFunc"
        }, {
            "name": "精度丢失",
            "value": "precisionLoss"
        }]
    }


@api.post("/code/upload", response_model=UploadCodeResponse, summary="上传待检查的代码文件")
def upload_code(file: Annotated[bytes, File()], filename: Annotated[str, Form()]):
    """上传文件，采用本地存储方案"""
    dir_name = f"{str(int(time.time()))}-{str(uuid.uuid4())}"
    saved_path = os.path.join(FILES_DIR, dir_name)
    if not os.path.exists(saved_path):
        os.makedirs(saved_path)

    with open(os.path.join(saved_path, filename), 'wb') as fd:
        fd.write(file)
    return {"uuid": dir_name}


@api.post("/code/clear", response_model=None, summary="删除本次上次的代码文件")
def delete_code(file: ClearCodeRequest):
    """删除指定目录下的代码文件，路径已经确保安全"""
    saved_path = os.path.join(FILES_DIR, file.uuid)
    if not os.path.exists(saved_path):
        return

    # 全删
    if file.filename is None:
        shutil.rmtree(saved_path)
    else:
        os.remove(os.path.join(saved_path, file.filename))


@api.post("/code/check", response_model=None, summary="开始进行代码检查")
def check_code(check_in: CheckCodeRequest):
    pass


# 前端路由
frontend = FastAPI()


@frontend.middleware("http")
async def default_page(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        if STATIC_DIR:
            return FileResponse(os.path.join(STATIC_DIR, "index.html"))
    return response

if STATIC_DIR and os.path.isdir(STATIC_DIR):
    frontend.mount("/", StaticFiles(directory=STATIC_DIR), name="app")


# 挂载前端、后端api
app.mount("/api/v1", app=api)
app.mount("/", app=frontend)


from typing import Annotated
import time
import os
import uuid
import shutil
import json
import asyncio

from fastapi import FastAPI, Form, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from backend.schemas import UploadCodeResponse, ClearCodeRequest, CheckersResponse
from backend.config import STATIC_DIR, FILES_DIR

checkers_map = {
    "awesomeprefixcheck": {
        "name": "函数命名必须有awesome",
        "type": "TIDY",
        "lib": "clang-tidy-plugin/build/lib/libAwesomePrefixCheck.so",
        "category": "coveo"
    },
    "snprintfargcountcheck": {
        "name": "snprintf函数占位符与参数个数不一致",
        "type": "TIDY",
        "lib": "clang-tidy-plugin/build/lib/libSnprintfArgCount.so",
        "category": "hs"
    },
    "assignmistakebyequalcheck": {
        "name": "赋值语句误用==",
        "type": "TIDY",
        "lib": "clang-tidy-plugin/build/lib/libAssignMistakeByEqual.so",
        "category": "hs"
    },
    "conditionmistakebyassigncheck": {
        "name": "条件判断语句中误用赋值",
        "type": "TIDY",
        "lib": "clang-tidy-plugin/build/lib/libConditionMistakeByAssign.so",
        "category": "hs"
    },
    "fileforgetclosecheck": {
        "name": "文件句柄close异常",
        "type": "CSA",
        "lib": "clang-tidy-plugin/build/lib/libFileForgetClose.so",
        "category": "hs"
    }
}
websocket_connects = {}  # 用于管理检查之后需要通知的链接
app = FastAPI()
# 后端API
api = FastAPI(root_path="/api/v1")


@api.get("/code/checkers", response_model=CheckersResponse, summary="获取指定编程语言支持的检查器")
def get_checkers(language: str):
    if language != "C++":
        raise HTTPException(status_code=404, detail=f"不支持{language}的检查器")
    return {
        "data": [{"name": value["name"], "value": key} for key, value in checkers_map.items()]
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """开始检查代码，并将结果告知web"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            if not request["uuid"]:
                await websocket.send_text("请先上传待检查的文件！")
            else:
                # websocket_connects[websocket] = request["uuid"]
                result = await execute_task(request)
                await websocket.send_text(result)
    except WebSocketDisconnect:
        pass
        # if websocket in websocket_connects:
        #     websocket_connects.pop(websocket)


async def execute_task(req):
    checker_name = req["checkerName"]
    category = checkers_map[checker_name]["category"]
    lib_path = checkers_map[checker_name]["lib"]
    checker_type = checkers_map[checker_name]["type"]
    target_path = os.path.join(FILES_DIR, req["uuid"])
    if checker_type == "CSA":
        command = f'clang-16 -fsyntax-only -fplugin={lib_path} -Xclang -analyze -Xclang -analyzer-checker={category}.{checker_name} {target_path}/*.cpp'
    elif checker_type == "TIDY":
        command = f'clang-tidy-16 --checks="{category}-{checker_name}" --load {lib_path} {target_path}/*.cpp'
    else:
        return f"检查失败，【{checker_name}】不支持该类型【{checker_type}】的检查"

    async def run_subprocess() -> str:
        """异步执行shell命令"""
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )
        stdout, stderr = await process.communicate()
        return stdout.decode() if stdout else ""

    # 特殊处理：没有编译命令时，删除前6行
    res = await run_subprocess()
    if checker_type == 'TIDY' and res.startswith("Error while trying to load a compilation database:"):
        lines = res.split('\n')
        res = '\n'.join(lines[6:])
    return res


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


from pydantic import BaseModel, constr
from datetime import datetime


class MyBaseModel(BaseModel):
    class Config:
        from_attributes = True  # orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        # datetime 的格式
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
        }


class UploadCodeResponse(MyBaseModel):
    uuid: str


class ClearCodeRequest(MyBaseModel):
    filename: str | None = None
    uuid: constr(pattern=r"^\d{10}-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$")  # 防止路径遍历攻击


class CheckCodeRequest(MyBaseModel):
    uuid: constr(pattern=r"^\d{10}-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$")
    language: str
    checkerName: str


class CheckerBase(MyBaseModel):
    name: str
    value: str


class CheckersResponse(MyBaseModel):
    data: list[CheckerBase]

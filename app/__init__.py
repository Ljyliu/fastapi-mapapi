from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.v1.api import api_v1
from app.core.exceptions import CustomException
import re

def create_app() -> FastAPI:
    app = FastAPI()

    # 自定义错误处理（业务异常）
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request, exc: CustomException):
        return JSONResponse(status_code=exc.code, 
                            content={"msg": exc.msg,
                                     "data": None,
                                     "code": exc.code})

    # HTTP错误处理（FastAPI抛出的错误）
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        msg_map = {
            "Not authenticated": "请先登录",
            "Could not validate credentials": "登录已过期，请重新登录",
            "Invalid authentication credentials": "登录信息无效",
            "Forbidden": "无权限访问",
            "Gateway Timeout": "请求超时",
            "Too Many Requests": "请求过于频繁，请稍后再试",
        }
        msg = msg_map.get(exc.detail, exc.detail)

        if exc.status_code in (404, 405, 413, 415):
            msg = "请求异常，请稍后重试"


        return JSONResponse(status_code=exc.status_code, 
                            content={"msg": msg,
                                     "data": None,
                                     "code":exc.status_code})

    # 参数错误处理 字段缺失（Pydantic抛出的错误）
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        msg_map = {
            "field required": "不能为空",
            "Field required": "不能为空",
            "String should have at least": "长度不能少于",
            "String should have at most": "长度不能超过",
            "value is not a valid email address": "邮箱格式不正确",
            "Input should be a valid string": "必须是字符串",
            "Input should be a valid integer": "必须是整数",
            "Input should be a valid number": "必须是数字"
        }

        field_map = {
            "username": "用户名",
            "password": "密码",
            "email": "邮箱",
            "phone": "手机号",
            "name": "姓名",
            "address": "地址",
            "remark": "备注"
        }

        # 获取第一条错误信息
        first_error = exc.errors()[0]
        # 获取信息中的错误位置的字段名
        field = first_error["loc"][-1]
        # 获取字段的中文映射
        field = field_map.get(field, field)
        # 英文原始错误信息
        err_msg = first_error["msg"]

        for en_key,cn_msg in msg_map.items():
            if en_key in err_msg:
                numbers = re.findall(r'\d+', err_msg) # 正则匹配数字(多个)
                if numbers:
                    err_msg = f"{cn_msg} {numbers[0]} 位"
                else:
                    err_msg = cn_msg  # 没有数字，直接中文
                break
        
        return JSONResponse(status_code=422, 
                            content={"msg": f"{field}: {err_msg}",
                                     "data": None,
                                     "code": 422})

    # 兜底错误处理
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception):
        return JSONResponse(status_code=500, 
                            content={"msg": f"服务器错误: {str(exc)}",
                                     "data": None,
                                     "code": 500})
    
    app.include_router(api_v1, prefix="/api/v1")

    return app
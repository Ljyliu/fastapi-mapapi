from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.v1.api import api_v1
from app.core.exceptions import CustomException

def create_app() -> FastAPI:
    app = FastAPI()

    # 自定义错误处理
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request, exc: CustomException):
        return JSONResponse(status_code=200, 
                            content={"msg": exc.message,
                                     "code": exc.code,
                                     "data": None})

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception):
        return JSONResponse(status_code=200, 
                            content={"msg": f"服务器错误: {str(exc)}",
                                     "code": -1,
                                     "data": None})
    
    app.include_router(api_v1, prefix="/api/v1")

    return app
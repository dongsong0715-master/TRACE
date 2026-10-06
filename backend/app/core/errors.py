from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException


class AppError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message


def success(request: Request, data: Any):
    return {"data": data, "request_id": request.state.request_id}


def error_response(request: Request, status: int, code: str, message: str):
    return JSONResponse(
        status_code=status,
        content={
            "error": {"code": code, "message": message},
            "request_id": request.state.request_id,
        },
    )


def install_error_handlers(app):
    @app.exception_handler(AppError)
    async def business_error(request: Request, exc: AppError):
        return error_response(request, exc.status, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        # Do not echo request bodies (especially passwords) into responses or logs.
        return error_response(request, 422, "VALIDATION_ERROR", "输入格式不正确，请检查字段")

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return error_response(request, exc.status_code, "HTTP_ERROR", "请求无法处理")

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):
        return error_response(request, 503, "DATABASE_UNAVAILABLE", "数据库暂不可用，请稍后重试")

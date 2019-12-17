#-*- coding: utf-8 -*-

from fastapi import APIRouter
from app.message import response
from starlette.status import HTTP_200_OK

router = APIRouter()


@router.get("/health", status_code=HTTP_200_OK)
async def health_check():
    check_result = response.HealthCheckResponse().message

    return {"message": check_result}

#-*- coding: utf-8 -*-

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "This is root."}

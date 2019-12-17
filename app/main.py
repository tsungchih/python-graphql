# -*- coding: utf-8 -*-

"""
.. module:: main
   :synopsis: The main program of fastapi-test.

.. moduleauthor:: George T. C. Lai
"""

#import graphene

from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.api.routes import api_router
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware


def init_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router)
    return application

app = init_application()

# Configure CORS
'''
origins = [
    "http://localhost",
    "https://localhost:443",
    "https://localhost:10443"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
'''







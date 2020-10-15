#-*- coding: utf-8 -*-

import aiohttp
import asyncio
import logging
import ssl
from fastapi import APIRouter
from graphene import Schema
from app.models.schema.pm25 import PM25Query
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.status import HTTP_200_OK
from timeit import default_timer as timer

# Configure SSL Context
FORCED_CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES'
)
sslcontext = ssl.create_default_context()
sslcontext.options |= ssl.OP_NO_SSLv3
sslcontext.options |= ssl.OP_NO_SSLv2
sslcontext.options |= ssl.OP_NO_TLSv1_1
sslcontext.options |= ssl.OP_NO_TLSv1_2
sslcontext.options |= ssl.OP_NO_TLSv1_3
sslcontext.set_ciphers(FORCED_CIPHERS)


router = APIRouter()

pm25_schema = Schema(query=PM25Query)

@router.get("/pm25/{county}", tags=["environment"], status_code=HTTP_200_OK)
async def pm25(county: str):
    start_time = timer()
    query_string = """
        query getPM25Info($county: String) {
            uv(county: $county) {
                county
                siteName
                uvi
                wgs84Lat
                wgs84Lon
            }
            pm10(county: $county) {
                county
                siteName
                pm10
                unit
            }
        }
    """
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        result = await pm25_schema.execute(
            query_string,
            context={
                'session': session,
                'sslctx': sslcontext
            },
            executor=AsyncioExecutor(loop=asyncio.get_running_loop()),
            return_promise=True,
            variables={"county": county})
    if result.errors is not None:
        logging.error(result.errors)
    end_time = timer()
    logging.info("The API pm25 spent time: {}".format(end_time - start_time))
    return {"message": result.data}

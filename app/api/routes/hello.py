#-*- coding: utf-8 -*-

import logging

from fastapi import APIRouter
from graphene import Schema
from app.models.schema.book import Query
from starlette.status import HTTP_200_OK

schema = Schema(query=Query)

router = APIRouter()

@router.get("/hello/{name}", status_code=HTTP_200_OK)
async def hello(name: str):
    """The function is used to demonstrate GraphQL.

    :param name: name
    :type name: str
    :return: message
    :rtype: str
    """

    #query_string = '{{ hello(name: "{who}") }}'.format(who=name)
    query_string = """
        query getBook($name: String) {
            hello(name: $name) {
                title
                author
            }
        }
    """
    result = schema.execute(query_string, variables={"name": name})
    logging.error(result.errors)
    return {"message": result.data['hello']}

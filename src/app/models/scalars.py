#-*- coding: utf-8 -*-

import datetime
from graphene.types import Scalar
from graphql.language import ast


class DateTime(Scalar):
    """The Custom scalar DateTime.

    :param Scalar: [description]
    :type Scalar: [type]
    """
    @staticmethod
    def serialize(dt):
        return dt.isoformat()

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, "%Y-%m-%dT%H:%M:%S.%f")
    
    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

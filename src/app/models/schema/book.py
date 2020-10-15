#-*- coding: utf-8 -*-


from graphene import String, List, ObjectType

class Book(ObjectType):
    title = String(description="book name")
    author = String(description="author name")



class Query(ObjectType):
    book = String(title=String(default_value="stranger"))
    hello = List(Book, name=String(default_value="stranger"))
    goodbye = String()

    def resolve_book(root, info, title: str):
        return Book(title=title, author="George")

    def resolve_hello(root, info, name: str):
        return [Book(title="Python in Action", author="George"), Book(title="Scala in action", author="Steven")]

    def resolve_goodbye(root, info):
        return 'See ya!!!'

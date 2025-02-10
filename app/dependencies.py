# app/dependencies.py
from fastapi import Query

def query_dependency(q: str = Query(None, max_length=50)):
    return q

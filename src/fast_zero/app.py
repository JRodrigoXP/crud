from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import UserPublic, UserSchema, UserList, Message


app = FastAPI()
database = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}



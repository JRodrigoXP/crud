from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.database import get_session

app = FastAPI()


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session=Depends(get_session)):
    users = session.scalars(select(User)).all()
    return {'users': users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int):
    if user_id <= 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    # a session é criada e passada como dependência para a função create_user
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already registered',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    session.add(db_user)  # adicionando o usuário à sessão
    session.commit()  # validação das alterações no banco de dados
    session.refresh(db_user)  # atualizando o objeto com os dados do banco

    return db_user


@app.put('/users/{user_id}', status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserSchema):
    if user_id <= 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    existing_user = database[user_id - 1]

    for other_user in database:
        if other_user.id == existing_user.id:
            continue
        if other_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )
        if other_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already registered',
            )

    existing_user.username = user.username
    existing_user.email = user.email
    existing_user.password = user.password
    return {'username': existing_user.username, 'email': existing_user.email}


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id <= 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]
    return {'message': 'User deleted'}

from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'user': database}


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
def create_user(user: UserSchema):
    for existing_user in database:
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already registered',
            )
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already registered',
            )
    user_id = len(database) + 1
    user_db = UserDB(id=user_id, **user.model_dump())
    database.append(user_db)
    return {
        'id': user_db.id,
        'username': user_db.username,
        'email': user_db.email,
    }


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


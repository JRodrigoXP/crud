from fast_zero.models import User, table_registry

from sqlalchemy import select
from sqlalchemy.orm import Session


def test_create_user(session):
    user = User(username='Rodrigo', email='ro@oli.com', password='tamenega')
    session.add(user)  # cria
    session.commit()  # persiste
    response = session.scalar(select(User).where(User.email == 'ro@oli.com'))
    assert response.username == 'Rodrigo'

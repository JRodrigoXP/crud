import pytest
from fast_zero.models import User, table_registry

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')  # conexão com o banco
    table_registry.metadata.create_all(engine)  # criação da tabela
    with Session(
        engine
    ) as session:  # instância da session com gerenciamento de contexto
        yield session
    table_registry.metadata.drop_all(engine)

from unittest.mock import AsyncMock, MagicMock

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.db.models.favorite_product_model import FavoriteProduct
from app.main import app

load_dotenv()


@pytest.fixture
def mock_db_session():
    mock = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock
    try:
        yield mock
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True)
def override_get_db(mock_db_session):
    def _get_db_override():
        yield mock_db_session

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_get_current_user():
    def mock_user():
        return {
            "id": 1,
            "name": "Test User",
            "email": "testuser@example.com",
        }

    app.dependency_overrides[get_current_user] = mock_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_product():
    """Mock de um produto válido retornado pela API mockada."""
    return {
        "id": 1,
        "title": "Produto Exemplo A",
        "price": 29.99,
        "image_url": "https://via.placeholder.com/150",
        "review": "Muito bom!",
    }


@pytest.fixture
def mock_requests(mocker):
    """Mock das requisições HTTP para evitar chamadas reais à API."""
    return mocker.patch("requests.get")


@pytest.fixture
def client(mocker):
    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()

    def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture
def favorite_product_entry():
    """Mock de uma entrada no banco de dados."""
    return FavoriteProduct(customer_id=1, product_id=1)


@pytest.fixture
def base_url():
    """URL base da API mockada."""
    return "http://localhost:8000/mock/products"

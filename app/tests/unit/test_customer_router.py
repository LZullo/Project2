from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

mock_user_dependency = patch(
    "app.core.dependencies.get_current_user", return_value="mock_user"
)


def test_create_customer_success():
    """Testa a criação de um novo cliente com dados válidos."""
    mock_customer = {
        "id": 1,
        "name": "Letícia",
        "email": "leticia@example.com",
        "favorites": [],
    }

    with patch(
        "app.router.customer_router.create_customer", return_value=mock_customer
    ), mock_user_dependency:
        response = client.post(
            "/customers/", json={"name": "Letícia", "email": "leticia@example.com"}
        )

        assert response.status_code == 201
        assert response.json() == mock_customer


def test_list_customers_success():
    """Testa a listagem de todos os clientes cadastrados."""
    mock_customers = [
        {"id": 1, "name": "Letícia", "email": "leticia@example.com", "favorites": []},
        {"id": 2, "name": "Ana", "email": "ana@example.com", "favorites": []},
    ]

    with patch(
        "app.router.customer_router.list_customers", return_value=mock_customers
    ), mock_user_dependency:
        response = client.get("/customers/")

        assert response.status_code == 200
        assert response.json() == mock_customers


def test_update_customer_success():
    """Testa a atualização de um cliente existente com novos dados válidos."""
    updated_customer = {
        "id": 1,
        "name": "Letícia Z.",
        "email": "leticia.z@example.com",
        "favorites": [],
    }

    with patch(
        "app.router.customer_router.update_customer", return_value=updated_customer
    ), mock_user_dependency:
        response = client.put(
            "/customers/1/",
            json={"name": "Letícia Z.", "email": "leticia.z@example.com"},
        )

        assert response.status_code == 200
        assert response.json() == updated_customer


def test_delete_customer_success():
    """Testa a remoção de um cliente existente pelo ID."""
    with patch("app.router.customer_router.remove_customer"), mock_user_dependency:
        response = client.delete("/customers/1/")
        assert response.status_code == 204

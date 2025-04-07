import requests_mock

from app.services.product_service import get_product_by_id


def test_get_product_by_id_success(base_url, mock_product):
    """Testa se a função retorna corretamente um produto existente."""
    with requests_mock.Mocker() as mocker:
        mocker.get(
            f"{base_url}/?product_id={mock_product['id']}",
            json=mock_product,
            status_code=200,
        )

        product = get_product_by_id(mock_product["id"])
        assert product == mock_product


def test_get_product_by_id_not_found(base_url):
    """Testa o caso onde o produto não é encontrado na API mockada."""
    product_id = 2

    with requests_mock.Mocker() as mocker:
        mocker.get(f"{base_url}/?product_id={product_id}", status_code=404)

        product = get_product_by_id(product_id)
        assert product is None


def test_get_product_by_id_api_error(base_url):
    """Testa um erro genérico da API."""
    product_id = 3

    with requests_mock.Mocker() as mocker:
        mocker.get(f"{base_url}/?product_id={product_id}", status_code=500)

        product = get_product_by_id(product_id)
        assert product is None

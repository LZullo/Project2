import logging

import requests

MOCK_API_URL = "http://localhost:8000/mock/products/"

logger = logging.getLogger(__name__)


def get_product_by_id(product_id: int):
    """Busca um produto na API mockada e retorna suas informações."""
    try:
        response = requests.get(f"{MOCK_API_URL}?product_id={product_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as e:
        logger.error(f"Erro ao conectar na API de produtos: {e}")
        return None

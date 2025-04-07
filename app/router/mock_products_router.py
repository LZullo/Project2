from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

MOCK_PRODUCTS = {
    1: {
        "id": 1,
        "title": "Produto Exemplo A",
        "price": 29.99,
        "image_url": "https://via.placeholder.com/150",
        "review": "Muito bom!",
    },
    2: {
        "id": 2,
        "title": "Produto Exemplo B",
        "price": 49.90,
        "image_url": "https://via.placeholder.com/150",
        "review": "Produto ok.",
    },
    3: {
        "id": 3,
        "title": "Produto Exemplo C",
        "price": 15.00,
        "image_url": "https://via.placeholder.com/150",
        "review": "Preço justo e boa qualidade.",
    },
    4: {
        "id": 4,
        "title": "Produto Exemplo D",
        "price": 99.99,
        "image_url": "https://via.placeholder.com/150",
        "review": "Produto excelente, recomendo!",
    },
    5: {
        "id": 5,
        "title": "Produto Exemplo E",
        "price": 5.99,
        "image_url": "https://via.placeholder.com/150",
        "review": "Cumpre o que promete.",
    },
    6: {
        "id": 6,
        "title": "Produto Exemplo F",
        "price": 120.50,
        "image_url": "https://via.placeholder.com/150",
        "review": "Produto premium, entrega rápida.",
    },
    7: {
        "id": 7,
        "title": "Produto Exemplo G",
        "price": 8.75,
        "image_url": "https://via.placeholder.com/150",
        "review": "Simples, mas útil.",
    },
    8: {
        "id": 8,
        "title": "Produto Exemplo H",
        "price": 74.20,
        "image_url": "https://via.placeholder.com/150",
        "review": "Acabamento de qualidade.",
    },
    9: {
        "id": 9,
        "title": "Produto Exemplo I",
        "price": 32.40,
        "image_url": "https://via.placeholder.com/150",
    },
    10: {
        "id": 10,
        "title": "Produto Exemplo J",
        "price": 18.30,
        "image_url": "https://via.placeholder.com/150",
    },
}


@router.get("/mock/products/")
def get_mock_product(product_id: Optional[int] = Query(None)):
    """Retorna todos os produtos mockados ou um específico, se informado."""
    if product_id is None:
        return list(MOCK_PRODUCTS.values())

    produto = MOCK_PRODUCTS.get(product_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

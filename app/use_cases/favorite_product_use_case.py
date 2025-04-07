import logging
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.repository.favorite_product_repository import (
    add_favorite_product as db_add_favorite,
    get_favorite_products as db_get_favorites,
    remove_favorite_product as db_remove_favorite,
)
from app.services.product_service import get_product_by_id
from app.schemas.product_schema import ProductBase
from app.schemas.favorite_product_schema import FavoriteListResponse
from app.db.models.favorite_product_model import FavoriteProduct

logger = logging.getLogger(__name__)


def list_favorite_products_use_case(db: Session, customer_id: int) -> FavoriteListResponse:
    favorites = db_get_favorites(db, customer_id)

    favorite_products = []
    for favorite in favorites:
        product_data = get_product_by_id(favorite.product_id)
        if product_data:
            favorite_products.append(ProductBase(**product_data))

    return FavoriteListResponse(
        customer_id=customer_id,
        favorites=favorite_products
    )


def add_favorite_product_use_case(db: Session, customer_id: int, product_id: int) -> ProductBase:
    product_data = get_product_by_id(product_id)
    if not product_data:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    new_fav = FavoriteProduct(
        customer_id=customer_id,
        product_id=product_data["id"],
        title=product_data["title"],
        image_url=product_data["image_url"],
        price=product_data["price"],
        review=product_data.get("review"),
    )

    try:
        _, error = db_add_favorite(db, new_fav)

        if error:
            raise HTTPException(status_code=500, detail="Erro ao adicionar produto aos favoritos.")       

        return ProductBase(**product_data)

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco: {e}")
        raise HTTPException(status_code=500, detail="Erro ao adicionar produto favorito.")


def remove_favorite_product_use_case(db: Session, customer_id: int, product_id: int) -> tuple[ProductBase | None, str | None]:
    try:
        logger.info(f"Removendo produto {product_id} dos favoritos do cliente {customer_id}")

        _, error_message = db_remove_favorite(db, customer_id, product_id)

        if error_message:
            logger.warning(f"Falha ao remover favorito: {error_message}")
            return None, error_message

        product_data = get_product_by_id(product_id)
        if not product_data:
            return None, "Produto removido, mas não encontrado na base externa."

        return ProductBase(**product_data), None

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco ao remover produto favorito: {e}")
        return None, "Erro interno ao remover produto favorito."
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.schemas.favorite_product_schema import (
    FavoriteListResponse,
    FavoriteProductCreate,
)
from app.use_cases.favorite_product_use_case import (
    list_favorite_products_use_case,
    add_favorite_product_use_case,
    remove_favorite_product_use_case,
)

router = APIRouter(tags=["Favorite Products"])


@router.get(
    "/customers/{customer_id}/favorites/",
    response_model=FavoriteListResponse,
    summary="Lista os produtos favoritos de um cliente",
)
def list_favorites(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return list_favorite_products_use_case(db, customer_id)


@router.post(
    "/customers/{customer_id}/favorites/",
    response_model=FavoriteListResponse,
    summary="Adiciona um ou mais produtos à lista de favoritos de um cliente",
)
def add_favorite_products(
    customer_id: int,
    favorite: FavoriteProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    added_products = []
    for product_id in favorite.product_ids:
        try:
            added = add_favorite_product_use_case(db, customer_id, product_id)
            added_products.append(added)
        except IntegrityError:
            db.rollback()
            continue
        except HTTPException as e:
            if len(favorite.product_ids) == 1:
                raise e
            continue

    if not added_products:
        raise HTTPException(status_code=400, detail="Nenhum produto foi adicionado")

    return FavoriteListResponse(customer_id=customer_id, favorites=added_products)


@router.delete(
    "/customers/{customer_id}/favorites/{product_id}/",
    response_model=FavoriteListResponse,
    summary="Remove um produto da lista de favoritos de um cliente",
)
def remove_favorite(
    customer_id: int,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    product, error = remove_favorite_product_use_case(db, customer_id, product_id)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return FavoriteListResponse(customer_id=customer_id, favorites=[product])
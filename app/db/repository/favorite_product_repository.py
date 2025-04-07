from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.favorite_product_model import FavoriteProduct


def get_favorite_products(db: Session, customer_id: int) -> List[FavoriteProduct]:
    return db.query(FavoriteProduct).filter(FavoriteProduct.customer_id == customer_id).all()


def add_favorite_product(db: Session, favorite: FavoriteProduct) -> tuple[FavoriteProduct, str | None]:
    try:
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite, None
    except IntegrityError:
        db.rollback()
        return None, "Produto já está nos favoritos"


def remove_favorite_product(db: Session, customer_id: int, product_id: int):
    favorite = (
        db.query(FavoriteProduct)
        .filter(
            FavoriteProduct.customer_id == customer_id,
            FavoriteProduct.product_id == product_id,
        )
        .first()
    )

    if not favorite:
        return None, "Produto não encontrado na lista de favoritos"

    db.delete(favorite)
    db.commit()
    return favorite, None
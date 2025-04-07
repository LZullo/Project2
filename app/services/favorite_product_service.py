from sqlalchemy.orm import Session

from app.db.repository.favorite_product_repository import \
    add_favorite_product as add_favorite_product_db
from app.db.repository.favorite_product_repository import \
    get_favorite_products as get_favorite_products_db
from app.db.repository.favorite_product_repository import \
    remove_favorite_product as remove_favorite_product_db
# from app.schemas.product_schema import ProductBase
# from app.services.product_service import get_product_by_id


from sqlalchemy.orm import Session
from app.schemas.favorite_product_schema import FavoriteListResponse, AddFavoriteRequest
from app.db.repository import favorite_product_repository
from app.db.models.favorite_product_model import FavoriteProduct
from sqlalchemy.orm import Session
from app.schemas.favorite_product_schema import AddFavoriteRequest, FavoriteListResponse, ProductBase

def get_favorites_service(db: Session, customer_id: int) -> FavoriteListResponse:
    favorites = get_favorite_products_db(db, customer_id)
    return FavoriteListResponse(customer_id=customer_id, favorites=favorites)


def add_favorite_service(db: Session, customer_id: int, favorite_data: AddFavoriteRequest):
    favorite = FavoriteProduct(**favorite_data.dict(), customer_id=customer_id)
    return add_favorite_product_db(db, favorite)



def remove_favorite_product_service(db: Session, customer_id: int, product_id: int):
    """Remove um produto favorito de um cliente."""
    favorite, error = remove_favorite_product_db(db, customer_id, product_id)
    if error:
        return None, error

    product = ProductBase(
        id=favorite.product_id,
        title=favorite.title,
        image_url=favorite.image_url,
        price=favorite.price,
        review=favorite.review,
    )

    return product, None

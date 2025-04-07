from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from app.use_cases.favorite_product_use_case import list_favorite_products_use_case, add_favorite_product_use_case, remove_favorite_product_use_case


def test_list_favorite_products_use_case(mock_db_session, mocker, mock_product):
    mock_favorite = MagicMock()
    mock_favorite.product_id = 1
    mock_db_session.query().filter().all.return_value = [mock_favorite]

    mocker.patch("app.services.product_service.get_product_by_id", return_value=mock_product)

    result = list_favorite_products_use_case(mock_db_session, 1)

    assert result.favorites[0].id == mock_product["id"]


def test_add_favorite_product_use_case_success(mock_db_session, mocker, mock_product):
    mocker.patch(
        "app.services.product_service.get_product_by_id",
        return_value=mock_product  
    )
    mocker.patch(
        "app.db.repository.favorite_product_repository.add_favorite_product",
        return_value=(mock_product, None) 
    )

    result = add_favorite_product_use_case(mock_db_session, 1, 1)

    assert result.id == mock_product["id"]
    assert result.title == mock_product["title"]
    assert result.price == mock_product["price"]
    assert str(result.image_url) == mock_product["image_url"]
    assert result.review == mock_product["review"]

def test_add_favorite_product_use_case_not_found(mock_db_session, mocker):
    mocker.patch("app.services.product_service.get_product_by_id", return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        add_favorite_product_use_case(mock_db_session, 1, 999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Produto não encontrado."

def test_remove_favorite_product_use_case_success(mock_db_session, mocker, mock_product):
    mocker.patch(
        "app.services.favorite_product_service.remove_favorite_product_service",
        return_value=mock_product
    )

    result, error = remove_favorite_product_use_case(mock_db_session, 1, 1)

    assert error is None
    assert result.id == 1




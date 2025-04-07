import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.repository.customer_repository import \
    create_customer as db_create_customer
from app.db.repository.customer_repository import \
    delete_customer as db_delete_customer
from app.db.repository.customer_repository import \
    get_customers as db_get_customers
from app.db.repository.customer_repository import \
    update_customer as db_update_customer
from app.schemas.customer_schema import CustomerResponse
from app.schemas.product_schema import ProductBase

logger = logging.getLogger(__name__)


def create_customer(db: Session, name: str, email: str):
    try:
        logger.info(f"Creating customer with email: {email}")
        customer = db_create_customer(db, name, email)

        return CustomerResponse.model_validate(customer)
    except RuntimeError as e:
        logger.warning(f"Customer creation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        logger.error("Database error while creating customer")
        raise HTTPException(status_code=500, detail="Erro interno ao criar cliente.")


def list_customers(db: Session, email: str = None):
    customers = db_get_customers(db, email)

    customer_responses = []
    for customer in customers:
        favorites = [
            ProductBase(id=fav.product_id) for fav in customer.favorites
        ]  

        customer_responses.append(
            CustomerResponse(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                favorites=favorites
            )
        )
    
    return customer_responses


def update_customer(db: Session, customer_id: int, name: str, email: str):
    try:
        logger.info(f"Updating customer {customer_id}")
        updated_customer = db_update_customer(db, customer_id, name, email)
        return updated_customer
    except RuntimeError as e:
        logger.warning(f"Customer update failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        logger.error("Database error while updating customer")
        raise HTTPException(
            status_code=500, detail="Erro interno ao atualizar cliente."
        )


def remove_customer(db: Session, customer_id: int):
    try:
        logger.info(f"Removing customer {customer_id}")
        customer = db_delete_customer(db, customer_id)
        if not customer:
            logger.warning(f"Customer {customer_id} not found")
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return customer
    except SQLAlchemyError:
        logger.error("Database error while removing customer")
        raise HTTPException(status_code=500, detail="Erro interno ao remover cliente.")

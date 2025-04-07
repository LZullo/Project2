import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.use_cases.customer_use_case import (create_customer, list_customers,
                                             remove_customer, update_customer)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/customers/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    logger.info("Rota /customers/ chamada com dados: %s", customer)
    return create_customer(db, customer.name, customer.email)


@router.get(
    "/customers/",
    response_model=list[CustomerResponse],
)
def list(
    email: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return list_customers(db, email)


@router.put(
    "/customers/{customer_id}/",
    response_model=CustomerResponse,
)
def update(
    customer_id: int,
    updated_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return update_customer(db, customer_id, updated_data.name, updated_data.email)


@router.delete(
    "/customers/{customer_id}/",
    status_code=204,
)
def remove(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    remove_customer(db, customer_id)
    return Response(status_code=204)

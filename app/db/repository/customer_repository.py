from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.customer_model import Customer


def get_customers(db: Session, email: str = None):
    """Retorna todos os clientes ou filtra pelo e-mail, se fornecido."""
    query = db.query(Customer)
    if email:
        query = query.filter(Customer.email == email)
    return query.all()


def create_customer(db: Session, name: str, email: str):
    """Cria o cliente no banco de dados e retorna o objeto cliente com o ID preenchido."""
    if db.query(Customer).filter_by(email=email).first():
        raise RuntimeError(f"O e-mail '{email}' já está cadastrado.")
    customer = Customer(name=name, email=email)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    print(customer.id)
    return customer


def update_customer(db: Session, customer_id: int, name: str, email: str):
    """Atualiza os dados de um cliente existente, garantindo que o novo e-mail não esteja em uso."""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        existing_customer = db.query(Customer).filter(Customer.email == email).first()
        if existing_customer and existing_customer.id != customer.id:
            raise HTTPException(
                status_code=400, detail="E-mail já cadastrado por outro cliente"
            )
        if name:
            customer.name = name
        if email:
            customer.email = email
        db.commit()
        db.refresh(customer)
        return customer
    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise RuntimeError(f"Erro ao atualizar cliente {customer_id}: {str(e)}")


def delete_customer(db: Session, customer_id: int):
    """Remove um cliente pelo ID."""
    try:
        customer = db.query(Customer).filter_by(id=customer_id).first()
        if customer:
            db.delete(customer)
            db.commit()
        return customer
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao deletar cliente {customer_id}: {str(e)}")

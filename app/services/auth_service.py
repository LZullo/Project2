from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (create_access_token, get_password_hash,
                               verify_password)
from app.db.models.user import User
from app.schemas.user_schema import UserCreate


class AuthService:
    @staticmethod
    def register(user_data: UserCreate, db: Session):
        """Cadastra um novo usuário no sistema."""
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")

        hashed_password = get_password_hash(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def authenticate(username: str, password: str, db: Session):
        """Verifica credenciais e gera token JWT."""
        user = db.query(User).filter(User.email == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            {"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

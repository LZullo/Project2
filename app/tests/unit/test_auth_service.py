from unittest.mock import MagicMock

from app.db.models.user import User
from app.schemas.user_schema import UserCreate
from app.services.auth_service import AuthService


def test_register_user(mock_db_session):
    """Testa o registro de um novo usuário diretamente no serviço."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    user_data = UserCreate(email="test@example.com", password="password123")

    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    user = AuthService.register(user_data, mock_db_session)

    assert isinstance(user, User)
    assert user.email == "test@example.com"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

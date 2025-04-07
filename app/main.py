import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

from app.core.config import settings
from app.db.database import engine
from app.router import (auth_router, customer_router, favorite_product_router,
                        mock_products_router)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Produtos Favoritos API",
    description="API para gerenciamento de clientes e seus produtos favoritos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="", tags=["Autentication"])
app.include_router(mock_products_router.router, prefix="", tags=["Mock Products"])
app.include_router(customer_router.router, prefix="", tags=["Customers"])
app.include_router(favorite_product_router.router, prefix="", tags=["Favorites"])


@app.get("/health", tags=["Health"])
def health_check():
    logger.info("Health check solicitado")
    return {"status": "ok"}


def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Banco de dados conectado com sucesso!")
                return
        except OperationalError:
            logger.warning("Banco de dados ainda não disponível. Tentando novamente...")
            time.sleep(3)
            retries -= 1
    logger.error("Não foi possível conectar ao banco de dados.")
    raise RuntimeError("Falha ao conectar ao banco de dados.")


def start_app():
    wait_for_db()


if __name__ == "__main__":
    import uvicorn

    start_app()

    logger.info(f"Iniciando a API em {settings.HOST}:{settings.PORT}")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

# Usa uma imagem oficial do Python
FROM python:3.11-slim AS base

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos necessários
COPY requirements.txt requirements-dev.txt ./

# Instala dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos
COPY . .

# Define comando de entrada para rodar migrações e iniciar API
# ENTRYPOINT ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
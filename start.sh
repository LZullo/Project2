#!/bin/sh

echo "Aguardando o banco iniciar..."
sleep 5

echo "Rodando migrations..."
alembic upgrade head

echo "Iniciando a API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000

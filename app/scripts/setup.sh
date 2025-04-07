#!/bin/bash

set -e  

echo "🔧 Iniciando setup do projeto..."

echo "🛑 Parando containers antigos..."
docker-compose down -v --remove-orphans || true

echo "🚀 Criando e subindo os containers..."
docker-compose up --build -d

echo "⏳ Aguardando banco de dados ficar disponível..."
until docker-compose exec -T db pg_isready -U myuser -d favorite_products >/dev/null 2>&1; do
  sleep 2
done
echo "✅ Banco de dados pronto!"

echo "⏳ Aguardando a API iniciar..."
until curl -s http://localhost:8000/docs >/dev/null 2>&1; do
  echo "⏳ Aguardando a API iniciar..."
  sleep 2
done
echo "✅ API rodando!"

if [ ! "$(ls -A app/migrations/versions 2>/dev/null)" ]; then
  echo "📁 Criando pasta de versões do Alembic dentro do container..."
  docker-compose exec -T api mkdir -p /app/app/migrations/versions

  if [ ! "$(ls -A app/migrations/versions 2>/dev/null)" ]; then
    echo "📜 Criando migração inicial..."
    docker-compose exec -T api alembic revision --autogenerate -m "initial"
  fi
fi

echo "🚀 Aplicando migrações..."
docker-compose exec -T api alembic upgrade head || {
  echo "❌ Erro ao aplicar migrações! Verifique os logs."
  exit 1
}

echo "✅ Setup concluído! A API está rodando em http://localhost:8000 🚀"

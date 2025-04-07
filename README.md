📌 FastAPI Favorite Products
Este projeto consiste em uma API RESTful desenvolvida com FastAPI para gerenciar produtos favoritados por clientes, com foco em performance, boas práticas de arquitetura, autenticação JWT, e uso profissional de ferramentas como Docker, SQLAlchemy, Alembic e Pytest.

🧠 Estratégia para Armazenamento de Produtos Favoritados
Durante o desenvolvimento, optei por armazenar localmente os principais dados do produto favoritado (title, image_url, price e review) na tabela favorite_products, ao invés de consultá-los dinamicamente da API externa de produtos.

✅ Justificativas Técnicas
Desempenho: evitar chamadas repetidas à API mockada reduz significativamente a latência na listagem de favoritos e melhora a escalabilidade do sistema.

Resiliência: com os dados armazenados localmente, a funcionalidade de favoritos permanece estável mesmo que a API externa esteja indisponível.

Congelamento de estado: o sistema registra o estado atual do produto no momento da adição como favorito, permitindo análises históricas e consistência de dados para o usuário.

Simplicidade para o consumidor da API: o frontend ou cliente da API pode exibir os produtos favoritados diretamente, sem realizar chamadas adicionais para complementar os dados.

🔄 Considerações
Essa abordagem pode ocasionar desatualização dos dados dos produtos com o tempo. Caso haja necessidade de consistência em tempo real, a aplicação poderá evoluir para:

Atualizar periodicamente os dados dos produtos.
Realizar sincronização sob demanda.
Ou transformar a API mockada em uma fonte interna com cache distribuído.

🧱 Estrutura do Projeto
A arquitetura está separada por responsabilidades claras:


🚀 Setup do Projeto
O script setup.sh foi criado para simplificar o ambiente de desenvolvimento e garantir consistência entre as máquinas dos avaliadores.

./app/scripts/setup.sh

Esse script realiza as seguintes etapas:

Finaliza containers antigos, se existirem;
Constrói e sobe os containers definidos no docker-compose.yml;
Aguarda o banco PostgreSQL estar disponível;
Aguarda a inicialização da API;
Cria e aplica as migrações do banco automaticamente, utilizando o Alembic;
Finaliza informando que a API está disponível em http://localhost:8000.

⚙️ Tecnologias Utilizadas
📦 Produção
FastAPI, SQLAlchemy, Alembic, Pydantic
PostgreSQL, Docker, Docker Compose
JWT com python-jose, passlib e bcrypt
python-dotenv, pydantic-settings para variáveis de ambiente

🧪 Desenvolvimento e Testes
pytest, pytest-asyncio, pytest-cov, httpx, pytest-mock
black, flake8, isort, mypy para qualidade de código
requests e python-multipart para integrações e testes


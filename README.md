# 📌 FastAPI Favorite Products

This project is a RESTful API built with **FastAPI** to manage customers' favorite products, focusing on performance, clean architecture practices, JWT authentication, and professional use of tools such as Docker, SQLAlchemy, Alembic, and Pytest.

---

## 🧠 Favorite Products Storage Strategy

During development, I chose to store the main data of each favorited product (`title`, `image_url`, `price`, and `review`) locally in the `favorite_products` table, instead of retrieving it dynamically from the external products API.

### ✅ Technical Justifications

- **Performance**: Avoiding repeated calls to the mock API significantly reduces latency when listing favorites and improves system scalability.
- **Resilience**: With the data stored locally, the favorites feature remains stable even if the external API is unavailable.
- **State freezing**: The system stores the product's state at the time it was favorited, allowing for historical analysis and consistent data presentation to the user.
- **Simplified API consumption**: The frontend or API consumer can directly display favorite products without making additional calls to fetch complementary data.

---

## 🔄 Considerations

This approach may lead to outdated product data over time. If real-time consistency is required, the application can evolve to:

- Periodically update product data;
- Perform on-demand synchronization;
- Or convert the mock API into an internal source with distributed caching.

---

## 🧱 Project Structure

The architecture is organized with clearly defined responsibilities to ensure maintainability and scalability.

---

## 🚀 Project Setup

A `setup.sh` script was created to simplify the development environment setup and ensure consistency across reviewers' machines.

```bash
./app/scripts/setup.sh
```
---

## 🛠️ Script Steps

- Stops any existing containers  
- Builds and starts containers from `docker-compose.yml`  
- Waits for the PostgreSQL database to be available  
- Waits for the FastAPI server to initialize  
- Automatically applies database migrations using **Alembic**  
- Informs that the API is ready at [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Technologies Used

### 📦 Production

- **FastAPI**, **SQLAlchemy**, **Alembic**, **Pydantic**
- **PostgreSQL**, **Docker**, **Docker Compose**
- JWT authentication with `python-jose`, `passlib`, `bcrypt`
- Environment management: `python-dotenv`, `pydantic-settings`

### 🧪 Development and Testing

- **Testing**: `pytest`, `pytest-asyncio`, `pytest-cov`, `httpx`, `pytest-mock`
- **Code quality**: `black`, `flake8`, `isort`, `mypy`
- **Integrations**: `requests`, `python-multipart`


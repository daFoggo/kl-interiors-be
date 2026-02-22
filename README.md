# KL Interiors Backend

This project is the Backend (API) for the KL Interiors application, built with Python, FastAPI, SQLAlchemy, and PostgreSQL. The architecture follows the **Bigger Applications** standards recommended by FastAPI, along with best practices for **RESTful API** design.

---

## 🚀 1. Installation and Execution

### Prerequisites

1. **Docker** and **Docker Compose** installed on your machine.
2. Ports **8000** and **5432** must be available (not occupied by other applications).

### Setup and Run

You can easily launch the project using Docker. The environment will automatically include 1 container for the web application (FastAPI) and 1 container for the database (PostgreSQL).

1. Clone the project and navigate to the root directory (`kl-interiors-be`).
2. Open the terminal and run the following command to build and start the application (in detached mode):
   ```bash
   docker-compose up -d --build
   ```
3. Once Docker is up and running, you can test it:
   - Health Check API: [http://localhost:8000/health/](http://localhost:8000/health/)
   - Interactive API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
   - Alternative API Documentation (ReDoc): [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Useful Commands

- **View web application logs**:
  ```bash
  docker-compose logs -f web
  ```
- **Stop the project (without deleting database data)**:
  ```bash
  docker-compose stop
  ```
- **Restart the application**:
  ```bash
  docker-compose restart
  ```
- **Stop and remove containers completely (keeps database volume intact)**:
  ```bash
  docker-compose down
  ```

_(Note: If you want to code on your local machine with IDE autocompletion support, it is recommended to create a venv and run `pip install -r requirements.txt` locally)._

---

## 🏗️ 2. Project Architecture (Bigger Applications)

This project is structured according to the "Bigger Applications" guidelines from FastAPI (suitable for medium to large-scale applications). It ensures business logic scope separation, prevents files from becoming too large, and improves maintainability.

Detailed structure of the `/app` directory:

```text
.
├── app/
│   ├── __init__.py           # Declares the app package
│   ├── main.py               # Main file to initialize FastAPI application and include routers
│   ├── dependencies.py       # Reusable dependencies across multiple routers (e.g., authentication)
│   ├── database.py           # Database connection setup (Engine, Session)
│   ├── routers/              # Contains API Endpoints split by modules
│   │   ├── __init__.py
│   │   ├── health.py         # Handles /health endpoint
│   │   └── users.py          # (Example) APIs related to users
│   └── internal/             # Contains internal logic (admin tasks, cron jobs, etc.) not exposed publicly
│       └── __init__.py
└── ...
```

### Guidelines for adding new features:

1. Each resource (e.g., `products`, `users`, `orders`) should have a **dedicated file** inside the `routers/` directory.
2. Initialize an `APIRouter` object in that specific file instead of using the main `app` object directly.
3. Bring the sub-router back and include it in `main.py` using `app.include_router(new_router)`.
4. Global logic like security protections (`header`, `token`, `session`) should be placed in `dependencies.py` and subsequently injected.

---

## 🌍 3. RESTful API Design Standards

API design principles in this project adhere to RESTful standards, ensuring system logical consistency and ease of understanding for clients.

### 3.1 Naming Conventions (Endpoint Naming)

- **Use Nouns, Not Verbs:**
  The endpoint should clearly describe the resource. Do not include actions in the URL.
  - ✅ Good: `GET /users`, `POST /orders`
  - ❌ Bad: `GET /get-users`, `POST /create-order`
- **Use Plural Nouns for Collections:**
  - ✅ Good: `GET /products`
  - ❌ Bad: `GET /product`
- **Represent Resource Hierarchy:** When you need "all comments of post 1"
  - ✅ Good: `GET /posts/1/comments`

### 3.2 Proper Use of HTTP Methods

Every operation (CRUD) must map to the corresponding HTTP Method:

| Method     | Description (Action)                                                                | Example Endpoint               | Expected Response                                                                |
| ---------- | ----------------------------------------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
| **GET**    | Retrieve information from a collection or single item (does not mutate DB).         | `GET /users` or `GET /users/5` | Returns a list or 1 object, status `200 OK`.                                     |
| **POST**   | Create a new resource. The client DOES NOT specify the ID.                          | `POST /users`                  | Server generates ID and returns `201 Created` with the created object or a link. |
| **PUT**    | Update the entire resource/override an existing entry. Must send full Body payload. | `PUT /users/5`                 | Returns modified object, status `200 OK`.                                        |
| **PATCH**  | Update particular properties of a resource (e.g., change password only).            | `PATCH /users/5`               | Returns updated record, status `200 OK`.                                         |
| **DELETE** | Remove a resource.                                                                  | `DELETE /users/5`              | Returns empty content with status `204 No Content`.                              |

### 3.3 HTTP Status Codes Standards

- `200 OK`: Request successful.
- `201 Created`: Resource successfully created.
- `204 No Content`: Successful processing but no data to return (used primarily for Delete).
- `400 Bad Request`: Syntax error or request data structure is invalid.
- `401 Unauthorized`: User is not logged in or invalid token.
- `403 Forbidden`: User logged in but lacks required business capabilities/permissions.
- `404 Not Found`: Demanded resource cannot be found.
- `500 Internal Server Error`: An unexpected backend error occurred.

---

## ⚡ 4. FastAPI & Python Best Practices

In addition to architecture and REST concepts, we adhere to the following community-driven best practices for FastAPI:

### 4.1. Async vs Sync Routes

- **I/O Bound tasks (DB calls, external API requests):** Use `async def` and non-blocking tools (like `httpx` or async database drivers like `asyncpg`).
- **CPU Bound tasks (Complex math, file processing):** Offload to separate workers (`Celery`, `multiprocessing`) to avoid blocking the single-threaded Event Loop.
- **Sync I/O tasks:** If you absolutely must use a synchronous library (like `requests` or `psycopg2`), use standard `def` routes so FastAPI can offload them to a separate threadpool, or use `run_in_threadpool`.

### 4.2. Pydantic Good Defaults

- Keep models decoupled. Having a giant `BaseSettings` file for the entire app is bad practice. Split settings (e.g., `AuthConfig`, `DatabaseConfig`) per module.
- Create a `CustomBaseModel` if you frequently need to override default Pydantic behaviors (like parsing datetime strings consistently to UTC).

### 4.3. Dependencies as Validators

- FastAPI `Depends()` is not just for dependency injection; it's extremely powerful for complex validations (e.g., checking if a user exists in the DB, verifying ownership of a resource).
- **Dependency Chaining:** Reuse dependencies inside other dependencies.
- **Caching:** FastAPI caches the result of a dependency per request. If 3 different functions inside a route rely on `get_db()`, the DB connection logic only fires once.
- Always prefer `async def` for dependencies unless they involve blocking code.

### 4.4. Database and ORM

- **SQL First:** CPython is slow at aggregating huge nested arrays. Let the database do the heavy lifting using `group_by`, joins, and JSON aggregations (like PostgreSQL's `json_build_object`) before returning data to Python.
- **Migration conventions:** When using Alembic, name files descriptively with slugs (e.g. `2024-02-23_added_users_table.py`). Migrations should be reversible and deterministic.

### 4.5. Hide Docs on Production

- Disable automatic documentation (`/docs`, `/redoc`) on Production environments by setting `openapi_url=None` based on environment variables to prevent exposing endpoints.

---

## 🐘 5. PostgreSQL Database Design Guidelines

Relational database design relies extensively on a table-based structure connected conceptually by relationships. According to industry-standard PostgreSQL guidelines, follow these core principles:

### 5.1. Normalization vs. Denormalization

- **Normalization (1NF, 2NF, 3NF):** Crucial for preventing data anomalies and duplication during data manipulation (insertions, updates, deletions). For instance, an `Items` column violating 1NF by containing multiple elements like `"Laptop, Mouse"` should be split into individual rows. Furthermore, avoid transitive dependencies to stay strictly compliant with 3NF.
- **Denormalization for Performance:** Sometimes data integrity trade-offs are justifiable if you require blistering read speeds, particularly on read-heavy or analytical endpoints. In these cases, combining tables reduces complex JOIN operations. Evaluate the trade-off logically.

### 5.2. Integrity through Constraints

- **Primary & Foreign Keys:** Ensure entity identity uniqueness using primary keys. Foreign keys mandate referential integrity (e.g., `client_id` inside a `contacts` table strictly matches an existing client). Take advantage of PostgreSQL's cascading options to propagate deletions seamlessly.

### 5.3. Effective Indexing Strategies

Understanding query patterns is necessary, as over-indexing impacts write/update speeds.

- **B-tree Indexes:** The default and most flexible tool for value retrieval and range queries.
- **Hash Indexes:** Ideal for simple equality comparisons where B-Tree processing is overkill.
- **GIN Indexes:** Perfect for multi-value types (e.g., arrays, `JSONB` columns frequently used in FastAPI).
- **BRIN Indexes:** Highly advantageous for enormous append-only data such as logs or time-series tracking.

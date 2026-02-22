import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Create an in-memory SQLite database for testing Fast execution
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

from app.models.user import User
from app.auth import get_password_hash

@pytest.fixture
def admin_token(client, db_session):
    user = User(
        username="adminuser",
        email="admin@test.com",
        password_hash=get_password_hash("password"),
        full_name="Admin User",
        role="ADMIN"
    )
    db_session.add(user)
    db_session.commit()
    
    res = client.post("/auth/login", data={"username": "adminuser", "password": "password"})
    return res.json()["access_token"]

@pytest.fixture
def customer_token(client, db_session):
    user = User(
        username="customeruser",
        email="customer@test.com",
        password_hash=get_password_hash("password"),
        full_name="Customer User",
        role="CUSTOMER"
    )
    db_session.add(user)
    db_session.commit()
    
    res = client.post("/auth/login", data={"username": "customeruser", "password": "password"})
    return res.json()["access_token"]

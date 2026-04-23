import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.core.db import get_db
from app.main import app
from app.models.parcel_type import ParcelType


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    session.add_all(
        [
            ParcelType(name="одежда"),
            ParcelType(name="электроника"),
            ParcelType(name="разное"),
        ]
    )
    session.commit()
    session.close()

    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    with TestClient(app) as test_client:
        yield test_client



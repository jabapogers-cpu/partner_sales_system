import os
import sys


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT_DIR, "app")

for path in (ROOT_DIR, APP_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

import pytest
from fastapi.testclient import TestClient

from database import Base, engine, SessionLocal, get_db
from main import app
import models


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    """
    Создаёт таблицы один раз перед всеми тестами и удаляет их после
    всего прогона.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """
    Создает новую сессию для тестов
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.query(models.Sale).delete()
        session.commit()
        session.close()


@pytest.fixture()
def client(db_session):
    """
    Меняем в исходном коде бд на тестовую
    """
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def make_sale(db_session):
    """
    Создает тестовую запись в бд
    """
    def _make_sale(**overrides):
        from datetime import date, timedelta

        defaults = dict(
            company_name="Фудзияма",
            sale_name="Сет за 1000р",
            date_of_add=str(date.today()),
            category="Еда",
            how_to_get="Продайте душу",
            sale_period=date.today() + timedelta(days=30),
            about_partner="Фудзияма суши",
            promo="UYUT15",
            address="ссылка типо",
        )
        defaults.update(overrides)
        sale = models.Sale(**defaults)
        db_session.add(sale)
        db_session.commit()
        db_session.refresh(sale)
        return sale

    return _make_sale
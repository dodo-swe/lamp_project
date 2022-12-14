import sys
from pathlib import Path
from typing import Any, Generator, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

sys.path.append(Path(".").parent.as_posix())
from api import router
from database import Base, User, get_db, Movie

_app = FastAPI()
_app.include_router(router)
engine = create_engine(url="sqlite://", connect_args={"check_same_thread": False})
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    with engine.connect() as connection:
        transaction = connection.begin()
        with sync_session(bind=connection) as session:
            yield session
        transaction.rollback()


@pytest.fixture(scope="module")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="module")
def test_users(app: FastAPI, db_session: Session) -> Generator[List[User], Any, None]:
    first_user = User(
        username="firstuser",
        firstname="firstname",
        lastname="lastname",
        password="pass",
    )
    second_user = User(
        username="seconduser",
        firstname="secondfirstname",
        lastname="secondlastname",
        password="pass",
    )
    db_session.add_all([first_user, second_user])
    db_session.commit()
    yield first_user, second_user


@pytest.fixture(scope="module")
def test_movie(app: FastAPI, db_session: Session) -> Generator[User, Any, None]:
    user = User(
        username="movieuser",
        firstname="firstname",
        lastname="lastname",
        password="pass",
        movies=[
            Movie(
                owner_id=3,
                title="somemovie",
                genre="somegenre",
                trailer="http://some.url",
            )
        ],
    )
    db_session.add(user)
    db_session.commit()
    yield user

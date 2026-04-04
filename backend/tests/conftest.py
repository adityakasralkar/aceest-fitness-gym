import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def auth_token(app):
    with app.app_context():
        token = create_access_token(identity="testuser", additional_claims={"role": "Admin"})
        return token


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        yield
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

import pytest
from base_sloi import HttpFacade
import uuid
import psycopg2
from basepage import LoginPage, CatalogPage, CartPage, OrderPage


@pytest.fixture(scope="session")
def api():
    return HttpFacade("http://localhost:8081")


@pytest.fixture
def unique_email():
    return f"user_{uuid.uuid4().hex[:8]}@example.com"

@pytest.fixture
def unique_password():
    return uuid.uuid4().hex[:8]

@pytest.fixture
def unique_name():
    return f"user_{uuid.uuid4().hex[:8]}"

def generate_unique_email():
    return f"user_{uuid.uuid4().hex[:8]}@example.com"

def generate_unique_password():
    return uuid.uuid4().hex[:8]

def generate_unique_name():
    return f"user_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def user(api):
    data = {
        "email": generate_unique_email(),
        "password": generate_unique_password(),
        "name": generate_unique_name()
    }
    response = api.users.register_user(data)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    resp_json = response.json()
    headers = {"Authorization": f"Bearer {resp_json['accessToken']}"}
    user_id = resp_json["user"]["id"]
    yield headers, user_id
    delete_resp = api.users.delete_user(user_id, headers=headers)
    assert delete_resp.status_code == 200

@pytest.fixture
def other_user(api):
    data = {
        "email": generate_unique_email(),
        "password": generate_unique_password(),
        "name": generate_unique_name()
    }
    response = api.users.register_user(data)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    resp_json = response.json()
    headers = {"Authorization": f"Bearer {resp_json['accessToken']}"}
    user_id = resp_json["user"]["id"]
    yield headers, user_id
    delete_resp = api.users.delete_user(user_id, headers=headers)
    assert delete_resp.status_code == 200


@pytest.fixture
def db_connect():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="store",
        user="store",
        password="store",
        sslmode="disable"
    )
    connection.autocommit = False
    yield connection
    connection.rollback()
    connection.close()

@pytest.fixture
def cursor(db_connect):
    cursor = db_connect.cursor()
    yield cursor
    cursor.close()

@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def catalog_page(page):
    return CatalogPage(page)

@pytest.fixture
def cart_page(page):
    return CartPage(page)

@pytest.fixture
def order_page(page):
    return OrderPage(page)
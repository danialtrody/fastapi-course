# ============================================================
#                           IMPORTS
# ============================================================
from fastapi import status

from .utils import *
from ..routers.users import get_current_user, get_db


# ============================================================
#                    DEPENDENCY OVERRIDES
# ============================================================
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# ============================================================
#                    TESTS – GET USER
# ============================================================
def test_return_user(test_user):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["username"] == "danialtest"
    assert data["email"] == "danialtest@gmail.com"
    assert data["first_name"] == "danialtest"
    assert data["last_name"] == "danialtest"
    assert data["role"] == "admin"
    assert data["phone_number"] == "0545361151"


# ============================================================
#                    TESTS – CHANGE PASSWORD
# ============================================================
def test_change_password_success(test_user):
    response = client.put(
        "/users/password",
        json={
            "password": "123",
            "new_password": "newpassqord",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/users/password",
        json={
            "password": "wrong",
            "new_password": "newpassqord",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


# ============================================================
#                    TESTS – CHANGE PHONE NUMBER
# ============================================================
def test_change_phone_number_success(test_user):
    response = client.put("/users/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT

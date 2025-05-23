from fastapi.testclient import TestClient
from test import session_fixture, client_fixture  # noqa: F401


def test_list_roles_success(client: TestClient):
    """
    Test retrieving all user roles successfully.
    """
    response = client.get("/roles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_users_success(client: TestClient):
    """
    Test retrieving all users successfully.
    """
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_retrieve_user_success(client: TestClient):
    """
    Test retrieving a user by ID successfully.
    """
    # First, create a user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "role_id": 1,
        "first_name": "New",
        "last_name": "User",
    }
    create_resp = client.post("/users", json=user_data)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["id"]

    # Now, retrieve the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_retrieve_user_not_found(client: TestClient):
    """
    Test retrieving a user by ID that does not exist.
    """
    response = client.get("/users/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_success(client: TestClient):
    """
    Test deleting a user by ID successfully.
    """
    # First, create a user
    user_data = {
        "username": "todelete",
        "email": "todelete@example.com",
        "role_id": 1,
        "first_name": "New",
        "last_name": "User",
    }
    create_resp = client.post("/users", json=user_data)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["id"]

    # Now, delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() is True


def test_delete_user_not_found(client: TestClient):
    """
    Test deleting a user by ID that does not exist.
    """
    response = client.delete("/users/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_add_user_success(client: TestClient):
    """
    Test creating a new user successfully.
    """
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "role_id": 1,
        "first_name": "New",
        "last_name": "User",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"


def test_add_user_missing_field(client: TestClient):
    """
    Test creating a new user with missing required fields.
    """
    user_data = {
        "username": "incompleteuser"
        # Missing email and role_id
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422  # Unprocessable Entity


def test_update_user_success(client: TestClient):
    """
    Test updating an existing user successfully.
    """
    # First, create a user
    user_data = {
        "username": "updateuser",
        "email": "updateuser@example.com",
        "role_id": 1,
        "first_name": "New",
        "last_name": "User",
    }
    create_resp = client.post("/users", json=user_data)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["id"]

    # Now, update the user
    update_data = {
        "username": "updateduser",
        "email": "updateduser@example.com",
        "role_id": 1,
    }
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


def test_update_user_not_found(client: TestClient):
    """
    Test updating a user that does not exist.
    """
    update_data = {
        "username": "ghost",
        "email": "ghost@example.com",
        "role_id": 1,
        "first_name": "New",
        "last_name": "User",
    }
    response = client.put("/users/999999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

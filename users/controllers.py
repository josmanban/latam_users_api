from fastapi import APIRouter, HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError
from pydantic import ValidationError
from base.db_connection import SessionDep
from users.models import User, UserList, UserRole
from users.repositories import UserRepository, UserRoleRepository

router = APIRouter()


@router.get("/roles", tags=["roles"], response_model=list[UserRole])
async def list_roles(session: SessionDep):
    """
    Retrieve all user roles.

    - **Description:** Returns a list of all available user roles.
    - **Response Example:**
        [
            {"id": 1, "name": "admin", "description": "Administrator"},
            {"id": 2, "name": "user", "description": "Regular user"},
            {"id": 3, "name": "guest", "description": "Guest user"}
        ]
    """
    repo = UserRoleRepository(session)
    return repo.get_all()


@router.get("/users", tags=["users"], response_model=list[UserList])
async def list_users(session: SessionDep):
    """
    Retrieve all users.

    - **Description:** Returns a list of all users with basic information.
    - **Response Example:**
        [
            {
                "id": 1,
                "username": "alice",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Smith",
                "active": true,
                "created_at": "2023-10-01T12:00:00",
                "updated_at": "2023-10-01T12:00:00"
            },
            {
                "id": 2,
                "username": "bob",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Johnson",
                "active": true,
                "created_at": "2023-10-01T12:00:00",
                "updated_at": "2023-10-01T12:00:00"
            }
        ]
    """
    repo = UserRepository(session)
    return repo.get_all()


@router.get("/users/{id}", tags=["users"], response_model=User)
async def retrieve_user(id: int, session: SessionDep):
    """
    Retrieve a user by ID.

    - **Description:** Returns detailed information about a specific user.
    - **Path Parameter:** `id` - The user's unique identifier.
    - **Response Example:**
        {
            "id": 1,
            "username": "alice",
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "active": true,
            "created_at": "2023-10-01T12:00:00",
            "updated_at": "2023-10-01T12:00:00",
            "role": {"id": 1, "name": "admin", "description": "Administrator"}
        }
    - **404:** User not found.
    """
    repo = UserRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="User not found")
    return instance


@router.delete("/users/{id}", tags=["users"])
async def delete_user(id: int, session: SessionDep):
    """
    Delete a user by ID.

    - **Description:** Removes a user from the system.
    - **Path Parameter:** `id` - The user's unique identifier.
    - **Response:** `true` if deleted.
    - **404:** User not found.
    """
    try:
        repo = UserRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/users", tags=["users"])
async def add_user(user: User, session: SessionDep):
    """
    Create a new user.

    - **Description:** Adds a new user to the system.
    - **Request Example:**
        {
            "username": "charlie",
            "email": "charlie@example.com",
            "first_name": "Charlie",
            "last_name": "Brown",
            "active": true,
            "created_at": "2023-10-01T12:00:00",
            "updated_at": "2023-10-01T12:00:00",
            "role_id": 2
        }
    - **Response:** The created user object.
    - **Response Example:**
        {
            "id": 3,
            "username": "charlie",
            "email": "charlie@example.com",
            "first_name": "Charlie",
            "last_name": "Brown",
            "active": true,
            "created_at": "2023-10-01T12:00:00",
            "updated_at": "2023-10-01T12:00:00",
            "role": {"id": 2, "name": "user", "description": "Regular user"}
        }
    """
    try:
        repo = UserRepository(session)
        return repo.add(user)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e.errors()))


@router.put("/users/{id}", tags=["users"])
async def update_user(id: int, user: User, session: SessionDep):
    """
    Update an existing user.

    - **Description:** Modifies user information.
    - **Path Parameter:** `id` - The user's unique identifier.
    - **Request Example:**
        {
            "username": "alice",
            "email": "alice@newdomain.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "active": true,
            "created_at": "2023-10-01T12:00:00",
            "updated_at": "2023-10-01T12:00:00",
            "role_id": 1
        }
    - **Response:** The updated user object.
    - **Response Example:**
        {
            "id": 1,
            "username": "alice",
            "email": "alice@newdomain.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "active": true,
            "created_at": "2023-10-01T12:00:00",
            "updated_at": "2023-10-01T12:00:00",
            "role": {"id": 1, "name": "admin", "description": "Administrator"}
        }
    - **404:** User not found.
    """
    try:
        repo = UserRepository(session)
        return repo.update(id, user)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="User not found")

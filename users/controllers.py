from fastapi import APIRouter, HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError

from base.db_connection import SessionDep
from users.models import User, UserList, UserRole
from users.repositories import UserRepository, UserRoleRepository

router = APIRouter()


@router.get("/roles", tags=["roles"], response_model=list[UserRole])
async def list_roles(session: SessionDep):
    repo = UserRoleRepository(session)
    return repo.get_all()


@router.get("/users", tags=["users"], response_model=list[UserList])
async def list_users(session: SessionDep):
    repo = UserRepository(session)
    return repo.get_all()


@router.get("/users/{id}", tags=["users"], response_model=User)
async def retrieve_user(id: int, session: SessionDep):
    repo = UserRepository(session)
    instance = repo.get(id)
    if not instance:
        raise HTTPException(status_code=404, detail="User not found")
    return instance


@router.delete("/users/{id}", tags=["users"])
async def delete_user(id: int, session: SessionDep):
    try:
        repo = UserRepository(session)
        return repo.delete(id)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/movie", tags=["users"])
async def add_user(user: User, session: SessionDep):
    repo = UserRepository(session)
    return repo.add(user)


@router.put("/users/{id}", tags=["users"])
async def update_user(id: int, user: User, session: SessionDep):
    try:
        repo = UserRepository(session)
        return repo.update(id, user)
    except UnmappedInstanceError:
        raise HTTPException(status_code=404, detail="User not found")

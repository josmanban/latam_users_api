from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class UserRoleBase(SQLModel):
    name: str
    description: str


class UserRole(UserRoleBase, table=True):
    id: int = Field(primary_key=True)
    users: list["User"] | None = Relationship(back_populates="role")


class UserBase(SQLModel):
    username: str
    email: str
    first_name: str
    last_name: str

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow, nullable=False)
    active: bool = Field(default=True)


class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    role_id: int | None = Field(default=None, foreign_key="userrole.id")
    role: UserRole | None = Relationship(back_populates="users")


class UserList(UserBase):
    pass

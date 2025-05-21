from base.repository import Repository

from users.models import User, UserRole


class UserRoleRepository(Repository[UserRole]):
    def __init__(self, session):
        super().__init__(UserRole, session)


class UserRepository(Repository[User]):
    def __init__(self, session):
        super().__init__(User, session)

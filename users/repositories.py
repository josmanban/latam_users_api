from datetime import datetime
from base.repository import Repository
from users.models import User, UserRole


class UserRoleRepository(Repository[UserRole]):
    def __init__(self, session):
        super().__init__(UserRole, session)


class UserRepository(Repository[User]):
    def __init__(self, session):
        super().__init__(User, session)

    def update(self, id, instance):
        updated_instance = super().update(id, instance)
        # set the updated_at field to the current datetime
        updated_instance.updated_at = datetime.now()
        self.session.commit()
        self.session.refresh(updated_instance)
        return updated_instance

from typing import TypeVar, Generic, Type, Sequence
from sqlmodel import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from base.db_connection import SessionDep

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, model_class: Type[T], session: SessionDep):
        """
        Initialize the repository.

        Args:
            model_class (Type[T]): The SQLModel class this repository manages.
            session (SessionDep): The database session to use for operations.
        """
        self.session = session
        self.model_class = model_class
        super().__init__()

    def get(self, id: int) -> T | None:
        """
        Retrieve a single record by its primary key.

        Args:
            id (int): The primary key of the record.

        Returns:
            Optional[T]: The record if found, otherwise None.

        Example:
            user = user_repository.get(1)
        """
        return self.session.get(self.model_class, id)

    def get_all(self) -> Sequence[T]:
        """
        Retrieve all records of the model.

        Returns:
            Sequence[T]: A sequence of all records.

        Example:
            users = user_repository.get_all()
        """
        statement = select(self.model_class)
        results = self.session.exec(statement).all()
        return results

    def add(self, new_instance: T) -> T:
        """
        Add a new record to the database.

        Args:
            new_instance (T): The instance to add.

        Returns:
            T: The newly added and refreshed instance.

        Example:
            new_user = user_repository.add(User(...))
        """
        self.session.add(new_instance)
        self.session.commit()
        self.session.refresh(new_instance)
        return new_instance

    def update(self, id: int, instance: T) -> T:
        """
        Update an existing record by its primary key.

        Args:
            id (int): The primary key of the record to update.
            instance (T): The instance containing updated data.

        Returns:
            T: The updated and refreshed instance.

        Raises:
            UnmappedInstanceError: If the record does not exist.

        Example:
            updated_user = user_repository.update(1, user_update)
        """
        db_instance = self.session.get(self.model_class, id)
        if not db_instance:
            raise UnmappedInstanceError(db_instance)
        instance_data = instance.model_dump(exclude_unset=True)  # type: ignore[attr-defined]
        db_instance.sqlmodel_update(instance_data)  # type: ignore[attr-defined]
        self.session.add(db_instance)
        self.session.commit()
        self.session.refresh(db_instance)
        return db_instance

    def delete(self, id: int) -> bool:
        """
        Delete a record by its primary key.

        Args:
            id (int): The primary key of the record to delete.

        Returns:
            bool: True if the record was deleted.

        Example:
            user_repository.delete(1)
        """
        instance = self.session.get(self.model_class, id)
        self.session.delete(instance)
        self.session.commit()
        return True

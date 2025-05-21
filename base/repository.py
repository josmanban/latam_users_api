from typing import TypeVar, Generic, Type, Sequence
from sqlmodel import select
from sqlalchemy.orm.exc import UnmappedInstanceError

from base.db_connection import SessionDep

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, model_class: Type[T], session: SessionDep):
        self.session = session
        self.model_class = model_class
        super().__init__()

    def get(self, id: int) -> T | None:
        return self.session.get(self.model_class, id)

    def get_all(self) -> Sequence[T]:
        statement = select(self.model_class)
        results = self.session.exec(statement).all()
        return results

    def add(self, new_instance: T) -> T:
        self.session.add(new_instance)
        self.session.commit()
        self.session.refresh(new_instance)
        return new_instance

    def update(self, id: int, instance: T) -> T:
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
        instance = self.session.get(self.model_class, id)
        self.session.delete(instance)
        self.session.commit()
        return True

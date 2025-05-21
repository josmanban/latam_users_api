import json
from users.models import UserRole
from sqlmodel import Session

from base.db_connection import engine


def load_user_roles(engine):
    with Session(engine) as session:
        with open("./datasets/userrole.json") as f:
            output_data = json.load(f)
            for genre_data in output_data:
                genre = UserRole(**genre_data)
                session.add(genre)
            session.commit()


def load_initial_data(engine):
    load_user_roles(engine)


def main():
    load_initial_data(engine)


if __name__ == "__main__":
    main()

from bot.Utils.PostDatabase.models import Gift
from bot.Utils.PostDatabase.db import gifts

from sqlalchemy.orm import Session
from sqlalchemy import select


class Database:
    def __init__(self, session: Session) -> None:
        self.session = session

    # пример запроса на добавление юзера
    async def add_user(self, user_id: str, username: str, name: str) -> None:
        with self.session as session:
            query = select(users).filter_by(user_id=user_id)
            user = session.execute(query).all()

            print(user)
            if not user:
                print("not user")
                user = User(
                    user_id=user_id,
                    username=username,
                    name=name
                )
                session.add(user)
                session.commit()

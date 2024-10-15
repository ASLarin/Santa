from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
from bot.config import config
import logging

logger = logging.getLogger("bot.bd")
logger.setLevel(logging.INFO)

DATABASE_URL = config.DATABASE_URL
# Создание движка подключения
engine = create_engine(DATABASE_URL)
# Базовый класс для декларативных моделей
Base = declarative_base()
# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False)
    telegram_id = Column(BigInteger, nullable=False, unique=True)

    def __repr__(self):
        return (f'<User(id={self.id}, nickname={self.nickname}, telegram_id={self.telegram_id}')

Base.metadata.create_all(engine)

def user_exists(telegram_id: int) -> bool:
    return session.query(Users).filter(Users.telegram_id == telegram_id).first() is not None

def new_user(nickname: str, telegram_id: int, caretaker_id: int = None):
    if user_exists(telegram_id):
        logger.info(f"Пользователь с telegram_id={telegram_id} уже существует.")
        return

    new_user = Users(nickname=nickname, telegram_id=telegram_id)
    session.add(new_user)
    session.commit()
    logger.info(f"Добавлен новый пользователь: {new_user}")

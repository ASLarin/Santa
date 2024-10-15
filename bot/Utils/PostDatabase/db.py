# Подключение к базе данных PostgreSQL
from sqlalchemy import create_engine, MetaData, Table, Column, Text, Integer, BLOB, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

from bot.config import config

host=config.POST_DB_HOST
user=config.POST_DB_USER
password=config.POST_DB_PASS
database=config.POST_DB_NAME
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}"

# Создание движка подключения
engine = create_engine(DATABASE_URL)


metadata = MetaData()

# Объявляем таблицы

# users = Table(
#     "users", metadata,
#     Column("user_id", Text(), primary_key=True),
#     Column("username", Text()),
#     Column("name", Text()),
#     Column("bought", Text()),
#     Column("genres", Text()),
# )

gifts = Table(
    "gifts", metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("image", Text()),
    Column("name", Text()),
    Column("price", Text()),
    Column("description", Text()),
    Column("store", Text()),
    Column("thematic", Text()),
    Column("form_factor", Text()),
    Column("reviews", Text()),
    Column("url", Text()),
)

# Создаём таблицы, если их нет
metadata.create_all(engine)


# Базовый класс для декларативных моделей
Base = declarative_base()

session = sessionmaker(bind=engine)

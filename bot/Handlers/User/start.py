from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os



class UserRegistration:

    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я бот. Пожалуйста, зарегистрируйтесь.")


    async def start_registration(message: types.Message, state: FSMContext, role: str):
        user_id = message.from_user.id
        username = message.from_user.username

        # Подключаемся к базе данных
        session = SessionLocal()

        try:
            # Проверяем, существует ли пользователь уже
            user = session.query(User).filter(User.telegram_id == user_id).first()
            if user:
                await message.reply("Вы уже зарегистрированы!")
            else:
                # Создаем нового пользователя и сохраняем в базе данных
                new_user = User(telegram_id=user_id, username=username, role=role)
                session.add(new_user)
                session.commit()
                await message.reply(f"Регистрация завершена! Роль {role} сохранена для пользователя {username}.")
        except Exception as e:
            await message.reply(f"Ошибка при регистрации: {e}")
            session.rollback()  # Откат транзакции в случае ошибки
        finally:
            session.close()  # Закрываем сессию

        # Обновляем состояние FSM
        await state.update_data(role=role)

# Функция для регистрации хэндлеров
def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(UserRegistration.send_welcome, commands=["start"])

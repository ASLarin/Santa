import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from bot.bot import dp
from pymorphy3 import MorphAnalyzer
from bot.Middleware import rate_limit
from bot.Utils.bd import new_user, user_exists
logger = logging.getLogger("bot.handler")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

class UserRegister(StatesGroup):
    waiting_for_name = State()
    waiting_for_group = State()

morph = MorphAnalyzer()
class UserRegistration:
    @rate_limit(3, 'start')
    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message, state: FSMContext, role: str):
        user_id = message.from_user.id
        await state.update_data(role=role)
        await message.reply("Давай познакомимся!\nНапиши ФИО:")
        await UserRegister.waiting_for_name.set()

    @dp.message_handler(state=UserRegister.waiting_for_name, content_types=types.ContentTypes.TEXT)
    async def process_full_name(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        full_name = message.text.strip()
        parts = full_name.split()
        if len(parts) != 3:
            await message.reply("Пожалуйста, введите ФИО в формате: Фамилия Имя Отчество")
            logger.warning(f"Пользователь {user_id} ввел некорректный формат ФИО: '{full_name}'.")
            return
        surname, name, patronymic = parts
        parsed_surname = morph.parse(surname)
        is_surname = any('Surn' in p.tag for p in parsed_surname)
        if not is_surname:
            await message.reply("Пожалуйста, введите корректную фамилию:")
            logger.warning(f"Пользователь {user_id} отправил некорректную фамилию: '{surname}'.")
            return
        parsed_name = morph.parse(name)
        is_name = any('Name' in p.tag for p in parsed_name)
        if not is_name:
            await message.reply("Пожалуйста, введите корректное имя:")
            logger.warning(f"Пользователь {user_id} отправил некорректное имя: '{name}'.")
            return
        parsed_patronymic = morph.parse(patronymic)
        is_patronymic = any('Patr' in p.tag for p in parsed_patronymic)
        if not is_patronymic:
            await message.reply("Пожалуйста, введите корректное отчество:")
            logger.warning(f"Пользователь {user_id} отправил некорректное отчество: '{patronymic}'.")
            return

        full_name = f"{surname} {name} {patronymic}"
        await state.update_data(full_name=full_name)
        await message.reply(f"Приятно познакомиться, {full_name}!")
        logger.info(f"Пользователь {user_id} ввел ФИО: {full_name}")
        await message.reply("Отлично!\nТеперь введи свою учебную группу\nПример: ИУ10-72")
        await UserRegister.waiting_for_group.set()
    @dp.message_handler(state=UserRegister.waiting_for_birthday, content_types=types.ContentTypes.TEXT)
    @staticmethod
    async def process_birthday(message: types.Message, state: FSMContext, role:str ):
        telegram_id  = message.from_user.id
        user_group = await state.get_data()
        name = user_group.get("name")
        nickname  = message.from_user.username or "unknown"
        if user_exists(telegram_id):
            await message.reply("Вы уже зарегистрированы.")
            logger.info(f"Пользователь {telegram_id } попытался зарегистрироваться повторно.")
        else:
            new_user(
                name = name,
                user_id=telegram_id ,
                #user_group = user_group,
                nickname = nickname
                )
            await message.reply(f"Отлично!\nТеперь осталось только подождать начала")
            logger.info(f"Пользователь {telegram_id } из группы {user_group} успешно зарегистрирован с именем '{name}'.")
            await state.finish()
            #Добавить маску.


import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.utils.exceptions import Throttled

def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=5, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}_{message.from_user.id}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message_{message.from_user.id}"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()
    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}_{message.from_user.id}")
        else:
            key = f"{self.prefix}_message_{message.from_user.id}"
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await message.reply('Слишком много запросов!')
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Блокировка снята.')

# Использование антифлуда с помощью @rate_limit(5, 'text'), где "5" - количество запросов, "text" - техническое обозначение.
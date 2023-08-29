from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from bot import dp
from sqliteFuncs.sql_setup import sqlDatabase, User


class States(StatesGroup):
    start = State()


@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    
    sql = sqlDatabase()
    id = int(sql.get_all_users_ids()[-1]) + 1
    telegram_id = message.from_user.id
    username = message.from_user.username

    user = User(id,telegram_id,username)
    sql.add_user(user)

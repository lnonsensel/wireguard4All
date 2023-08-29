from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from bot import dp, bot
from sqliteFuncs.sql_setup import sqlDatabase, User
from keyboards.keyboards import *
from keyboards.russian import start_text
from wireguardLib.createUserConfig import userConfigCreator, userConfigManipulator


class States(StatesGroup):
    start = State()
    menu = State()

    howItWork = State()
    startTestPeriod = State()
    buySubscription = State()


def isequal(a, b) -> bool:
    return a == b

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    
    await message.answer(start_text, reply_markup=kb_menu)

    sql = sqlDatabase()

    id = int(sql.get_all_users_ids()[-1]) + 1
    telegram_id = message.from_user.id
    username = message.from_user.username

    if sql.user_exists(telegram_id):
        user = User(id,telegram_id,username)
        sql.add_user(user)
    else:
        await States.menu.set()


@dp.message_handler(lambda message: message.text == menu_b1_text, state = States.menu)
async def menu_1(message: types.Message):
    await message.answer(how_it_works_text, reply_markup=kb_menu)

@dp.message_handler(lambda message: message.text == menu_b2_text, state = States.menu)
async def menu_2(message: types.Message, state: FSMContext):
    
    configCreator = userConfigCreator()
    configCreator.createKeys()
    configCreator.createConfig()
    configCreator.saveAllUserConfiguration()
    configPath = configCreator.userConfigFilePath
    chat_id = message.from_user.id
    with open(configPath, 'rb') as config:
        userConfig = await bot.send_document(chat_id=chat_id, document=config)
    
    await state.update_data(configFileId = userConfig.document.file_id)
    print(userConfig.document.file_id)

@dp.message_handler(lambda message: message.text == menu_b3_text, state = States.menu)
async def menu_3(message: types.Message):
    await message.answer()

@dp.message_handler(state=States.menu)
async def menu_wrong(message: types.Message):
    await message.answer(wrong_menu_text)
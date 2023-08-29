from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from bot import dp, bot
from sqliteFuncs.sql_setup import sqlDatabase, User
from keyboards.keyboards import *
from keyboards.russian import start_text
from wireguardLib.createUserConfig import userConfigCreator, userConfigManipulator
import time
from utils.generateNewTimestamp import generateNewTimeStamp

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

    id = len(sql.get_all_users_ids())
    telegram_id = message.from_user.id
    username = message.from_user.username

    if not sql.user_exists(telegram_id):
        user = User(id=id,
                    telegram_id=telegram_id,
                    username=username,
                    active=True,
                    config_id=-1,
                    config_file_id=-1,
                    on_trial=False,
                    trial_used=False,
                    on_subscription=False,
                    subscription_ending_timestamp=0)
        
        sql.add_user(user)
    else:
        await States.menu.set()


@dp.message_handler(lambda message: message.text == menu_b1_text, state = States.menu)
async def menu_how_it_works(message: types.Message):
    await message.answer(how_it_works_text, reply_markup=kb_menu)

@dp.message_handler(lambda message: message.text == menu_b2_text, state = States.menu)
async def menu_start_test_period(message: types.Message, state: FSMContext):

    await message.answer(confirm_start_trial_text, reply_markup=kb_start_trial)
    await States.startTestPeriod.set()

@dp.message_handler(lambda message: message.text == menu_b3_text, state = States.menu)
async def menu_start_subscription(message: types.Message):
    await message.answer()

@dp.message_handler(state=States.menu)
async def menu_wrong(message: types.Message):
    await message.answer(wrong_menu_text)


@dp.message_handler(lambda message: message.text == start_trial_b1_text,state = States.startTestPeriod)
async def startTestPeriod(message: types.Message, state: FSMContext):

    sql = sqlDatabase()
    chat_id = message.from_user.id

    if sql.user_on_trial(chat_id):
        await message.answer(subscription_already_activated, reply_markup=kb_menu)
        await States.menu.set()
        return None

    if sql.user_trial_used(chat_id):
        await message.answer(trial_already_used, reply_markup=kb_menu)
        await States.menu.set()
        return None

    configCreator = userConfigCreator()
    configCreator.createKeys()
    configCreator.createConfig()
    configCreator.saveAllUserConfiguration()
    configPath = configCreator.userConfigFilePath

    with open(configPath, 'rb') as config:
        userConfig = await bot.send_document(chat_id=chat_id, document=config)
    
    sql.change_user_config_id(configCreator.userId, chat_id)
    sql.change_user_config_file_id(userConfig.document.file_id, chat_id)

    configAdmin = userConfigManipulator(configCreator.userId)
    configAdmin.addUserToServerConfig()
    
    sql.change_user_on_trial(True, chat_id)
    sql.change_user_subsription_ending_timestamp(generateNewTimeStamp(7), chat_id)


@dp.message_handler(lambda message: message.text == start_trial_b2_text, state = States.startTestPeriod)
async def decline_startTestPeriod(message: types.Message, state: FSMContext):
    
    await message.answer(back_to_menu_text, reply_markup=kb_menu)


@dp.message_handler(state = States.startTestPeriod)
async def wrong_startTestPeriod(message: types.Message):
    await message.answer(wrong_menu_text, reply_markup=kb_start_trial)

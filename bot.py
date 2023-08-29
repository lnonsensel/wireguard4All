from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_config import *

bot = Bot(BOT_API_MAIN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage = storage)
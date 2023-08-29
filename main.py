from aiogram import executor
from bot import dp
from states.States import *


executor.start_polling(dp, skip_updates=True)
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.russian import *

menu_all = [menu_b1_text, menu_b2_text, menu_b3_text]
menu_b1 = KeyboardButton(menu_b1_text)
menu_b2 = KeyboardButton(menu_b2_text)
menu_b3 = KeyboardButton(menu_b3_text)
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_menu.add(menu_b1, menu_b2, menu_b3)

start_trial_all = [start_trial_b1_text, start_trial_b2_text]
start_trial_b1 = KeyboardButton(start_trial_b1_text)
start_trial_b2 = KeyboardButton(start_trial_b2_text)
kb_start_trial = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start_trial.add(start_trial_b1, start_trial_b2)
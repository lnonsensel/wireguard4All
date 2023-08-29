from dotenv import dotenv_values

dotenvValues = dotenv_values('.env')
BOT_API_MAIN = dotenvValues['BOT_API_MAIN']

DATABASE_PATH = './databases'
from dotenv import dotenv_values

dotenvValues = dotenv_values('.env')
SERVER_PRIVATE_KEY = dotenvValues['SERVER_PRIVATE_KEY']
SERVER_PUBLIC_KEY = dotenvValues['SERVER_PUBLIC_KEY']

SERVER_IP = dotenvValues['SERVER_IP']

CFG_PATH = './config'
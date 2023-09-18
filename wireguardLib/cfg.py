from dotenv import dotenv_values

#define path to .env
dotenvValues = dotenv_values("")

SERVER_PRIVATE_KEY = dotenvValues['SERVER_PRIVATE_KEY']
SERVER_PUBLIC_KEY = dotenvValues['SERVER_PUBLIC_KEY']

SERVER_IP = dotenvValues['SERVER_IP']

#define path to cfg
CFG_PATH = ""

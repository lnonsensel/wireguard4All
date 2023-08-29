from dotenv import dotenv_values

dotenvValues = dotenv_values("/mnt/c/Users/LTT's PC/Desktop/python/wireGuard4All/wireguardLib/.env")
SERVER_PRIVATE_KEY = dotenvValues['SERVER_PRIVATE_KEY']
SERVER_PUBLIC_KEY = dotenvValues['SERVER_PUBLIC_KEY']

SERVER_IP = dotenvValues['SERVER_IP']

CFG_PATH = "/mnt/c/Users/LTT's PC/Desktop/python/wireGuard4All/wireguardLib/config"
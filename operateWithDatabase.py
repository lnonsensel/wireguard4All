from sqliteFuncs.sql_setup import sqlDatabase, User
from random import randint, shuffle
from string import ascii_lowercase, ascii_uppercase


def fulfillDatabase():
    database = sqlDatabase()
    allLetters = ascii_uppercase + ascii_lowercase
    for i in range(0,100):
        allLetters = list(allLetters)
        shuffle(allLetters)
        allLetters = ''.join(allLetters)
        id = database.get_users_quantity()
        user = User(str(id), str(randint(111111111,999999999)), allLetters[:randint(5,10)])
        database.add_user(user)


def clearDatabase():
    database = sqlDatabase()
    database.clear_database()

def checkIfUserExists(telegram_id):
    database = sqlDatabase()
    return database.user_exists(telegram_id)

def getUsersQuantity():
    database = sqlDatabase()
    return database.get_users_quantity()

def getAllUsersIds():
    database = sqlDatabase()
    return database.get_all_users_ids()

def checkIfUserOnTrial(telegram_id):
    database = sqlDatabase()
    return database.user_on_trial(telegram_id=telegram_id)


if __name__ == '__main__':
    clearDatabase()
    
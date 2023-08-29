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
        user = User(str(i), str(randint(1111111,9999999)), allLetters[:randint(5,10)])
        database.add_user(user)


def clearDatabase():
    database = sqlDatabase()
    database.clear_database()

if __name__ == '__main__':
    fulfillDatabase()
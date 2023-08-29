import sqlite3 as sq
from sqliteFuncs.database_config import DATABASE_PATH
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class User:

    id: str
    telegram_id: str
    username: str

    def unpack(self) -> list[str]:
        data = self.__dict__.values()
        return [str(i) for i in data]


class sqlDatabase():

    def __init__(self, database_name = 'database.db'):

        base = sq.connect(f'{DATABASE_PATH}/{database_name}')
        cursor = base.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (id TEXT,
                telegram_id TEXT,
                username TEXT
                )"""
                )

        base.commit()

        self.cursor = cursor
        self.base = base

    def add_user(self, user: User) -> None:

        cursor = self.cursor
        base = self.base

        request = 'INSERT INTO users VALUES (?, ?, ?)'

        userData = user.unpack()
        cursor.execute(request, userData)
        base.commit()
    

    def delete_user(self, user_id) -> None:

        cursor = self.cursor
        base = self.base

        request = 'DELETE FROM users WHERE id = (?)'

        cursor.execute(request, user_id)
        base.commit()


    def get_user_data(self, user_id) -> None:

        base = self.base

        request = f'SELECT * FROM users WHERE id = {user_id}'
        df = pd.read_sql(request, base)

        if df.empty:
            return False
        
        df = df.to_dict('records')[0]
        df = [i for i in df.values()]
        user = User(*df)
        return user
    

    def get_all_users_ids(self):
        
        cursor = self.cursor
        base = self.base

        request = 'SELECT id FROM users'
        ids = cursor.execute(request).fetchall()

        ids = [i[0] for i in ids]

        if ids == []: 
            return [-1]
        
        return ids


    def get_users_quantity(self):
        
        return len(self.get_all_users_ids())



if __name__ == '__main__':
    database = sqlDatabase()

    user = User('0','qweqwe','qweqweqwe')

    # database.add_user(user)

    # database.delete_user('0')

    # print(database.get_user_data('0'))

    print(database.get_all_users_ids())
import sqlite3 as sq
from sqliteFuncs.database_config import DATABASE_PATH
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class User:

    id: int
    telegram_id: int
    username: str
    active: bool
    config_id: int
    config_file_id: str
    on_trial: bool
    trial_used: bool
    on_subscription: bool
    subscription_ending_timestamp: float

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
                username TEXT,
                active BOOL,
                config_id INTEGER,
                config_file_id TEXT,
                on_trial BOOL,
                trial_used BOOL,
                on_subscription BOOL,
                subscription_ending_timestamp TEXT
                )"""
                )

        base.commit()

        self.cursor = cursor
        self.base = base


    def add_user(self, user: User) -> None:

        cursor = self.cursor
        base = self.base
        
        request = 'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        userData = user.unpack()
        cursor.execute(request, userData)
        base.commit()
    

    def delete_user_by_id(self, user_id) -> None:

        cursor = self.cursor
        base = self.base

        request = 'DELETE FROM users WHERE id = (?)'

        cursor.execute(request, user_id)
        base.commit()

    def delete_user_by_telegram_id(self, telegram_id) -> None:

        cursor = self.cursor
        base = self.base

        request = 'DELETE FROM users WHERE telegram_id = (?)'

        cursor.execute(request, telegram_id)
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
    

    def get_all_users_ids(self) -> list:
        
        cursor = self.cursor
        base = self.base

        request = 'SELECT id FROM users'
        ids = cursor.execute(request).fetchall()

        ids = [i[0] for i in ids]
        
        return ids


    def get_users_quantity(self) -> int:
        
        return len(self.get_all_users_ids())


    def user_exists(self, telegram_id) -> bool:

        cursor = self.cursor
        request = f"SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}"
        telegram_ids = cursor.execute(request)
        telegram_ids = telegram_ids.fetchall()
        telegram_ids = [i[0] for i in telegram_ids]

        if telegram_ids == []:
            return False
        else:
            return True


    def user_on_trial(self, telegram_id) -> None:

        cursor = self.cursor

        request = f'SELECT on_trial FROM users WHERE telegram_id = {telegram_id}'

        on_trial = cursor.execute(request).fetchone()[0]

        if on_trial == 'False':
            return False
        return True    

    def user_trial_used(self, telegram_id) -> None:

        cursor = self.cursor

        request = f'SELECT trial_used FROM users WHERE telegram_id = {telegram_id}'

        on_trial = cursor.execute(request).fetchone()[0]

        if on_trial == 'False':
            return False
        return True  

    def user_on_subscription(self, telegram_id) -> None:

        cursor = self.cursor

        request = f'SELECT on_subscription FROM users WHERE telegram_id = {telegram_id}'

        on_trial = cursor.execute(request).fetchone()[0]

        if on_trial == 'False':
            return False
        return True    


    def get_user_config_file_id(self, telegram_id):

        cursor = self.cursor

        request = f'SELECT config_file_id FROM users WHERE telegram_id = {telegram_id}'

        config_file_id = cursor.execute(request).fetchone()[0]

        return config_file_id   


    def clear_database(self) -> None:

        cursor = self.cursor
        base = self.base

        request = "DELETE FROM users"

        cursor.execute(request)
        base.commit()


    def change_user_config_id(self, new_id, telegram_id) -> None:

        cursor = self.cursor
        base = self.base

        request = f"UPDATE users SET config_id = {new_id} WHERE telegram_id = {telegram_id}"
        cursor.execute(request)
        base.commit()


    def change_user_config_file_id(self, new_file_id, telegram_id) -> None:

        cursor = self.cursor
        base = self.base

        request = f'UPDATE users SET config_file_id = "{new_file_id}" WHERE telegram_id = {telegram_id}'
        cursor.execute(request)
        base.commit()


    def change_user_subsription_ending_timestamp(self, new_timestamp, telegram_id) -> None:

        cursor = self.cursor
        base = self.base

        request = f"UPDATE users SET subscription_ending_timestamp = {new_timestamp} WHERE telegram_id = {telegram_id}"
        cursor.execute(request)
        base.commit()


    def change_user_on_trial(self, new_value, telegram_id) -> None:

        cursor = self.cursor
        base = self.base

        request = f'UPDATE users SET on_trial = {new_value} WHERE telegram_id = {telegram_id}'

        cursor.execute(request)
        base.commit()


    def change_user_on_subscription(self, new_value, telegram_id) -> None:

        cursor = self.cursor
        base = self.base

        request = f'UPDATE users SET on_subscription = {new_value} WHERE telegram_id = {telegram_id}'

        cursor.execute(request)
        base.commit()

if __name__ == '__main__':
    database = sqlDatabase()
    print(database.user_exists(7081171))
    database.delete_user_by_id(0)
    database.delete_user_by_id(1)
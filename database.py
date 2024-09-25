import sqlite3
import datetime as dt
import yadisk
import os

yadisk_token = 'y0_AgAAAAAz3q8eAAr2mwAAAAD0Rs3otjfzkvntRf6Rsx5SlBJWe4N8880'


class DatabaseCloud:

    def __init__(self, token):
        self.disk = yadisk.YaDisk(token=token)

    def upload(self, user_file, disk_file, remove=True):
        if disk_file in self.listdir() and remove:
            self.remove(disk_file)
        self.disk.upload(user_file, f'database/{disk_file}')

    def download(self, user_file, disk_file):
        os.remove(user_file)
        self.disk.download(f'database/{disk_file}', user_file)

    def listdir(self):
        return [i.name for i in list(self.disk.listdir("/database"))]

    def remove(self, disk_file):
        self.disk.remove(f'database/{disk_file}')


cloud = DatabaseCloud(yadisk_token)

cloud.download('reportbot.db', 'reportbot.db')
print('База данных установлена.')


class Create:

    @staticmethod
    def search_table():
        # Проверяем наличие таблицы
        connect = sqlite3.connect('reportbot.db')
        cursor = connect.cursor()

        check = cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' and name='main'"
        )

        # Если таблицы не существует - создаем её
        if check.fetchone() is None:
            cursor.execute("CREATE TABLE main ("
                           "n STRING PRIMARY KEY,"
                           "iron,"
                           "accessories,"
                           "additionally)"
                           )


class Database:
    def __init__(self):
        connect = sqlite3.connect('reportbot.db')
        cursor = connect.cursor()

        self.iron = cursor.execute('SELECT iron FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.accessories = cursor.execute('SELECT accessories FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.additionally = cursor.execute('SELECT additionally FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.iron_day = cursor.execute('SELECT iron_day FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.accessories_day = cursor.execute('SELECT accessories_day FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.additionally_day = cursor.execute('SELECT additionally_day FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.additionally_day_plan = cursor.execute('SELECT additionally_day_plan FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.oss = cursor.execute('SELECT oss FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.iron_quantity = cursor.execute('SELECT iron_quantity FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.accessories_quantity = cursor.execute('SELECT accessories_quantity FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.rso = cursor.execute('SELECT rso FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.chist = cursor.execute('SELECT chist FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.acme = cursor.execute('SELECT acme FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.rso_q = cursor.execute('SELECT rso_q FROM main WHERE n = ?', (1,)).fetchone()[0]
        self.chist_q = cursor.execute('SELECT chist_q FROM main WHERE n = ?', (1,)).fetchone()[0]

    def save(self, **kwargs):
        connect = sqlite3.connect('reportbot.db')
        cursor = connect.cursor()

        for key, value in kwargs.items():
            cursor.execute(f"UPDATE main SET {key} = ? WHERE n = ?", (value, 1))

        cloud.upload('reportbot.db', 'reportbot.db')
        connect.commit()
        connect.close()


Create().search_table()


import telebot
from telebot import types
import datetime as dt

from config import *
from database import Database

print("Active")
bot = telebot.TeleBot(token)

month = {1: 31,
         2: 28,
         3: 31,
         4: 30,
         5: 31,
         6: 30,
         7: 31,
         8: 31,
         9: 30,
         10: 31,
         11: 30,
         12: 31}


class Data:
    def __init__(self):
        self.end_day = month[dt.date.today().month]
        self.day = dt.date.today().day
        self.iron_plan = 540000
        self.accessories_plan = 105000
        self.additionally_plan = 126719
        # Илья Трухин, Нерсисян Денис, Афонин Иван
        self.users_id = [1820487086, 1750882022, 5689147524]

        self.process = 0
        # 1 - Iron
        # 2 - Accessories
        # 3 - Additionally


data = Data()


@bot.message_handler(commands=["start"])
def start(message):
    database = Database()
    iron_plan_day = int((data.iron_plan - database.iron) / (data.end_day - data.day))
    accessories_plan_day = int((data.accessories_plan - database.accessories) / (data.end_day - data.day))
    additionally_plan_day = int((int(data.additionally_plan) - int(database.additionally)) / (data.end_day - data.day))

    iron_plan_day = 0 if iron_plan_day < 0 else iron_plan_day
    accessories_plan_day = 0 if accessories_plan_day < 0 else accessories_plan_day
    additionally_plan_day = 0 if additionally_plan_day < 0 else additionally_plan_day

    general_plan_day = iron_plan_day + accessories_plan_day + additionally_plan_day
    general_day = database.iron_day + database.accessories_day + database.additionally_day

    dol_a = int((database.accessories_day / general_day) * 100) if general_day > 0 else 0
    dol_d = int((database.additionally_day / general_day) * 100) if general_day > 0 else 0

    bot.send_message(message.chat.id, 'Алексин 1\n\n'
                                      f'Общее ТО (план/факт) - {general_plan_day}/{general_day}\n'
                                      'Кредит - 0\n'
                                      'Фз (шт/факт) - 0\n'
                                      f'Железо (план/факт) - {iron_plan_day}/{database.iron_day}\n'
                                      f'Железо (шт) - {database.iron_quantity}\n'
                                      f'Аксы (план/факт) - {accessories_plan_day}/{database.accessories_day}\n'
                                      f'Аксы (шт) - {database.accessories_quantity}\n'
                                      f'Акми (шт) - {database.acme}\n'
                                      f'РСО2 (сумма/шт) - {database.rso}/{database.rso_q}\n'
                                      f'Чистка (сумма/шт) - {database.chist}/{database.chist_q}\n'
                                      f'ДОП (план/факт) - {additionally_plan_day}/{database.additionally_day}\n'

                                      '————————————-\n'
                                      f'Доля акс - {dol_a}%\n'
                                      f'Доля доп - {dol_d}%\n'
                                      f'Доля кредит - 0%\n'
                                      '————————————-\n'
                                      f'ОСС - {database.oss}')


@bot.message_handler(commands=["close"])
def close(message):
    database = Database()

    general_day = database.iron_day + database.accessories_day + database.additionally_day
    bot.send_message(message.chat.id, f'{general_day=}\n'
                                      f'{database.iron_day=}\n'
                                      f'{database.accessories_day=}\n'
                                      f'{database.additionally_day=}\n'
                                      f'{database.additionally_day_plan=}\n')

    database.save(iron=database.iron + database.iron_day,
                  accessories=database.accessories + database.accessories_day,
                  additionally=int(database.additionally) + int(database.additionally_day_plan),
                  iron_day=0,
                  accessories_day=0,
                  additionally_day=0,
                  additionally_day_plan=0,
                  oss=0,
                  iron_quantity=0,
                  accessories_quantity=0,
                  acme=0,
                  rso=0,
                  rso_q=0,
                  chist=0,
                  chist_q=0)
    for i in data.users_id:
        bot.send_message(i, f'@{message.from_user.username} Закрыл смену')


@bot.message_handler(commands=["panel"])
def panel(message):
    database = Database()
    data.day = dt.date.today().day
    bot.send_message(message.chat.id, f'{database.iron_day=}\n'
                                      f'{database.accessories_day=}\n'
                                      f'{database.additionally_day=}\n'
                                      f'{database.additionally_day_plan=}\n'
                                      f'{database.iron=}\n'
                                      f'{database.accessories=}\n'
                                      f'{database.additionally=}\n\n'
                                      f'{data.day=}\n'
                                      f'{data.end_day=}')


@bot.message_handler(commands=["oss"])
def oss(message):
    database = Database()
    database.save(oss=database.oss + 1)
    bot.send_message(message.chat.id, 'Сим карта успешно продана')
    for i in data.users_id:
        bot.send_message(i, f'@{message.from_user.username} Внес симкарту')


@bot.message_handler(commands=["iron"])
def iron(message):
    data.process = 1
    bot.send_message(message.chat.id, 'Напишите сколько вы продали Железа:')


@bot.message_handler(commands=["accessories"])
def accessories(message):
    data.process = 2
    bot.send_message(message.chat.id, 'Напишите сколько вы продали Аксов:')


@bot.message_handler(commands=["additionally"])
def additionally(message):
    data.process = 3
    bot.send_message(message.chat.id, 'Напишите сколько вы продали Допов:')


@bot.message_handler(commands=["additionally_plan"])
def additionally_plan(message):
    data.process = 4
    bot.send_message(message.chat.id, 'Напишите сколько вы продали Допов для плана:')


@bot.message_handler(commands=["minus_iron"])
def additionally_plan(message):
    data.process = 5
    bot.send_message(message.chat.id, 'Напишите сколько удалить Железа:')


@bot.message_handler(commands=["minus_accessories"])
def additionally_plan(message):
    data.process = 6
    bot.send_message(message.chat.id, 'Напишите сколько удалить Аксов:')


@bot.message_handler(commands=["minus_additionally"])
def additionally_plan(message):
    data.process = 7
    bot.send_message(message.chat.id, 'Напишите сколько удалить Допов:')


@bot.message_handler(commands=["minus_additionally_plan"])
def additionally_plan(message):
    data.process = 8
    bot.send_message(message.chat.id, 'Напишите сколько удалить Допов (план):')


@bot.message_handler(commands=["akme"])
def additionally_plan(message):
    database = Database()
    database.save(acme=database.acme + 1)
    bot.send_message(message.chat.id, 'Продан Акме')
    for i in data.users_id:
        bot.send_message(i, f'@{message.from_user.username} Внес акме')


@bot.message_handler(commands=["rso"])
def additionally_plan(message):
    data.process = 9
    bot.send_message(message.chat.id, 'Напишите сколько вы продали РСО2:', )


@bot.message_handler(commands=["chist"])
def additionally_plan(message):
    data.process = 10
    bot.send_message(message.chat.id, 'Напишите на сколько вы продали Чистку')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call): ...


@bot.message_handler(content_types=["text"])
def handler_text(message):
    database = Database()
    process = data.process
    print(message.from_user.username, message.from_user.id)
    try:
        if process == 1:
            database.save(iron_day=database.iron_day + int(message.text),
                          iron_quantity=database.iron_quantity + 1)
            bot.send_message(message.chat.id,
                             f'Продано {message.text} Железа.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} внес {message.text} в железо')
        if process == 2:
            database.save(accessories_day=database.accessories_day + int(message.text),
                          accessories_quantity=database.accessories_quantity + 1)
            bot.send_message(message.chat.id,
                             f'Продано {message.text} Аксов.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} внес {message.text} в аксы')
        if process == 3:
            database.save(additionally_day=database.additionally_day + int(message.text))
            bot.send_message(message.chat.id,
                             f'Продано {message.text} Допов.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} внес {message.text} в допы')
        if process == 4:
            database.save(additionally_day_plan=database.additionally_day_plan + int(message.text))
            bot.send_message(message.chat.id,
                             f'Продано {message.text} Допов(план).')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} внес {message.text} в допы (план)')

        if process == 5:
            database.save(iron_day=database.iron_day - int(message.text),
                          iron_quantity=database.iron_quantity - 1)
            bot.send_message(message.chat.id,
                             f'Удалено {message.text} Железа.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} удалил {message.text} железа')

        if process == 6:
            database.save(accessories_day=database.accessories_day - int(message.text),
                          accessories_quantity=database.accessories_quantity - 1)
            bot.send_message(message.chat.id,
                             f'Удалено {message.text} Аксов.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} удалил {message.text} аксов')

        if process == 7:
            database.save(additionally_day=database.additionally_day - int(message.text))
            bot.send_message(message.chat.id,
                             f'Удалено {message.text} Допов.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} удалил {message.text} допов')

        if process == 8:
            database.save(additionally_day_plan=database.additionally_day_plan - int(message.text))
            bot.send_message(message.chat.id,
                             f'Удалено {message.text} Допов(план).')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} удалил {message.text} допов (план)')

        if process == 9:
            database.save(rso=database.rso + int(message.text), rso_q=database.rso_q + 1)
            bot.send_message(message.chat.id,
                             f'Продано {message.text} РСО2.')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} продал {message.text} РСО2')

        if process == 10:
            database.save(chist=database.chist + int(message.text), chist_q=database.chist_q + 1,)
            bot.send_message(message.chat.id, f'Продана {message.text} чистка')
            for i in data.users_id:
                bot.send_message(i, f'@{message.from_user.username} продал {message.text} чистки')

    except:
        bot.send_message(message.chat.id, 'Действие отменено')

    data.process = 0


bot.polling(none_stop=True, interval=0, timeout=20)

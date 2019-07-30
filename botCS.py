import telebot
from telebot import types
import sqlite3
import requests

token = "982710971:AAHQIucfeFUkm0dPapKhfkIGdkUlf1vcDyY"

bot = telebot.TeleBot(token)

conn = sqlite3.connect("BotST.db", check_same_thread=False)  #, check_same_thread=False
cursor = conn.cursor()


try:
    cursor.execute("""CREATE TABLE stell
                      (User_id integer, Username text, Phone text, Group_Id text)
                   """)
except sqlite3.OperationalError:
    print(1)



check = True
add = False


@bot.message_handler(commands=['start'])
def Start_bot(message):
    bot.send_message(
        message.chat.id,
        'Привет! :)\nИспользуй: /help,\nчтобы узнать список доступных команд!.\n',
    )


@bot.message_handler(commands=["auto"])
def auto_log(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=True, resize_keyboard=True)
    btn_1 = types.KeyboardButton(text="Регистрация/Авторизация", request_contact=True)
    btn_2 = types.KeyboardButton(text='/home')
    keyboard.add(btn_1)
    keyboard.add(btn_2)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы пройти Регистрацию/Авторизацию.", reply_markup=keyboard)


@bot.message_handler(content_types=["contact"])
def contact(message):
    global check
    if message.contact is not None:
        contact_one = message.contact
        us_id = "%s" % contact_one.user_id
        us_name = "%s" % contact_one.first_name
        phone = "%s" % contact_one.phone_number

        args = str(phone)
        cursor.execute(""" SELECT Phone FROM stell WHERE Phone = ? """, [args])
        row = cursor.fetchone()

        if row == None:
            cursor.execute('insert into stell (User_id, Username, Phone) values (?, ?, ?)', (us_id, us_name, phone))
            print(cursor.execute('select * from stell').fetchall())
            conn.commit()
            bot.send_message(message.chat.id, "Вы успешно Зарегистрировались/Авторизовались!", reply_markup=keyboard())
            check = True
            return check
        else:
            bot.send_message(message.chat.id, 'Вы уже Зарегистрированы!', reply_markup=keyboard())
            check = True
            return check


@bot.message_handler(commands=['home'])
def home(message):
    bot.send_message(message.chat.id, 'Вы находитесь на домашней странице!', reply_markup=keyboard())
    print(check)


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Создатель', url='telegram.me/Stelland'))
    bot.send_message(
        message.chat.id,
        '1) Опаааа.\n' +
        '2) Раз, два, три.\n' +
        '3) Ещё текст',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['para'])
def para(message):
    pass
    global add, cursor
    bot.send_message(message.chat.id, '123')
    group = str(message.text)
    pass
    if group == '/para' or group == 'пара':
        name = str(message.from_user.id)
        print(name)
        cursor.execute("SELECT Group_Id from stell WHERE Group_Id=? and Username = ?", [group], [name])
        row = cursor.fetchone()
        print(row)

        if row != None:
            bot.send_message(message.from_user.id, "Введите новый api key: ")
            asd1 = True

        elif asd1 == False:
            bot.send_message(message.from_user.id, "Введите api key: ")
            asd = True
            print(asd)

    elif asd1 == True:
        conn = pymysql.connect('91.134.194.237', 'gs9966', 'STelland3102YT', 'gs9966')
        cursor = conn.cursor()
        name = message.from_user.id
        print(name)
        query = "SELECT `user_id` FROM `users` WHERE api_key = %s"
        args = str(message.text)
        cursor.execute(query, args)
        row = cursor.fetchone()

        if row == None:
            query = "UPDATE `users` SET `api_key`= %s WHERE user_id = %s "
            args = str(message.text), (str(name))
            print(args)
            cursor.execute(query, args)
            conn.commit()
            conn.close()
            print(message.text)
            asd1 = False
            bot.send_message(message.from_user.id, "api key - Привязан успешно!", reply_markup=keyboard())
            print(asd)
        else:
            bot.send_message(message.from_user.id, 'Данный api key уже используется!', reply_markup=keyboard())
            asd1 = False

    # if check == True:
    #     servstop = "https://www.ks54.ru/Студенту/Расписание_On-Line?group=" % text
    #     print(servstop)
    #     # requests.post(servstop)
    #     bot.send_message(message.from_user.id, "Выполнено", reply_markup=keyboard())
    # else:
    #     bot.send_message(message.chat.id, 'Войдите или зарегистрируйтесь, чтобы использовать данную функцию!')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global add


    # if message.text == "/para":
    #         if check == True:
    #             bot.send_message(message.chat.id, 'Ыыыыыы')
    #             pass
    #         else:
    #             bot.send_message(message.chat.id, 'Войдите или зарегистрируйтесь, чтобы использовать данную функцию!')
    if message.text == 'Group':
        msg = bot.send_message(message.chat.id, '<b>Введите группу</b>', parse_mode="HTML")
        bot.register_next_step_handler(msg, para)


    print(check)


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('/help')
    btn2 = types.KeyboardButton('/para')
    btn3 = types.KeyboardButton('/auto')
    btn4 = types.KeyboardButton('Group')
    markup.add(btn1, btn2)
    markup.add(btn4)
    markup.add(btn3)
    return markup


bot.polling(none_stop=True, interval=0)

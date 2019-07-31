import telebot
from telebot import types
import sqlite3

token = '918573896:AAEM0r2hDXAJoCwy5WtTFZJ92iEmhxmoVeM'
bot = telebot.TeleBot(token)

conn = sqlite3.connect('game.db', check_same_thread=False)
cursor = conn.cursor()

try:
    cursor.execute('''CREATE TABLE game 
                    (User_ID integer, Score integer, business text)
                    ''')
except sqlite3.OperationalError:
    pass

score = 0
check = False
gg = False


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Ты зашёл в нашу игру!', reply_markup=keyboard())


@bot.message_handler(commands=["Login"])
def auto_log(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=True, resize_keyboard=True)
    btn_1 = types.KeyboardButton(text="Регистрация/Авторизация", request_contact=True)
    btn_2 = types.KeyboardButton(text='/home')
    keyboard.add(btn_1)
    keyboard.add(btn_2)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы пройти Регистрацию/Авторизацию.", reply_markup=keyboard)


@bot.message_handler(content_types=["contact"])
def contact(message):
    global check, score
    if message.contact is not None:
        contact_one = message.contact
        us_id = "%s" % contact_one.user_id

        args = int(us_id)
        cursor.execute(""" SELECT User_ID FROM game WHERE User_ID = ? """, [args])
        row = cursor.fetchone()

        if row == None:
            cursor.execute('insert into game (User_id, Score) values (?, ?)', (us_id, score))
            print(cursor.execute('select * from game').fetchall())
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


def get_info(message):
    uid_new = message.text
    us_id = message.from_user.id
    print(uid_new)
    if uid_new == '1':
        bus = 'Магнит'
        # cursor.execute("INSERT INTO game(business) VALUES (?) WHERE User_ID = ?''', [us_id]
        # conn.commit()
        cursor.execute('''UPDATE game SET business = 'Магнит' WHERE User_ID = ?''', [us_id])
        conn.commit()
        bot.send_message(message.chat.id, 'Вы преобрели: Магнит', reply_markup=keyboard())
    elif uid_new == '2':
        cursor.execute('''UPDATE game SET business = 'Пятёрочка' WHERE User_ID = ?''', [us_id])
        conn.commit()
        bot.send_message(message.chat.id, 'Вы преобрели: Пятёрочку', reply_markup=keyboard())
    elif uid_new == '3':
        cursor.execute('''UPDATE game SET business = 'DNS' WHERE User_ID = ?''', [us_id])
        conn.commit()
        bot.send_message(message.chat.id, 'Вы преобрели: DNS', reply_markup=keyboard())
    else:
        bot.send_message(message.chat.id, 'Ошибка!', reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    global gg, check
    text = message.text
    if text == 'Привет' or text == 'привет':
        bot.send_message(message.chat.id, 'Хааааай', reply_markup=keyboard())
    elif text == 'Ваш баланс' or text == 'Баланс':
        us_id = str(message.from_user.id)
        cursor.execute("SELECT Score from game WHERE User_ID=?", [us_id])
        row = cursor.fetchone()
        us_score = row[0]
        bot.send_message(message.chat.id, 'Ваш баланс: ' + str(us_score) + ' монет.')
        print(row[0])
    elif text == 'Купить':
        sent = bot.send_message(message.chat.id, 'Выберите бизнес:\n1- Магнит\n2- Пятёрочка\n3- DNS')
        bot.register_next_step_handler(sent, get_info)
        # us_id = str(message.from_user.id)
        # cursor.execute("SELECT business from game WHERE User_ID=?", [us_id])
        # row = cursor.fetchone()
        # us_buy = str(row[0])
        # print(us_buy)
        #
        # if us_buy != 'None':
        #     pass
        # elif gg == False:
        #     bot.send_message(message.from_user.id, "Выберите бизнес:\n1 Магнит\n2 Пятёрочка\n3 DNS")
        #
        #     gg = True
        #     print(gg)
        #     if gg == True:
        #         bot.send_message(message.from_user.id, "Вы приобрели бизнес!")

    elif text == 'Мои Бизнесы' or text == 'Бизнесы':
        us_id = str(message.from_user.id)
        cursor.execute("SELECT business from game WHERE User_ID=?", [us_id])
        row = cursor.fetchone()
        us_bus = str(row[0])
        if us_bus == 'None':
            bot.send_message(message.chat.id, 'У Вас нет бизнесов.')
        else:
            bot.send_message(message.chat.id, 'Ваши бизнесы: ' + str(us_bus))
        print(row[0])
    elif text == 'Получить монеты':

        us_id = str(message.from_user.id)
        cursor.execute("SELECT business from game WHERE User_ID=?", [us_id])
        row = cursor.fetchone()
        business = str(row[0])
        if business == 'Магнит':
            cursor.execute(''' update game set Score=Score+10 where User_ID=?''', [us_id])
            conn.commit()
            bot.send_message(message.chat.id, 'Вы получили 10 очков')
        elif business == 'Пятёрочка':
            cursor.execute(''' update game set Score=Score+50 where User_ID=?''', [us_id])
            conn.commit()
            bot.send_message(message.chat.id, 'Вы получили 50 очков')
        elif business == 'DNS':
            cursor.execute(''' update game set Score=Score+100 where User_ID=?''', [us_id])
            conn.commit()
            bot.send_message(message.chat.id, 'Вы получили 100 очков')
        else:
            bot.send_message(message.chat.id, 'У Вас нет бизнесов!')
    elif text == 'Help' or text == 'Помощь':
        bot.send_message(message.chat.id, 'Помощь во всём!!!', reply_markup=keyboard())
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю!', reply_markup=keyboard())








def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_1 = types.KeyboardButton('Help')
    btn_2 = types.KeyboardButton('/Login')
    btn_3 = types.KeyboardButton('Баланс')
    btn_4 = types.KeyboardButton('Купить')
    btn_5 = types.KeyboardButton('Мои Бизнесы')
    btn_6 = types.KeyboardButton('Получить монеты')
    markup.add(btn_1, btn_3)
    markup.add(btn_4, btn_5)
    markup.add(btn_6)
    markup.add(btn_2)
    return markup


bot.polling(none_stop=True, interval=0)

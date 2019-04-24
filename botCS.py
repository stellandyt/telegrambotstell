import telebot
import pyowm
# import logging
# from flask import Flask, request
# import os
from telebot import types


bot = telebot.TeleBot("767640365:AAGLF3nApdXdsJUYXMC-V5VDRIiMaLYoGN8")
owm = pyowm.OWM('c687e4132128127329716ffed7313e70', language='ru')

texty = ''
asd = False


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global asd
    if message.text == 'Погода':
        bot.send_message(message.chat.id, "Введите город/страну!")
        texty = message.text

        if message.text == 'Абакан' or 'Азов' or 'Александров' or 'Алексин' or 'Альметьевск' or 'Анапа' or 'Ангарск' or 'Анжеро-Судженск' or 'Апатиты' or 'Арзамас' or 'Армавир' or 'Арсеньев' or 'Артем':
            asd = True
        else:
            bot.send_message(message.from_user.id, "Вы ввели неправильный город", reply_markup=keyboard())

    elif asd == True:
        texty = message.text
        observation = owm.weather_at_place(texty)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')["temp"]

        answer = "В городе " + texty + " сейчас: " + w.get_detailed_status() + "\n"
        answer += "Температура сейчас в районе: " + str(temp)

        bot.send_message(message.from_user.id, answer)
        print(answer)
        asd = False
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю :(", reply_markup=keyboard())

# @bot.message_handler(content_types=['text'])
# def get_message(message):
#     if message.text == "Помощь" or message.text == "/help":
#         bot.send_message(message.from_user.id, "Воспользуйтесь специальной клавиатурой снизу или же используйте команды:\n /start\n /stop\n /status \n /load \n /restart \n /update \n P.S На команды можно нажимать :)")
#     else:
#         bot.send_message(message.from_user.id, "гг")

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Погода')
    markup.add(btn1)
    return markup


# if "HEROKU" in list(os.environ.keys()):
#     logger = telebot.logger
#     telebot.logger.setLevel(logging.INFO)

#     server = Flask(__name__)

#     @server.route("/bot", methods=['POST'])
#     def getMessage():
#         bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#         return "!", 200

#     @server.route("/")
#     def webhook():
#         bot.remove_webhook()
#         bot.set_webhook(url="https://dashboard.heroku.com/apps/csservbot") # этот url нужно заменить на url вашего Хероку приложения
#         return "?", 200
#     server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
# else:
#     # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
#     # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
#     bot.remove_webhook()
#     bot.polling(none_stop=True)

bot.polling(none_stop=True, interval=0)

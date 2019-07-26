import telebot
import pyowm
# import logging
# from flask import Flask, request
# import os
from telebot import types

token = "767640365:AAGLF3nApdXdsJUYXMC-V5VDRIiMaLYoGN8"
tokenOWM = "c687e4132128127329716ffed7313e70"

bot = telebot.TeleBot(token)
owm = pyowm.OWM(tokenOWM, language='ru')


aaa = False
city = ""


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # global aaa, city
    # bot.send_message(message.chat.id, "Введите город/страну!")
    city = message.text
    aaa = True

    if aaa == True:
        try:
            observation = owm.weather_at_place(city)
            w = observation.get_weather()
            temp = w.get_temperature('celsius')["temp"]

            answer = "В городе " + city + " сейчас: " + w.get_detailed_status() + "\n"
            answer += "Температура сейчас в районе: " + str(temp)

            bot.send_message(message.from_user.id, answer)
            print(answer)
            asd = False

        except pyowm.exceptions.api_response_error.NotFoundError:
            bot.send_message(message.from_user.id, "Я тебя не понимаю :(", reply_markup=keyboard())


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Погода')
    markup.add(btn1)
    return markup


bot.polling(none_stop=True, interval=0)

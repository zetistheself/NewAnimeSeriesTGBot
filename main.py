import telebot
from telebot import types
from Globals import *
from bs4 import BeautifulSoup as bs
import requests
from keep_alive import keep_alive
import sqlite3


TOKEN = get_token()


db = sqlite3.connect('data.sqlite3')
cur = db.cursor()


def get_today_anime():
    r = requests.get(get_url())
    html = bs(r.text, 'lxml')
    today_list = html.findAll('div', class_='last-update-container scroll collapse show')[1].findAll('div', class_='list-group-item list-group-item-action border-left-0 border-right-0 border-bottom-0')
    answer = []
    for i in today_list:
        answer.append(f"{i.find('div', class_='media-body').find('div', class_='d-flex align-items-center').find('div', class_='ml-3 text-right').find('div', class_='text-gray-dark-6 text-truncate').text[-6:-4]}:{i.find('div', class_='media-body').find('div', class_='d-flex align-items-center').find('div', class_='ml-3 text-right').find('div', class_='text-gray-dark-6 text-truncate').text[-3:-1]} -- {i.find('div', class_='media-body').find('div', class_='d-flex align-items-center').find('div', class_='d-flex mr-auto').text} ({i.find('div', class_='media-body').find('div', class_='d-flex align-items-center').find('div', class_='ml-3 text-right').find('div', class_='font-weight-600 text-truncate').text})\n")
    return answer


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute('SELECT id FROM Subscribers')
    fetch = cur.fetchall()
    if tuple([message.chat.id]) not in fetch:
        markup_1.add(types.KeyboardButton('Включить уведомления!✅'))
    else:
        markup_1.add(types.KeyboardButton('Выключить уведомления!❌'))
    markup_1.add(types.KeyboardButton('Сегодняшнее расписание аниме!📅'))
    bot.send_message(message.chat.id, f"Привет!👋\n\nЭто бот для получения уведомлений о выходе новых серий аниме.🔔\n\nЕсли захочешь сможешь отключить их в любой момент!\n\nСоздатель:@adilkaSSS",reply_markup=markup_1)


@bot.message_handler(content_types=['text'])
def read_text(message):
    if message.text == 'Сегодняшнее расписание аниме!📅':
        text = get_today_anime()
        answer = ''
        for i in sorted(text):
            answer += i + '\n'
        try:
            bot.send_message(message.chat.id, answer)
        except:
            bot.send_message(message.chat.id, 'Пока нет😓')
    elif message.text == 'Выключить уведомления!❌':
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_1.add(types.KeyboardButton('Включить уведомления!✅'))
        markup_1.add(types.KeyboardButton('Сегодняшнее расписание аниме!📅'))
        cur.execute(f"DELETE FROM Subscribers WHERE id={message.chat.id}")
        db.commit()
        bot.send_message(message.chat.id, "Теперь ты не будешь получать уведомления!🔕", reply_markup=markup_1)
    elif message.text == 'Включить уведомления!✅':
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_1.add(types.KeyboardButton('Выключить уведомления!❌'))
        markup_1.add(types.KeyboardButton('Сегодняшнее расписание аниме!📅'))
        cur.execute('SELECT id FROM Subscribers')
        fetch = cur.fetchall()
        if tuple([message.chat.id]) in fetch:
            bot.send_message(message.chat.id, f"Вы уже получаете уведомления!🔔")
        else:
             cur.execute(f"""
                INSERT INTO Subscribers VALUES
                    ({message.chat.id})
             """)
             db.commit()
             bot.send_message(message.chat.id, f"Теперь вы будете получать уведомления!📢", reply_markup=markup_1)

keep_alive()
bot.infinity_polling()

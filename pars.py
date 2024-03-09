from bs4 import BeautifulSoup as bs
import requests
from Globals import *
import telebot
import time
from telebot import types
import psycopg2


bot = telebot.TeleBot(get_token())


db = psycopg2.connect('postgres://adilka:XG7hOpA6q5lOinRtltyv271PZ8PB6vph@dpg-cka3cqfs0fgc739f48kg-a.singapore-postgres.render.com/main_wp2z')
cur = db.cursor()


while True:
    r = requests.get('https://animego.org')
    html = bs(r.text, 'lxml')
    cur.execute('SELECT name FROM LIST')
    fetch = cur.fetchall()
    try:
        name = html.find('span', class_="last-update-title font-weight-600").text
        ser = html.find('div', class_='ml-3 text-right').find("div", 'font-weight-600 text-truncate').text
        if tuple([name + ser]) not in fetch:
            res = name + ser
            cur.execute(f"INSERT INTO LIST VALUES('{res}')")
            cur.execute('SELECT id FROM Subscribers')
            db.commit()
            fetch = cur.fetchall()
            for i in fetch:
                markup = types.InlineKeyboardMarkup()
                URL = 'https://animego.org' + html.find('div', class_='last-update-item list-group-item list-group-item-action border-left-0 border-right-0 border-bottom-0 border-top-0 cursor-pointer').get('onclick')[15:-1]
                markup.add(types.InlineKeyboardButton('Смотреть🎬', url=URL))
                bot.send_message(i[0], f'{name} ({ser})', reply_markup=markup)
    except Exception:
        try:
            url = html.find('div', class_='last-update-item list-group-item list-group-item-action border-left-0 border-right-0 border-bottom-0 border-top-0 cursor-pointer').get('onclick')[15:-1]
            bot.send_message(950479413, f"Error was found\nLink:{r.url}")
        except Exception:
            bot.send_message(950479413, f"Error was found\nUrl not found")
    time.sleep(60)
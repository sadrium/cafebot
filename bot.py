import telebot
from telebot import types

bot = telebot.TeleBot('1191270917:AAGrJS2Xhky93Q-BERhcWDEN0izqhNykaWU')

otvety = []
# для кнопок станций
stancii = {}
with open('stanc.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        line = line.split('|')
        list1 = []
        for i in range(0, len(line)):
            if i > 0:
                list1.append(line[i])
        dict1 = {line[0]: list1}
        stancii.update(dict1)

# команда старт
@bot.message_handler(commands=['start'])
def start(message):
    send_mess = "Привет! Где ты хочешь поесть?"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    pl1 = types.KeyboardButton('Кофейня')
    pl2 = types.KeyboardButton('Ресторан')
    pl3 = types.KeyboardButton('Фастфуд')
    markup.add(pl1, pl2, pl3)

    bot.send_message(message.chat.id, send_mess, reply_markup=markup)
    bot.register_next_step_handler(message, vetka)

# тут начинается опрос пользователя, выясняем, чего он хочет
@bot.message_handler(content_types=['text'])

# кнопки для веток
def vetka(message):
    vetki = ['красная','оранжевая', 'желтая', 'зеленая', 'салатовая', 'голубая', 'синяя', 'фиолетовая', 'серая', 'кольцевая']
    mesta = ['кофейня', 'ресторан', 'фастфуд']
    a = message.text.lower()
    if a in mesta:
        otvety.append(a)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for vetochka in vetki:
            knopka = types.KeyboardButton(vetochka)
            markup.add(knopka)
        bot.send_message(message.chat.id, 'Выбери ветку', reply_markup=markup)
        bot.register_next_step_handler(message, station)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        pl1 = types.KeyboardButton('Кофейня')
        pl2 = types.KeyboardButton('Ресторан')
        pl3 = types.KeyboardButton('Фастфуд')
        markup.add(pl1, pl2, pl3)
        bot.send_message(message.chat.id, 'Пожалуйста, нажми на кнопку', reply_markup=markup)
        bot.register_next_step_handler(message,vetka)

def station(message):

    b = message.text.lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for key, value in stancii.items():
        if key == b:
            otvety.append(b)
            for l in value:
                knopkanew = types.KeyboardButton(l)
                markup.add(knopkanew)
            bot.send_message(message.chat.id, 'Выбери станцию', reply_markup=markup)
            bot.register_next_step_handler(message, konets)

    if b not in stancii.keys():

        vetki = ['красная', 'оранжевая', 'желтая', 'зеленая', 'салатовая', 'голубая', 'синяя', 'фиолетовая',
                     'серая', 'кольцевая']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for vetochka in vetki:
            knopka = types.KeyboardButton(vetochka)
            markup.add(knopka)
        bot.send_message(message.chat.id, 'Пожалуйста, нажми на кнопку', reply_markup=markup)
        bot.register_next_step_handler(message, station)


def konets(message):

    k = message.text
    n = 0
    for value in stancii.values():

        if k in value:
            n = n+1

    if n >= 1:

        k = message.text.lower()
        otvety.append(k)
        with open('final_sp.txt', encoding='utf-8') as f:
            text = f.read()
        lines = text.split("\n")
        words = []
        final_message = []
        for line in lines:
            words = line.split('#')
            if words[:3] == otvety[:3]:
                final_message.append(words[-1])
        st = ', '.join(final_message)
        stroka = 'Вот что я для тебя нашел: ' + st
        bot.send_message(message.chat.id, stroka)
        otvety.clear()

    else:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for key, value in stancii.items():
            if key == otvety[1]:
                for l in value:
                    knopkanew = types.KeyboardButton(l)
                    markup.add(knopkanew)
                bot.send_message(message.chat.id, 'Выбери станцию', reply_markup=markup)
                bot.register_next_step_handler(message, konets)



bot.polling(none_stop=True)

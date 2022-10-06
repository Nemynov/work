import telebot
from extensions import Converter, ConversionException
from config import keys, TOKEN



bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работать, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>\n\
Увидеть список всех доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) !=3:
            raise ConversionException('Число параметров не равно трём')

        total_cost = Converter.convert(values)

    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.reply_to(message, f'{values[2]} {values[0]} = {total_cost} {values[1]}')

bot.polling(none_stop=True)
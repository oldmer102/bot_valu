from get_params import get_config, get_data_msg, get_list_currencies
import telebot
from api import GetPrice


BOT = telebot.TeleBot(get_config('token'))


@BOT.message_handler(commands=["start"])
def start_message(message):
    BOT.send_message(message.chat.id, "Привет ✌\n Я бот для конвертации валют ")


@BOT.message_handler(commands=["help"])
def help_message(message):
    BOT.send_message(
        message.chat.id,
        f"Давай помогу с примерами как я работаю. Для начала необходимо запросить список валют, взятый из ЦБ РФ "
        f". Пример работы: EUR RUB 20",
    )


@BOT.message_handler(commands=["values"])
def values_help_message(message):
    BOT.send_message(
        message.chat.id,
        "Список всех валют которые я знаю: \n" + get_data_msg() + "RUB: Российский рубль",
    )


@BOT.message_handler(content_types=['text'])
def test_message(message):
    data = message.text.split(" ")
    price = GetPrice(base=data[0], quote=data[1], amount=data[2], rule=get_list_currencies())
    if not price.conversion_rule():
        BOT.send_message(
            message.chat.id, "Я не знаю валюту: " + price.conversion_rule()
        )
    BOT.send_message(message.chat.id, f"{price.conversion()} {price.conversion_rule()}")

if __name__ == "__main__":
    BOT.infinity_polling()



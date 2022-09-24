import telebot
import requests
from api import GetPrice
import time

DATA = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
MSG = ""
LIST_CURRENCIES = []
for i in DATA["Valute"]:
    url = f"https://api.coingate.com/v2/rates/merchant/{i}/RUB"
    try:
        requests.get(url).json()
        MSG += i + ": " + DATA["Valute"][i]["Name"] + "\n"
        LIST_CURRENCIES.append(i)
    except requests.exceptions.JSONDecodeError:
        pass

TOKEN = "5651013243:AAGE7cnaRXUXgAqDzaNJS8Nip03g3XLVCw8"

BOT = telebot.TeleBot(TOKEN)


@BOT.message_handler(commands=["start"])
def start_message(message):
    BOT.send_message(message.chat.id, "Привет ✌\n Я бот для конвертации валют ")


@BOT.message_handler(commands=["help"])
def help_message(message):
    BOT.send_message(
        message.chat.id,
        f"Давай помогу с примерами как я работаю. Для начала необходимо запросить список валют, которые мне предоставляет ЦБ РФ.  Если мы ходим конвертировать валюту в рубли необходимо написать короткое название валюты и сумму, которую хотим узнать: EUR 20",
    )


@BOT.message_handler(commands=["values"])
def values_help_message(message):
    BOT.send_message(
        message.chat.id,
        "Список всех валют которые я знаю: \n" + MSG + "RUB: Российский рубль",
    )


@BOT.message_handler(content_types=["text"])
def test_message(message):
    data = message.text.split(" ")
    price = GetPrice(base=data[0], quote=data[1], amount=data[2], rule=LIST_CURRENCIES)
    if not price.conversion_rule():
        BOT.send_message(
            message.chat.id, "Я не знаю валюту: " + price.conversion_rule()
        )
    BOT.send_message(message.chat.id, f"{price.conversion()} {price.conversion_rule()}")


BOT.infinity_polling()

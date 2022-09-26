from get_params import get_config, get_data_msg
import telebot
from extensions import GetPrice, MyError


BOT = telebot.TeleBot(get_config('token'))


@BOT.message_handler(commands=["start"])
def start_message(message):
    BOT.send_message(message.chat.id, "Привет ✌\n Я бот для конвертации валют, для подробной информации нажми сюда --> /help")


@BOT.message_handler(commands=["help"])
def help_message(message):
    BOT.send_message(
        message.chat.id,
        f"Давай помогу с примерами как я работаю. Для начала необходимо запросить список валют, взятый из ЦБ РФ командой --> /values "
        f"После выбора нужных валют введи значения в следующей последовательности: <Короткое имя валюты, "
        f"цену которой хотим узнать> <Короткое имя валюты, в которой надо узнать цену первой валюты> <Количество первой "
        f"валюты> Пример работы: EUR RUB 20  Важно! Запись делать используя пробелы",


    )


@BOT.message_handler(commands=["values"])
def values_help_message(message):
    BOT.send_message(
        message.chat.id,
        "Список всех валют которые я знаю: \n" + get_data_msg()[0] + "RUB: Российский рубль",
    )


@BOT.message_handler(content_types=['text'])
def test_message(message):
    data = message.text.split(" ")
    if len(data) == 3:
        price = GetPrice(base=data[0], quote=data[1], amount=data[2], rule=get_data_msg()[1])
        try:
            if not price.conversion_rule()[0]:
                BOT.send_message(
                    message.chat.id, "Ошибка: " + price.conversion_rule()[1]
                )
                raise MyError

            else:
                BOT.send_message(message.chat.id, f"{price.conversion()} {price.conversion_rule()}")
        except MyError:
            print('Былло введено не коректое значение!')
    else:
        BOT.send_message(message.chat.id, 'Даныые введены не коректно! нажмите сюда --> /help для просмотра инструкции')


if __name__ == "__main__":
    #Предзагрузка файлов, дождитесь вывода информации
    get_data_msg()
    #Старт бота
    BOT.infinity_polling()

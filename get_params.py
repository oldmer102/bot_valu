import os.path
from file_read_backwards import FileReadBackwards
import requests


def get_config(param):
    with FileReadBackwards(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'), encoding="utf-8") as f:
        for line in f:
            s = line.replace('\n', '')
            if s[0:1] != '#' and s[0:s.find(':')] == param:
                return s[s.find(':') + 1:].strip()


def get_data_msg():
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    msg = ""

    for i in data["Valute"]:
        url = f"https://api.coingate.com/v2/rates/merchant/{i}/RUB"
        try:
            requests.get(url).json()
            msg += i + ": " + data["Valute"][i]["Name"] + "\n"
        except requests.exceptions.JSONDecodeError:
            pass
    return msg


def get_list_currencies():
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    list_currencies = []
    for i in data["Valute"]:
        url = f"https://api.coingate.com/v2/rates/merchant/{i}/RUB"
        try:
            requests.get(url).json()
            list_currencies.append(i)
        except requests.exceptions.JSONDecodeError:
            pass
    return list_currencies

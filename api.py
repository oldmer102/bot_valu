import requests


class GetPrice():
    def __init__(self, base, quote, amount, rule):
        self.base = base
        self.quote = quote
        self.amount = amount
        self.rule = rule

    def conversion_rule(self):
        k = 0
        p = 0
        for i in self.rule:
            if self.base == i or self.base == 'RUB':
                k = 1
            if self.quote == i or self.quote == 'RUB':
                p = 1
            if k == 0:
                return self.base
            if p == 0:
                return self.quote
            if k == 1 and p == 1:
                return self.quote

    def conversion(self):
        data = requests.get(f'https://api.coingate.com/v2/rates/merchant/{self.base}/{self.quote}').json()
        return data * int(self.amount)





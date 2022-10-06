import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(values: list):
        val1, val2, amount = values
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}')

        if not (val1 in keys and val2 in keys):
            raise  ConversionException('Вы ввели валюту, которой нет в списке /values')

        if val1 == val2:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {val1}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[val1]}&tsyms={keys[val2]}')
        total_cost = float(json.loads(r.content)[keys[val2]]) * amount

        return total_cost

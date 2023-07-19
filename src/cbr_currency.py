import requests
from configparser import ParsingError


def currency_transfer():
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    except ParsingError:
        print('Ошибка доступа к API ЦБ. Данные по валютам будут от 22.07.2023')
        currency_data = {
            'RUB': 1,
            'RUR': 1,
            'USD': 83.6077,
            'GBP': 106.441,
            'BYN': 28.0563,
            'BGN': 46.6926,
            'EUR': 91.943,
            'UAH': 22.6376/10,
            'KZT': 18.6875/100,
            'CAD': 63.4208,
            'CNY': 11.6221,
            'SGD': 62.3659,
            'JPY': 58.9285/100,
            'UZS': 72.7023/10000,
        }
        return currency_data
    else:
        currency_data = {
            'RUB': 1,
            'RUR': 1,
            'USD': data['Valute']['USD']['Value']/data['Valute']['USD']['Nominal'],
            'GBP': data['Valute']['GBP']['Value']/data['Valute']['GBP']['Nominal'],
            'BYN': data['Valute']['BYN']['Value']/data['Valute']['BYN']['Nominal'],
            'BGN': data['Valute']['BGN']['Value']/data['Valute']['BGN']['Nominal'],
            'EUR': data['Valute']['EUR']['Value']/data['Valute']['EUR']['Nominal'],
            'UAH': data['Valute']['UAH']['Value']/data['Valute']['UAH']['Nominal'],
            'KZT': data['Valute']['KZT']['Value']/data['Valute']['KZT']['Nominal'],
            'CAD': data['Valute']['CAD']['Value']/data['Valute']['CAD']['Nominal'],
            'CNY': data['Valute']['CNY']['Value']/data['Valute']['CNY']['Nominal'],
            'SGD': data['Valute']['SGD']['Value']/data['Valute']['SGD']['Nominal'],
            'JPY': data['Valute']['JPY']['Value']/data['Valute']['JPY']['Nominal'],
            'UZS': data['Valute']['UZS']['Value']/data['Valute']['UZS']['Nominal'],
        }
        return currency_data

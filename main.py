# pip install requests, pytelegrambotapi, wheel, telebot
import requests
from datetime import datetime
import telebot
from auth_data import token  # it is token for telegram bot


def get_data():
    req = requests.get('https://yobit.net/api/3/ticker/btc_usdt')
    response = req.json()
    # print(response)

    sell_price = response['btc_usdt']['sell']

    return f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nSell BTC price: {sell_price}'


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @ bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hello friend! Write the name of the crypto to find out the cost.'
                                          '\nBTC, ETH, USDC, BUSD, LTC, TONCOIN, XRP, DOGE')

    @ bot.message_handler()
    def send_text(message):
        if message.text.lower() in {"btc", "eth", "usdc", "ltc", "busd", "toncoin", "xrp", "doge"}:
            try:
                req = requests.get(f'https://yobit.net/api/3/ticker/{message.text.lower()}_usdt')
                response = req.json()
                sell_price = response[f'{message.text.lower()}_usdt']['sell']
                bot.send_message(message.chat.id,
                                 f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nSell {message.text.upper()} price: {sell_price}')
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, "Something was wrong...")
        else:
            bot.send_message(message.chat.id, "Incorrect command")

    bot.polling()


def main():
    # print(get_data())
    telegram_bot(token)


if __name__ == '__main__':
    main()

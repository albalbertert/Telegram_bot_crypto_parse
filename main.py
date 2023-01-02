import pandas as pd
from binance import Client
import requests
from datetime import datetime
import telebot
from auth_data import token  # This is the token for telegram bot. You can get token from BotFather in telegram.
from api_keys import api_key, secret_key  # These are the keys for the Binance access. You can get keys in Binance.
# https://www.binance.com/ru/my/settings/api-management


def get_data_binance(coin):
    client = Client(api_key, secret_key)
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    usdt = ticker_df[ticker_df.symbol.str.contains('USDT')]
    usdt = usdt[~((usdt.symbol.str.contains('UP')) | (usdt.symbol.str.contains('DOWN')))]
    usdt.set_index('symbol', inplace=True)
    coin_pair = coin.upper() + 'USDT'
    try:
        price = float(usdt.loc[coin_pair].price)
    except:
        price = None
        # print('Coin isn\'t found.')
    return price


def get_data(coin):
    req = requests.get(f'https://yobit.net/api/3/ticker/{coin.lower()}_usdt')
    response = req.json()
    # print(response)
    try:
        sell_price = response[f'{coin.lower()}_usdt']['sell']
    except:
        sell_price = None
        # print('Coin isn\'t found.')
    return sell_price


def telegram_bot(token_):
    bot = telebot.TeleBot(token_)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, 'Hello.\n'
                                          'Please select from which exchange you want to get data '
                                          '(1 - for Binance, 2- for YObit). '
                                          'Then write the name of the crypto to find out the cost.'
                                          '\nFor example: 1 - BTC, 2 - ETH, 2 - TONCOIN', parse_mode='html')

    @bot.message_handler()
    def get_user_text(message):
        mess_list = message.text.split('-')
        mess_list = [i.strip() for i in mess_list]
        if len(mess_list) == 2 and mess_list[0] == '1':
            try:
                price = get_data_binance(mess_list[1])
                if price:
                    bot.send_message(message.chat.id, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                                                      f'Sell {mess_list[1].upper()} price: {price}', parse_mode='html')
                else:
                    bot.send_message(message.chat.id, 'The wrong name of the cryptocurrency, '
                                                      'or this cryptocurrency is absent in the Binance exchange.',
                                     parse_mode='html')
            except Exception as ex:
                bot.send_message(message.chat.id, f"Something was wrong.\n{ex}", parse_mode='html')

        elif len(mess_list) == 2 and mess_list[0] == '2':
            try:
                price = get_data(mess_list[1])
                if price:
                    bot.send_message(message.chat.id, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                                                      f'Sell {mess_list[1].upper()} price: {price}')
                else:
                    bot.send_message(message.chat.id, 'The wrong name of the cryptocurrency, '
                                                      'or this cryptocurrency is absent in the YObit exchange.',
                                     parse_mode='html')
            except Exception as ex:
                bot.send_message(message.chat.id, f"Something was wrong.\n{ex}", parse_mode='html')

        else:
            bot.send_message(message.chat.id, 'Wrong data, try again.', parse_mode='html')

    bot.polling()


def main():
    # print(get_data('toncoin'))
    # print(get_data_binance('btc'))
    telegram_bot(token)


if __name__ == '__main__':
    main()

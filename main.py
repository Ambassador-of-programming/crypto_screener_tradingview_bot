import concurrent.futures
import os
import telebot
import pandas as pd
import datetime as dt
import plotly.graph_objects as go

from time import sleep
from telebot import types
from coin_data import pd_datas
from config.TOKEN_telegram import TOKEN
from tradingview_ta import TA_Handler, Interval, Exchange


# Перечисляем монеты которые мы собираемся анализировать
all_coins = pd.Series(['BTCUSDT', 'ETHUSDT', 'DOGE_USDT', 'BNBUSDT',], copy=False)

while True:
    # Подключаем телеграм бота и вставляем токен
    bot = telebot.TeleBot(TOKEN, parse_mode=None)

    # Указываем группу в которую будет присылать всю информацию
    name_channel = '@HereWriteTelegramGroup'
    
    
    def moving_averages():
        for coin in all_coins:
            tesla = TA_Handler(
                symbol=coin,
                exchange="BINANCE",
                screener="CRYPTO",
                interval=Interval.INTERVAL_4_HOURS, 
            )

        # Устанавливаем стратегию основанную на moving_averages  
        rec = tesla.get_analysis().moving_averages

        def strong_buy():
            if rec['RECOMMENDATION'] == 'STRONG_BUY':
                today = dt.datetime.now()
                one_month_ago = today - dt.timedelta(days=2)
                dataset = pd_datas(coin, '5m', one_month_ago, today)
                dataset['Datetime'] = dataset['Datetime'].map(lambda x: dt.datetime.fromtimestamp(x / 1000.0))
                dataset['new'] = dataset['Datetime']

                fig = go.Figure([go.Scatter(x=dataset['Datetime'], y=dataset['Close'])])
                fig.update_layout(title=f"Монета: {coin}  Время: {dt.datetime.now()}")
                fig.write_image("image/strong_buy_moving_averages.png", scale=5)
                bot.send_photo(name_channel, photo=open('image/strong_buy_moving_averages.png', 'rb'))

                link = f"https://www.binance.com/ru/futures/{coin}"
                markup = types.InlineKeyboardMarkup()
                link_button = types.InlineKeyboardButton(text='Посмотреть на Binance', url=link)
                markup.add(link_button)
                bot.send_message(name_channel, f'''
💣Есть сигнал на STRONG BUY\n
🧠Стратегия на: moving_averages\n
🥇Название монеты: {coin}\n
📈Актуальная цена: {dataset.tail(1)['Close'].value_counts().index[-1]}\n
👇Минимальная цена за последние 2 дня: {dataset["Close"].min()} ({dataset.loc[dataset["Close"].idxmin(), "Datetime"]})\n
👆Максимальная цена за последние 2 дня: {dataset["Close"].max()} ({dataset.loc[dataset["Close"].idxmax(), "Datetime"]})\n
💰Средняя цена за последние 2 дня: {dataset["Close"].mean()}
                ''', reply_markup=markup)
                os.remove("image/strong_buy_moving_averages.png")
                sleep(1800)

        def strong_sell():
            if rec['RECOMMENDATION'] == 'STRONG_SELL':
                today = dt.datetime.now()
                one_month_ago = today - dt.timedelta(days=2)
                dataset = pd_datas(coin, '5m', one_month_ago, today)
                dataset['Datetime'] = dataset['Datetime'].map(lambda x: dt.datetime.fromtimestamp(x / 1000.0))
                dataset['new'] = dataset['Datetime']

                fig = go.Figure([go.Scatter(x=dataset['Datetime'], y=dataset['Close'])])
                fig.update_layout(title=f"Монета: {coin}  Время: {dt.datetime.now()}")
                fig.write_image("image/strong_sell_moving_averages.png", scale=5)
                bot.send_photo(name_channel, photo=open('image/strong_sell_moving_averages.png', 'rb'))

                link = f"https://www.binance.com/ru/futures/{coin}"
                markup = types.InlineKeyboardMarkup()
                link_button = types.InlineKeyboardButton(text='Посмотреть на Binance', url=link)
                markup.add(link_button)
                bot.send_message(name_channel, f'''
🍒Есть сигнал на STRONG SELL\n
🧠Стратегия на: moving_averages\n
🥇Название монеты: {coin}\n
📈Актуальная цена: {dataset.tail(1)['Close'].value_counts().index[-1]}\n
👇Минимальная цена за последние 2 дня: {dataset["Close"].min()} ({dataset.loc[dataset["Close"].idxmin(), "Datetime"]})\n
👆Максимальная цена за последние 2 дня: {dataset["Close"].max()} ({dataset.loc[dataset["Close"].idxmax(), "Datetime"]})\n
💰Средняя цена за последние 2 дня: {dataset["Close"].mean()}\n
                ''', reply_markup=markup)

                os.remove("image/strong_sell_moving_averages.png")
                sleep(1800)

        # запускаем асинхронно 2 фукнции
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(strong_buy)
            future2 = executor.submit(strong_sell)


    def oscillators():
        for coin in all_coins:
            tesla = TA_Handler(
                symbol=coin,
                exchange="BINANCE",
                screener="CRYPTO",
                interval=Interval.INTERVAL_4_HOURS, 
            )

        # Устанавливаем стратегию основанную на oscillators
        rec = tesla.get_analysis().oscillators

        def strong_buy():
            if rec['RECOMMENDATION'] == 'STRONG_BUY':
                today = dt.datetime.now()
                one_month_ago = today - dt.timedelta(days=2)
                dataset = pd_datas(coin, '5m', one_month_ago, today)
                dataset['Datetime'] = dataset['Datetime'].map(lambda x: dt.datetime.fromtimestamp(x / 1000.0))
                dataset['new'] = dataset['Datetime']

                fig = go.Figure([go.Scatter(x=dataset['Datetime'], y=dataset['Close'])])
                fig.update_layout(title=f"Монета: {coin}  Время: {dt.datetime.now()}")
                fig.write_image("image/strong_buy_oscillators.png", scale=5)
                bot.send_photo(name_channel, photo=open('image/strong_buy_oscillators.png', 'rb'))

                link = f"https://www.binance.com/ru/futures/{coin}"
                markup = types.InlineKeyboardMarkup()
                link_button = types.InlineKeyboardButton(text='Посмотреть на Binance', url=link)
                markup.add(link_button)
                bot.send_message(name_channel, f'''
💣Есть сигнал на STRONG BUY\n
🧠Стратегия на: oscillators\n
🥇Название монеты: {coin}\n
📈Актуальная цена: {dataset.tail(1)['Close'].value_counts().index[-1]}\n
👇Минимальная цена за последние 2 дня: {dataset["Close"].min()} ({dataset.loc[dataset["Close"].idxmin(), "Datetime"]})\n
👆Максимальная цена за последние 2 дня: {dataset["Close"].max()} ({dataset.loc[dataset["Close"].idxmax(), "Datetime"]})\n
💰Средняя цена за последние 2 дня: {dataset["Close"].mean()}
            ''', reply_markup=markup)
            os.remove("image/strong_buy_oscillators.png")
            sleep(1800)

        def strong_sell():
            if rec['RECOMMENDATION'] == 'STRONG_SELL':
                today = dt.datetime.now()
                one_month_ago = today - dt.timedelta(days=2)
                dataset = pd_datas(coin, '5m', one_month_ago, today)
                dataset['Datetime'] = dataset['Datetime'].map(lambda x: dt.datetime.fromtimestamp(x / 1000.0))
                dataset['new'] = dataset['Datetime']

                fig = go.Figure([go.Scatter(x=dataset['Datetime'], y=dataset['Close'])])
                fig.update_layout(title=f"Монета: {coin}  Время: {dt.datetime.now()}")
                fig.write_image("image/strong_sell_oscillators.png", scale=5)
                bot.send_photo(name_channel, photo=open('image/strong_sell_oscillators.png', 'rb'))

                link = f"https://www.binance.com/ru/futures/{coin}"
                markup = types.InlineKeyboardMarkup()
                link_button = types.InlineKeyboardButton(text='Посмотреть на Binance', url=link)
                markup.add(link_button)
                bot.send_message(name_channel, f'''
🍒Есть сигнал на STRONG SELL\n
🧠Стратегия на: oscillators\n
🥇Название монеты: {coin}\n
📈Актуальная цена: {dataset.tail(1)['Close'].value_counts().index[-1]}\n
👇Минимальная цена за последние 2 дня: {dataset["Close"].min()} ({dataset.loc[dataset["Close"].idxmin(), "Datetime"]})\n
👆Максимальная цена за последние 2 дня: {dataset["Close"].max()} ({dataset.loc[dataset["Close"].idxmax(), "Datetime"]})\n
💰Средняя цена за последние 2 дня: {dataset["Close"].mean()}\n
            ''', reply_markup=markup)

                os.remove("image/strong_sell_oscillators.png")
                sleep(1800)

        # запускаем асинхронно 2 фукнции
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future3 = executor.submit(strong_buy)
            future4 = executor.submit(strong_sell)
    
    #Запуск асинхронно 2 функций на moving_averages и oscillators
    with concurrent.futures.ThreadPoolExecutor() as executor:
            future5 = executor.submit(moving_averages)
            future6 = executor.submit(oscillators)

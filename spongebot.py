#!/usr/bin/python3

import requests
import re
import functools
from telegram import Bot
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from datetime import datetime, timedelta
from number_parser.phone import format_number


DAT_FILE_PATH = "clients-list.dat"


def trycatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(f"Error in {func.__name__}")
            print(ex)
    return wrapper


class BaseBot():
    def __init__(self):
        self.token = open("spongebot.token", "r").read().splitlines()[0]
        self.listeners = open(DAT_FILE_PATH, "r").read().splitlines()
        self.telegram_client = Bot(self.token)
        self.updater = Updater(self.token, use_context=True)
        self._notify_clients()
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler('echo', self._echo))
        self.dp.add_handler(CommandHandler('subscribe', self._subscribe))
        self.dp.add_handler(CommandHandler('unsubscribe', self._unsubscribe))

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def _notify_clients(self):
        print(self.listeners)
        for client_id in self.listeners:
            if len(client_id) > 0:
                self.telegram_client.send_message(chat_id=client_id, text="I'm back online!")

    def _store_clients(self):
        print("Savind data..")
        with open(DAT_FILE_PATH, mode='w') as datfile:
            datfile.write('\n'.join(self.listeners))

    def _echo(self, bot, context):
        print("Got echo, replying...")
        bot.message.reply_text("Sup")

    @trycatch
    def _subscribe(self, bot, context):
        client = str(bot.message.chat.id)
        print(client)
        print(self.listeners)
        if not client in self.listeners:
            self.listeners.append(client)
            self._store_clients()
            print(f"{client}, welcome!")

    def _unsubscribe(self, bot, context):
        client = str(bot.message.chat.id)
        print(client)
        if client in clients:
            clients.reomve(client)
            self._store_clients()


class WhatsappBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.dp.add_handler(CommandHandler('wa', self._whatsapp_link))

    def _whatsapp_link(self, bot, context):
        print(bot.message.text)
        parsed_number = format_number(bot.message.text)
        bot.message.reply_text("http://wa.me/" + parsed_number)


# YOUR_TOKEN = open("spongebot.token", "r").read().splitlines()[0]
# clients = open(DAT_FILE_PATH, "r").read().splitlines()


def main():
    # client = Bot(YOUR_TOKEN)
    # updater = Updater(YOUR_TOKEN, use_context=True)
    # print(clients)
    # for client_id in clients:
    #     if len(client_id) > 0:
    #         client.send_message(chat_id=client_id, text="I'm back online!")
    # dp = updater.dispatcher
    # dp.add_handler(CommandHandler('echo', echo))
    # dp.add_handler(CommandHandler('subscribe', subscribe))
    # dp.add_handler(CommandHandler('wa', whatsapp_link))
    # dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    # updater.start_polling()
    # updater.idle()
    myBot = WhatsappBot()
    myBot.start()

if __name__ == '__main__':
    main()

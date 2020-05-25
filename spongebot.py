#!/usr/bin/python3

import requests
import re
import functools
from telegram import Bot
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from datetime import datetime, timedelta
from number_parser.phone import format_number


def store_clients():
    print("Savind data..")
    with open(DAT_FILE_PATH, mode='w') as datfile:
        datfile.write('\n'.join(clients))


def echo(bot, context):
    print("Got echo, replying...")
    bot.message.reply_text("Sup")


def trycatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(f"Error in {func.__name__}")
            print(ex)
    return wrapper


@trycatch
def subscribe(bot, context):
    client = str(bot.message.chat.id)
    print(client)
    print(clients)
    if not client in clients:
        clients.append(client)
        store_clients()
        print(f"{client}, welcome!")
        schedule(context, int(client))


def unsubscribe(bot, context):
    client = str(bot.message.chat.id)
    print(client)
    if client in clients:
        clients.reomve(client)
        store_clients()
    

def whatsapp_link(bot, context):
    print(bot.message.text)
    parsed_number = format_number(bot.message.text)
    bot.message.reply_text("http://wa.me/" + parsed_number)


DAT_FILE_PATH = "clients-list.dat"
YOUR_TOKEN = open("spongebot.token", "r").read().splitlines()[0]
clients = open(DAT_FILE_PATH, "r").read().splitlines()


def main():
    client = Bot(YOUR_TOKEN)
    updater = Updater(YOUR_TOKEN, use_context=True)
    print(clients)
    for client_id in clients:
        if len(client_id) > 0:
            client.send_message(chat_id=client_id, text="I'm back online!")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('echo', echo))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('wa', whatsapp_link))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

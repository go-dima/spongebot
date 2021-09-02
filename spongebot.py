#!/usr/bin/python3

from telegram.ext import MessageHandler, Filters
from number_parser.phone import format_number
from base_bot.base_bot import BaseBot


class WhatsappBot(BaseBot):
    def __init__(self, clients_file: str):
        super().__init__("spongebot", clients_file)
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self._whatsapp_link))

    @staticmethod
    def _whatsapp_link(bot, context):
        print(bot.message.text)
        parsed_number = format_number(bot.message.text)
        bot.message.reply_text("http://wa.me/" + parsed_number)


def main():
    bot = WhatsappBot("clients-list.dat")
    bot.start()

if __name__ == '__main__':
    main()

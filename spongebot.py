#!/usr/bin/python3

from number_parser.phone import format_number
from base_bot.base_bot import BaseBot
from telegram.ext import CommandHandler


class WhatsappBot(BaseBot):
    def __init__(self, clients_file: str):
        super().__init__("spongebot", clients_file)
        self.dp.add_handler(CommandHandler('wa', self._whatsapp_link))

    def _whatsapp_link(self, bot, context):
        print(bot.message.text)
        parsed_number = format_number(bot.message.text)
        bot.message.reply_text("http://wa.me/" + parsed_number)


def main():
    myBot = WhatsappBot("clients-list.dat")
    myBot.start()

if __name__ == '__main__':
    main()

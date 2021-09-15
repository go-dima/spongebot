#!/usr/bin/python3

from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import MessageHandler, Filters, InlineQueryHandler

from base_bot.base_bot import BaseBot
from number_parser.phone import format_number


class WhatsappBot(BaseBot):
    def __init__(self, clients_file: str):
        super().__init__("spongebot", clients_file)
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self._reply_message))
        self.dp.add_handler(InlineQueryHandler(self._reply_inline))

    @staticmethod
    def _whatsapp_link(number_to_parse):
        parsed_number = format_number(number_to_parse)
        return f"http://wa.me/{parsed_number}"

    def _reply_message(self, bot, context):
        print("message", bot.message.text)
        bot.message.reply_text(self._whatsapp_link(bot.message.text))

    def _reply_inline(self, bot, context):
        query = bot.inline_query.query
        print("query", query)
        if len(query) < 10:
            return

        reply = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Whatsapp Link",
                input_message_content=InputTextMessageContent(self._whatsapp_link(query)),
            )
        ]
        bot.inline_query.answer(reply)


def main():
    bot = WhatsappBot("clients-list.dat")
    bot.start()


if __name__ == '__main__':
    main()

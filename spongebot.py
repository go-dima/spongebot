#!/usr/bin/python3

import functools
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import MessageHandler, Filters, InlineQueryHandler

from base_bot.base_bot import BaseBot
from number_parser.phone import format_number
from utils.utils import setup_logger


logger = logging.getLogger(__name__)
setup_logger(logger)

_version_ = "0.1.0"


def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


class WhatsappBot(BaseBot):
    def __init__(self, clients_file: str):
        super().__init__("spongebot", clients_file)
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self._reply_message))
        self.dp.add_handler(InlineQueryHandler(self._reply_inline))

    @staticmethod
    def _whatsapp_link(number_to_parse):
        parsed_number = format_number(number_to_parse)
        return f"http://wa.me/{parsed_number}"

    @log_call
    def _reply_message(self, update, context):
        logger.info(f"message is {update.message.text}")
        update.message.reply_text(self._whatsapp_link(update.message.text))

    @log_call
    def _reply_inline(self, update, context):
        query = update.inline_query.query
        logger.info(f"query is {query}")
        if len(query) < 10:
            return

        reply = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Whatsapp Link",
                input_message_content=InputTextMessageContent(self._whatsapp_link(query)),
            )
        ]
        update.inline_query.answer(reply)

    def version(self):
        return _version_


def main():
    logger.info("Loading spongebot")
    bot = WhatsappBot("clients-list.dat")
    bot.start()


if __name__ == '__main__':
    main()

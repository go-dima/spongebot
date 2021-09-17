import functools
import logging

from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def trycatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(f"Error in {func.__name__}", ex)

    return wrapper


class BaseBot:
    def __init__(self, name: str, clients_file: str):
        self.clients_file = clients_file
        self.token = open(f"{name}.token", "r").read().splitlines()[0]
        self.listeners = open(clients_file, "r").read().splitlines()
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
        logger.info(f"current registered clients: {self.listeners}")
        for client_id in self.listeners:
            if len(client_id) > 0:
                self.telegram_client.send_message(chat_id=client_id, text="I'm back online!")

    def _store_clients(self):
        logger.info("Updating clients list..")
        with open(self.clients_file, mode='w') as clients_file:
            clients_file.write('\n'.join(self.listeners))

    def _echo(self, update, context):
        if context.args:
            update.message.reply_text(f"You said: {''.join(context.args)}")
        else:
            update.message.reply_text("You said nothing")

    @trycatch
    def _subscribe(self, update, context):
        client = str(update.message.chat_id)
        logger.info(f"Subscribing client {client}")
        if client in self.listeners:
            logger.info(f"Client {client} is already subscribed")
            update.message.reply_text("You are already subscribed.")
        else:
            self.listeners.append(client)
            self._store_clients()
            logger.info(f"Client {client} has been successfully subscribed")
            update.message.reply_text("You have been subscribed!")

    def _unsubscribe(self, update, context):
        client = str(update.message.chat_id)
        logger.info(f"Unsubscribing client {client}")
        if client in self.listeners:
            self.listeners.remove(client)
            self._store_clients()
            logger.info(f"Client {client} has been successfully unsubscribed")
            update.message.reply_text("You have been unsubscribed!")
        else:
            logger.info(f"Client {client} is not subscribed")
            update.message.reply_text("You are not subscribed.")

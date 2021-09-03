import functools
from telegram import Bot
from telegram.ext import Updater, CommandHandler


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
        print(self.listeners)
        for client_id in self.listeners:
            if len(client_id) > 0:
                self.telegram_client.send_message(chat_id=client_id, text="I'm back online!")

    def _store_clients(self):
        print("Savind data..")
        with open(self.clients_file, mode='w') as datfile:
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
        if client in self.listeners:
            clients.reomve(client)
            self._store_clients()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from helpers import telegram_bot as telegram
import json


# config contains telegram bot token and url from where data is obtained
with open("config.json", "r") as f:
    config = json.load(f)

if __name__ == '__main__':
    TOKEN = config["token"]

    # create the updater, that will automatically create also a dispatcher and a queue to
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", telegram.start))
    dispatcher.add_handler(CommandHandler("help", telegram.help))
    dispatcher.add_handler(CommandHandler("stand", telegram.get_stand))
    dispatcher.add_handler(CommandHandler("commands", telegram.get_commands))
    dispatcher.add_handler(CommandHandler("inzidenz", telegram.inzidenz, pass_args=True))
    dispatcher.add_handler(CommandHandler("love", telegram.love))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, telegram.text))
#     updater.dispatcher.add_handler(CallbackQueryHandler(telegram.data_gen))

    # add error handling
    dispatcher.add_error_handler(telegram.error)

    # start bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()

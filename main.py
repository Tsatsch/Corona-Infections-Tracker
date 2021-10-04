from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from helpers import telegram_bot as telegram
import json


# config contains telegram bot token and url from where data is obtained
with open("config.json", "r") as f:
    config = json.load(f)

def main() -> None:
    """Run the bot."""
    TOKEN = config["token"]
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('incidence', telegram.incidence)],
        states={
            telegram.CHOICE1: [MessageHandler(Filters.regex('^(States|Districts)$'), telegram.choise_state_or_district)],
            telegram.CHOICE2: [MessageHandler(Filters.regex(' /^(?!my).*/'), telegram.choise_particular)],
        },
        fallbacks=[CommandHandler('cancel', telegram.cancel)],
    )

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CommandHandler("help", telegram.help))
    dispatcher.add_handler(CommandHandler("commands", telegram.get_commands))
    dispatcher.add_handler(CommandHandler("love", telegram.love))
    dispatcher.add_handler(CommandHandler("start", telegram.start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, telegram.text))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

import json
import logging

from emoji import emojize
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineQueryResultDocument
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
import helpers.extractor as ex
from telegram.ext.dispatcher import run_async

data = None

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOICE1, CHOICE2 = range(2)

with open("config.json", "r") as f:
    config = json.load(f)

@run_async
def incidence(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['States', 'Districts']]
    update.message.reply_text(
        'Hi! I have an up-to-date info about corona incidence. '
        'Send /cancel to stop talking to me.\n\n'
        'Do you wnat to know the incidence of particular district or state of Germany?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='State or District?'
        ),
    )
    return CHOICE1


def choise_state_or_district(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Choise1 of %s: %s", user.first_name, update.message.text)
    global save_choise1, data
    save_choise1 = update.message.text
    if update.message.text == 'States':
        data = ex.extract_data_states()
    elif update.message.text == 'Districts':
        data = ex.extract_data_districts()
    else:
        data = None
    all_keys = data.keys()
    if len(all_keys) < 20:
        as_string = ", "
        as_string = as_string.join(all_keys)
    else:
        as_string = 'München, Hamburg, Berlin Mitte, Köln, Frankfurt am Main usw. \nAlle ansehen: bit.ly/districts-de '
    # update.message.reply_text(
    #     f'Oki-doki, please write a certain {update.message.text[:-1].lower()}. '
    #     f'Here is a list of all {update.message.text[:-1].lower()}: \n\n'
    #     f'{as_string}'
    # )
    return CHOICE2


def choise_particular(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Choise2 of %s: %s", user.first_name, update.message.text)
    global data
    result = ex.retrieve_from_data(update.message.text, data)
    incindence = ""
    if not "Uf... I could not find the location." in result:
        incindence = ex.get_incidence_diff(update.message.text, data)
    update.message.reply_text(result + "\n" + incindence)
    # let user write again
    if "Uf... I could not find the location." in result:
        return CHOICE2
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Abort the mission!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def love(update, context):
    user = update.message.from_user
    print(user)
    if user['username'] == "ianamak":
        love_emoji = emojize(":heart:", use_aliases=True)
        update.message.reply_text(f'Love you {love_emoji}')


def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'Sorry, but for now the bot is too silly for a conversation, he can only run commands')


# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text(f'Something went wrong, check whether you have typos')


def help(update, content):
    update.message.reply_text("Heyho, have a look at our available commands: \n")
    get_commands(update, content)


def get_commands(update, content):
    answer = 'List of available commands: \n'
    answer += "/commands - list all available commands\n"
    answer += "/incidence - get incidence of state or district\n"
    answer += "/help\n"
    update.message.reply_text(answer)


def start(update, content):
    help(update, content)

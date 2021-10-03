import json
from pathlib import Path
from helpers import data_parser
from emoji import emojize
from helpers import extractor

with open("config.json", "r") as f:
    config = json.load(f)


def start(update, content):
    update.message.reply_text("Welcome, have a look at our available commands: \n")
    commands(update, content)


def help(update, content):
    update.message.reply_text("Heyho, have a look at our available commands: \n")
    commands(update, content)


def commands(update, content):
    answer = 'List of available commands: \n'
    answer += "/stand - Info wie aktuell die Datan sind\n"
    answer += "/commands - List all available commands\n"
    answer += "/inzidenz <Bundesland1> <Bundesland2>...  or \"all\" - inzidenz von ausgezählten Bundesländer anzeigen\n"
    answer += "/help\n"
    answer += "/start"
    update.message.reply_text(answer)


def stand(update, content):
    rki_report = Path("resources/rki_report.xlsx")
    if not rki_report.is_file():
        extractor.download_rki(config['url_rki'])
    data = extractor.extract_data_from_rki(['stand'])
    update.message.reply_text(data['stand'])


def inzidenz(update, content):
    user_input = content.args
    if len(user_input) == 0:
        update.message.reply_text("Oops, please enter a Bundesland like this: /inzidenz <Bundesland1>")
    else:
        rki_report = Path("resources/rki_report.xlsx")
        if not rki_report.is_file():
            extractor.download_rki(config['url_rki'])

        if len(user_input) == 1 and user_input[0] == "all":
            user_input = [blnd.replace("\n","") for blnd in open("resources/bundeslander.txt")]

        data = extractor.extract_data_from_rki(user_input)
        message = ""
        for key, value in data.items():
            message += f"\n{key} - {value[0]}\n"
            if value[1] > 0:
                tendenz = emojize(":arrow_upper_right:", use_aliases=True) + str(value[1])
            else:
                tendenz = emojize(":arrow_lower_left:", use_aliases=True) + str(value[1])
            message += tendenz + "\n"
        update.message.reply_text(message)


def love(update, context):
    love_emoji = emojize(":heart:", use_aliases=True)
    update.message.reply_text(f'Love you {love_emoji}')


# function to handle normal text
def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'did you said "{text_received}" ?')


# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text(f'Something went wrong, check whether you have typos')

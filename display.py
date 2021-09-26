import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import json
from lxml import etree

# config contains telegram bot token and url from where data is obtained
with open("config.json", "r") as f:
    config = json.load(f)


def get_inzidenz():
    link = config["url_muc"]
    html = requests.get(link)
    soup = BeautifulSoup(html.text, features="html.parser")
    inzidenz = str(soup.find_all("script"))

    all_scripts = inzidenz.split("</script>,")

    infographik = ""
    for script in all_scripts:
        if "window.infographicData" in script:
            infographik = script

    infographik = infographik.replace("null", "None")[:-1]
    infographik = infographik.replace("true", "True")
    infographik = infographik.replace("false", "False")
    infographik = eval(infographik.split("<script>window.infographicData=")[1])  # convert str to dict

    base_data = infographik["elements"]["content"]["content"]["entities"]
    data = base_data["528220a8-2300-4e38-87d8-654779ac6556"]["props"]["contentHTML"]
    inzidenz_muc = data.split("data-text=\"True\">")[1].split("</span>")[0]

    url = config["url_rki"]
    html = requests.get(url)
    soup = BeautifulSoup(html.text, features="html.parser")

    dom = etree.HTML(str(soup))
    stand = dom.xpath('//*[@id="main"]/div[1]/p[1]')[0].text[:-1].split(",")[0] + " ("
    stand += dom.xpath('//*[@id="main"]/div[1]/p[1]/text()[2]')[0][1:-1] + ")"

    table = dom.xpath('//*[@id="main"]/div[1]/table')
    table = str(etree.tostring(table[0]))
    table_data = [[cell.text for cell in row("td")]
                  for row in BeautifulSoup(table, features="lxml")("tr")]

    bavaria_data = None
    for arr in table_data:
        if "Bayern" in arr:
            bavaria_data = arr

    inzidenz_rki_arr = [stand, bavaria_data[4]]
    return inzidenz_muc, inzidenz_rki_arr


def notify(update, content):
    inzidenz_muc, inzidenz_rki_arr = get_inzidenz()
    message = "Inzidenz in MUC: \n\n " \
              "Laut Infogram: %s \n See more: %s \n\n" \
              "Laut RKI: %s nach %s \n See more: %s " % (
                  inzidenz_muc, config["url_muc"], inzidenz_rki_arr[1], inzidenz_rki_arr[0],
                  config["url_rki"])
    update.message.reply_text(message)


# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('an error occured')


# function to handle normal text
def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'did you said "{text_received}" ?')


def main():
    TOKEN = config["token"]

    # create the updater, that will automatically create also a dispatcher and a queue to
    updater = Updater(TOKEN, use_context=True)
    bot = telegram.Bot(token=TOKEN)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands

    dispatcher.add_handler(CommandHandler("inzidenz", notify))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()

    # # once a day execute command:
    # while True:
    #     inzidenz = get_inzidenz()
    #     today = date.today()
    #     formatted_date = today.strftime("%d %B %Y")
    #     text = "(%s) Inzidenz in MUC: %s" % (formatted_date, inzidenz)
    #     now = datetime.now()
    #     today8am = now.replace(hour=17, minute=20, second=0, microsecond=0)
    #     if now == today8am:
    #         bot.sendMessage(chat_id=-<ID>, text=text)


if __name__ == '__main__':
    main()

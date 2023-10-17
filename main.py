import json
import typing
import random
import requests
import constants
import logging
import os
import dotenv
from datetime import datetime
from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          filters, ContextTypes, ConversationHandler)

dotenv.load_dotenv()
TOKEN: typing.Final = os.getenv("TOKEN")

print(TOKEN)


# set up logging for bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.bot.username)
    user = update.effective_user
    await update.message.reply_html(constants.startHtml.format(
        username=user.mention_html(),
        botname=context.bot.username))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(constants.helpHtml)


async def dateDiff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # user = update.message.from_user
    # user.get("username")

    await update.message.reply_html(constants.diffHtml.format(user=user))

    return 1


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        userDates = update.message.text.split(" ")

        if len(userDates) == 1:

            userDateParsed = datetime.strptime(userDates[0], "%d/%m/%Y")
            todayDate = datetime.now()

            dayDiff = abs(todayDate - userDateParsed).days

            await update.message.reply_html(constants.singleDateDiff.format(
                dayDiff=dayDiff
                ))

        elif len(userDates) == 2:
            firstUserDateParsed = datetime.strptime(userDates[0], "%d/%m/%Y")
            secondUserDateParsed = datetime.strptime(userDates[1], "%d/%m/%Y")

            dayDiff = abs(firstUserDateParsed - secondUserDateParsed).days

            await update.message.reply_html(constants.dualDateDiff.format(
                dateOne=userDates[0],
                dateTwo=userDates[1],
                dayDiff=dayDiff))

        else:
            await update.message.reply_markdown(constants.errorDateDiffNumArgs)

    except ValueError:
        await update.message.reply_markdown(constants.errorDateDiffValueError)

    return ConversationHandler.END


def cancel():
    pass


# TODO just for testing, remove this eventually
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


async def onThisDay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    baseUrl = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/"
    msgData = update.message.text.split(" ")

    # check if user has provided date
    if (len(msgData) > 1):
        requestDate = msgData[1]
    else:
        requestDate = datetime.strftime(datetime.now(), "%m/%d")

    response = requests.get(baseUrl + requestDate)
    data = json.loads(response.text)

    selectedIndex = random.randint(0, len(data['selected']))
    photoCaption = "{date}/{year}\n\n".format(
        date=requestDate,
        year=data['selected'][selectedIndex]['year']
        )
    photoCaption += data['selected'][selectedIndex]['text']

    print(len(data['selected']))

    await update.message.reply_photo(
        photo=data['selected'][selectedIndex].get('pages')[0]
        .get('thumbnail').get('source'),
        caption=photoCaption
        )

    # await update.message.reply_html(
    #     constants.onDayResponse.format(
    #         textContent=data['selected'][selectedIndex]['text'],
    #         imgSrc=data['selected'][selectedIndex].get('pages')[0]
    #         .get('thumbnail').get('source')
    #         )
    #     )


def main() -> None:
    # build the bot
    app = Application.builder().token(TOKEN).build()

    # handle commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('onday', onThisDay))

    # handler for date difference
    app.add_handler(ConversationHandler(
            entry_points=[CommandHandler("diff", dateDiff)],
            states={
                1: [MessageHandler(filters.TEXT, get_date)],
            },
            fallbacks=[CommandHandler("cancel", cancel)]
            ))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

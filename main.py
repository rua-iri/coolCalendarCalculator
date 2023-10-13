import typing
import logging
import os
import dotenv
from datetime import datetime
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

dotenv.load_dotenv()
TOKEN: typing.Final = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

print(TOKEN)
print(BOT_USERNAME)


# set up logging for bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
rf"""
Hello, {user.mention_html()}
I'm {BOT_USERNAME}
I can do some fun stuff

Type /help to find out more!
""")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
r"""
Here are the functions I'm currently capable of performing:

/help - The command you've just run

/diff - Get the difference between two dates
""")



async def dateDiff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # user = update.message.from_user
    # user.get("username")

    await update.message.reply_html(
rf"""
Okay {user},

Get number of days between today and another date

Enter your chosen date (format dd/mm/yyyy)

""")
    
    return 1
    


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userDate = update.message.text

    userDateParsed = datetime.strptime(userDate, "%d/%m/%Y")
    todayDate = datetime.now()

    dayDiff = abs(todayDate - userDateParsed).days

    await update.message.reply_html(
rf"""
There are 
{dayDiff}
days between today and your date
""")

    return ConversationHandler.END




def cancel():
    pass




# TODO just for testing, remove this eventually
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)





def main() -> None:
    # build the bot
    app = Application.builder().token(TOKEN).build()

    # handle commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

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




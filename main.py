import typing
import logging
import os
import dotenv
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

dotenv.load_dotenv()
TOKEN: typing.Final = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

print(TOKEN)
print(BOT_USERNAME)


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

/help

/diff
""")

async def dateDiff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
r"""
Get Difference between two dates
""")




async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('diff', dateDiff))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()




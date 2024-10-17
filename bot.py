import os
import threading
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scrapper import fetchRows
from form import fillForm

# loading env vars
load_dotenv()

# setting up threads
threads_array = []
thread_count = 3

async def sheets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Please enter 2 parameters for this to work")
        return

    await update.message.reply_text(f'Hello {update.effective_user.first_name}, preparing your data...')

    fromCol = context.args[0]
    toCol = context.args[1]
    res = fetchRows(fromCol, toCol)

    await update.message.reply_text(res)

    """
    i know i know threads could have been used better here
    but oh well, here it is. Does the job for now...
    """
    start = 0
    end = thread_count
    for _ in range(thread_count):
        for row in res[start:end]:
            thread = threading.Thread(target=fillForm, args=(row[0], row[1])) 
            threads_array.append(thread)
            thread.start()

        for thread in threads_array:
            thread.join()

        # setting values for start and end
        start += thread_count
        end += thread_count

    for row in res:
        fillForm(row[0], row[1])

    await update.message.reply_text("Data has been fed into the Tally form...")

async def threads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        await update.message.reply_text('Please pass in the number of threads you want')
        return
       
    thread_count = int(context.args[0])
    await update.message.reply_text(f'Thread count has been set to {thread_count}')

# starting application
app = ApplicationBuilder().token(str(os.getenv("TELEGRAM_BOT_TOKEN"))).build()

# command handlers for the telegram bot
app.add_handler(CommandHandler("sheets", sheets))
app.add_handler(CommandHandler("threads", threads))

app.run_polling()


"""
NOTE: 

I just like to add comments for my own readability and debugging,
it's not GPT code :)
"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telebot.credentials import bot_token, bot_user_name, URL
# from pymongo import MongoClient
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = bot_token

def start(update, context):
    keyboard = [
        [InlineKeyboardButton('Zone A', callback_data='A')],
        [InlineKeyboardButton('Zone B', callback_data='B')],
        [InlineKeyboardButton('Zone C', callback_data='C')],
        [InlineKeyboardButton('Zone D', callback_data='D')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose your zone:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Your Selected Zone: {}".format(query.data))


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TOKEN)
    updater.bot.set_webhook("https://krounterbot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main() 

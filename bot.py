from ctypes import sizeof
from html import entities
from nis import match
import time
from apikey import API_KEY
from apikey import frigi_chat_id
from subprocess import call

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(random.randint(1,6))




    message_id = msg['message_id']
    ""from""
    chat_id = msg['from']['id']
    is_bot = msg['from']['is_bot']
    first_name = msg['from']['first_name']
    username = msg['from']['username']
    language_code = msg['from']['language_code']
    ""chat""
    chat_id_2 = msg['chat']['id']
    first_name_2 = msg['chat']['first_name']
    username_2 = msg['chat']['username']
    chat_type = msg['chat']['type']

    message_date = msg['date']
    text = msg['text']

    return("Here's, what informations I received with your message:\n - The message id is " + str(message_id) +
        ".\n - Our chat id is " + str(chat_id) +
        ".\n - You're " + ("a" if is_bot else "no") + " bot"
        ".\n - Your first name is " + first_name + ", your username " + username +
        ".\n - The language code of our chat is: " + language_code +
        ".\n - The chat type is set to: " + chat_type +
        ".\n - The date code for your message is: " + str(message_date) +
        ".\n - The message text is: \"" + text + "\"."        
        )
def greetingGenerator(msg):
    first_name = msg['chat']['first_name']

    options = [
        "Sry but i got no Hi's left over for you.",
        "Hello there " + first_name + "!",
        "There we go again... \nHi stranger!",
        "Howdy! You alright, friend?",
        "Yo! What’s going on, man?",
        "What’s up! Buddy?",
        "Sup?",
        "Wazzup! Dude?",
        "Hello! It’s been a pleasure meeting you.",
        "Hi " + first_name + "!",
        "It's %s o'clock and this is all u got for me? Shame on you %s!" % (time.strftime("%H",time.localtime()), first_name),
    ]

    return options[random.randint(0,len(options) - 1)]

def handle(msg):
    try:
        chat_id = msg['chat']['id']
        command = msg['text']
        if msg['chat']['first_name']:
            first_name = msg['chat']['first_name']
        else:
            first_name = "Stranger"
        if msg['from']['username']:
            username = msg['from']['username']
        else:
            username = "unknown"

        print ("Got command: %s" % (command))
        bot.sendMessage(frigi_chat_id, "Got a chat: %s. From %s (@%s)" % (command, first_name, username))

        if command == '/roll':
            bot.sendMessage(chat_id, random.randint(1,6))
        elif command == '/time':
            bot.sendMessage(chat_id, time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime()))
        elif command == '/hello':
            bot.sendMessage(chat_id, greetingGenerator(msg))
        elif command == '/myinfo':
            bot.sendMessage(chat_id, myInfo(msg))
        elif command == '/update':
            bot.sendMessage(chat_id, "Gimme a second.")
            call("git -C /home/frigi/raspberrypi4 pull", shell=True)
            call("sudo systemctl restart bot", shell=True)
        elif command == '/rebootpi':
            bot.sendMessage(chat_id, "Ok, cya.")
            call("sudo reboot", shell=True)
        elif command == '/impossible':
            bot.sendMessage(chat_id, "Whyyyyyy")
            raise NameError('MyBad')
        elif command[0] == '/':
            bot.sendMessage(chat_id, "You want more functions? Just send your suggestion to @frigiii")
            bot.sendMessage(frigi_chat_id, "Oy look at this: %s (@%s) Just typed %s." % (first_name, username, command))
        else:
            bot.sendMessage(chat_id, "Isn't it nice to have someone, who always writes you back? But maybe it should be someone else than me (I'm only a bot)")
    except BaseException as error:
        bot.sendMessage(frigi_chat_id, "Oops! \"" + format(error) + "\" occurred on %s. From %s (@%s)" % (command, first_name, username))
        print("Oops!", format(error), "occurred.")

"""

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_KEY).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
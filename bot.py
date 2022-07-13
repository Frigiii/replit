from ctypes import sizeof
from html import entities
from nis import match
import time
from turtle import update
from unittest import skip
from apikey import API_KEY
from apikey import frigi_chat_id
import subprocess
from subprocess import call
from subprocess import run
import random

import asyncio
import logging
from typing import NoReturn

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

from telegram import Bot
from telegram.error import Forbidden, NetworkError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    async with Bot(API_KEY) as bot:
        # get the first pending update_id, this is so we can skip over it in case
        # we get a "Forbidden" exception.
        try:
            update_id = (await bot.get_updates())[0].update_id #returns only one element
        except IndexError:
            update_id = None

        logger.info("listening for new messages...")
        await bot.send_message(frigi_chat_id, text="Startup Succesfull!")
        while True:
            try:
                update_id = await echo(bot, update_id)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                update_id += 1
            except BaseException as error:
                try:
                    (await bot.get_updates(offset=update_id + 1, timeout=1))[0].update_id #skip current update id
                except IndexError:
                    None
                except BaseException as error_2:
                    None
                print("Oops! In Main-Function \"", format(error), "\"occurred.")
                await bot.send_message(frigi_chat_id, text="Oops! In Main Function \"" + format(error) + "\" occurred.")

async def echo(bot: Bot, update_id: int) -> int:
    # Request updates after the last update_id
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1
        # your bot can receive updates without messages
        # and not all messages contain text
        if update.message and update.message.text:
            # Reply to the message
            text = update.message.text            
            x = text.split()
            logger.info("Input: %s", x)
            try:
                await bot.sendMessage(frigi_chat_id, text = "Got a chat: \"%s\". From %s (@%s)" % (text, update.effective_user.first_name, update.effective_user.username))
                if text == "/roll":
                    await roll(bot, update)
                elif text == "/update":
                    await updater(bot, update, update.update_id)
                elif text == "/status":
                    await status(bot, update)
                elif text == "/help":
                    await help_command(bot, update)
                elif text == "/time":
                    await teletime(bot, update)
                elif text == "/hello":
                    await hello(bot, update)    
                elif text == "/myinfo":
                    await myinfo(bot, update)
                elif text == "/impossible":
                    await impossible(bot, update)
                elif text == "/rebootpi":
                    await rebootpi(bot, update, update.update_id)
                elif text[0] == '/':
                    await update.message.reply_text("You want more functions? Just send your suggestion to @frigiii")
                    await bot.send_message(frigi_chat_id, text = "Oy look at this: %s (@%s) Just typed %s." % (update.effective_user.first_name, update.effective_user.username, text))
                else:
                    logger.info("A lonely message occured: %s!", update.message.text)
                    await update.message.reply_text("Isn't it nice to have someone, who always writes you back? But maybe it should be someone else than me (I'm only a bot)")
            except BaseException as error:
                print("Oops! In Echo-Function \"", format(error), "\" occurred.")
                await bot.send_message(frigi_chat_id, text="Oops! In Echo Function \"" + format(error) + "\" occurred.")
        return next_update_id
    return update_id


async def roll(bot: Bot, update: update) -> None:
    await update.message.reply_text(random.randint(1,6))

async def help_command(bot: Bot, update: update) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help mee!")

async def teletime(bot: Bot, update: update) -> None:
    await update.message.reply_text(time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime()))

async def hello(bot: Bot, update: update) -> None:
    first_name = update.effective_user.first_name

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
        "What do u do, fellow kids?",
        "Hi " + first_name + "!",
        "It's %s o'clock and this is all u got for me? Shame on you %s!" % (time.strftime("%H",time.localtime()), first_name),
    ]
    await update.message.reply_text(options[random.randint(0,len(options)-1)])

async def myinfo(bot: Bot, update: update) -> None:
    await update.message.reply_text(random.randint(1,6))

async def updater(bot: Bot, update: update, update_id) -> None:
    if(update.effective_user.username) == "Frigiii":
        await update.message.reply_text("Gimme a second.")
        try:
            (await bot.get_updates(offset=update_id + 1, timeout=1))[0].update_id #skip current update id
        except IndexError:
            None
        subprocess.call('git -C /home/frigi/raspberrypi4 pull https://frigiii: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@github.com/frigiii/raspberrypi4.git', shell=True)
        subprocess.call('sudo systemctl restart bot', shell=True)
        await update.message.reply_text("Done.")
    else:
        await update.message.reply_text("Sry, but i can't do this for u ;(")

async def status(bot: Bot, update: update) -> None:
    if(update.effective_user.username) == "Frigiii":
        response = str(subprocess.check_output('sudo systemctl status bot', shell=True))
        response.replace('\n', '\n')
        await update.message.reply_html(format(response))
    else:
        await update.message.reply_text("Sry, got no Infos for you.")

async def rebootpi(bot: Bot, update: update, update_id) -> None:
    if(update.effective_user.username) == "Frigiii":
        await update.message.reply_text("Ok, cya.")
        try:
            (await bot.get_updates(offset=update_id + 1, timeout=1))[0].update_id #skip current update id
        except IndexError:
            None
        subprocess.Popen("sudo reboot", shell=True)
    else:
        await update.message.reply_text("Ha! U thought so, but i won't allow you ;)")

async def impossible(bot: Bot, update: update) -> None:
    #await bot.send_message(chat_id=frigi_chat_id, text="Dis Working?")
    try:
        await update.message.reply_text("Whyyyyyy")
        raise NameError('MyBad')
    except BaseException as error:
        await update.message.reply_text(format(error))
    raise NameError('AlsoMyBad')

"""
async def process_error(update: Update, error, job=None, coroutine = None) -> None:

    return None


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

        elif command[0] == '/':
            bot.sendMessage(chat_id, "You want more functions? Just send your suggestion to @frigiii")
            bot.sendMessage(frigi_chat_id, "Oy look at this: %s (@%s) Just typed %s." % (first_name, username, command))
        else:
            bot.sendMessage(chat_id, "Isn't it nice to have someone, who always writes you back? But maybe it should be someone else than me (I'm only a bot)")
    except BaseException as error:
        bot.sendMessage(frigi_chat_id, "Oops! \"" + format(error) + "\" occurred on %s. From %s (@%s)" % (command, first_name, username))
        print("Oops!", format(error), "occurred.")

"""


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
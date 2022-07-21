from ctypes import sizeof
from html import entities
from nis import match
from ntpath import join
from re import X
import time
from turtle import update
from unittest import skip
from urllib import response
from apikey import API_KEY
from apikey import frigi_channel_id
from apikey import frigi_chat_id
from apikey import GIT_URL
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
        await bot.send_message(frigi_channel_id, text="Startup Succesfull!")
        while True:
            try:
                update_id = await echo(bot, update_id)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                update_id += 1
            except BaseException as error:
                # skips the current message
                update_id += 1
                print("Oops! In Main-Function \"", format(error), "\"occurred.")
                await bot.send_message(frigi_channel_id, text="Oops! In Main Function \"" + format(error) + "\" occurred.")

async def echo(bot: Bot, update_id: int) -> int:
    # Request updates after the last update_id
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1
        # your bot can receive updates without messages
        # and not all messages contain text
        if update.message and update.message.text:
            # Reply to the message
            try:
                text = update.message.text            
                x = text.split()
                text = x[0]
                await bot.sendMessage(frigi_channel_id, text = "Got a chat: \"%s\". From %s (@%s)" % (' '.join(x), update.effective_user.first_name, update.effective_user.username))
                if text == "/roll":
                    await roll(bot, update, 'message')
                elif text == "/update":
                    await updater(bot, update, update.update_id)
                elif text == "/status":
                    await status(bot, update)
                elif text == "/shell":
                    await shell(bot, update, x)
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
                    await bot.send_message(frigi_channel_id, text = "Oy look at this: %s (@%s) Just typed %s." % (update.effective_user.first_name, update.effective_user.username, text))
                else:
                    logger.info("A lonely message occured: %s!", update.message.text)
                    await update.message.reply_text("Isn't it nice to have someone, who always writes you back? But maybe it should be someone else than me (I'm only a bot)")
            except BaseException as error:
                print("Oops! In Echo-Function \"", format(error), "\" occurred.")
                await bot.send_message(frigi_channel_id, text="Oops! In Echo Function \"" + format(error) + "\" occurred.")
        elif update.channel_post and update.channel_post.text:
            try:
                await roll(bot, update, 'channel_post')
            except BaseException as error:
                print("Oops! In Echo-Function \"", format(error), "\" occurred.")
                await bot.send_message(frigi_channel_id, text="Oops! In Echo Function \"" + format(error) + "\" occurred.")
        return next_update_id
    return update_id


async def roll(bot: Bot, update: update, __type__) -> None:
    await update.__type__.reply_text(random.randint(1,6))

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
        subprocess.call('git -C /home/frigi/raspberrypi4 pull ' + GIT_URL, shell=True)
        subprocess.call('sudo systemctl restart bot', shell=True)
        await update.message.reply_text("Done.")
    else:
        await update.message.reply_text("Sry, but i can't do this for u ;(")

async def shell(bot: Bot, update: update, x) -> None:
    cont = True
    for i in x:
        if i in ['restart','stop']:
            cont = False
    if(update.effective_user.username) == "Frigiii" and cont:
        x.pop(0)
        if len(x):
            await update.message.reply_text("There we go:")
            response = str(subprocess.check_output(' '.join(x), shell=True))
            await update.message.reply_text("Got a response:")
            text = list(response)
            i = 0
            while i < len(text):
                if text[i] == '\\' :
                    if text[i+1] == 'n':
                        text[i] = '\n'
                        text.pop(i+1)
                        while(text[i+1] == " "):
                            text.pop(i+1)
                        if(text[i+1] == '\\'):
                            while not (text[i+1] == '\\' and text[i+2]=='n'):
                                text.pop(i+1)
                i += 1
            i = 0
            while i < len(text):
                if text[i] == '\n' and text[i+1] == '\n':
                    text.pop(i)
                i += 1
            response = "".join(text)
            text = []
            max_length = 4096
            while len(response) > max_length:
                text.append(response[0:max_length])
                response = response[max_length:len(response)-1]
            text.append(response)
            for i in text:
                print(i)
                await update.message.reply_text(format(i))
        else:
            await update.message.reply_text("At least tell me what to do!")
    else:
        await update.message.reply_text("Why u even trying?")

async def status(bot: Bot, update: update) -> None:
    if(update.effective_user.username) == "Frigiii":
        response = str(subprocess.check_output('sudo systemctl status bot', shell=True))
        text = list(response)
        i = 0
        while not (text[i] == 'b' and text[i+1] == 'o'):
            text.pop(i)
        while i < len(text):
            if text[i] == '\\' :
                if text[i+1] == 'n':
                    text[i] = '\n'
                    text.pop(i+1)
                    while(text[i+1] == " "):
                        text.pop(i+1)
                    if(text[i+1] == '\\'):
                        while not (text[i+1] == '\\' and text[i+2]=='n'):
                            text.pop(i+1)
            i += 1
        i = 0
        while i < len(text):
            if text[i] == '\n' and text[i+1] == '\n':
                text.pop(i)
            i += 1
        response = "".join(text)
        await update.message.reply_html(response)
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
    #await bot.send_message(chat_id=frigi_channel_id, text="Dis Working?")
    try:
        await update.message.reply_text("Whyyyyyy")
        raise NameError('MyBad')
    except BaseException as error:
        await update.message.reply_text(format(error))
    raise NameError('AlsoMyBad')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
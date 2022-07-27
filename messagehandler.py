import time
from apikey import frigi_channel_id
from apikey import frigi_chat_id
import random
import asyncio
from typing import NoReturn
import telegram


async def roll(update, type) -> None:
    text = random.randint(1,6)
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def help_command(update, type) -> None:
    """Send a message when the command /help is issued."""
    text = "Help mee!"
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def teletime(update, type) -> None:
    text = time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime())
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def hello(update, type) -> None:
    if type == 'channel_post':
        return
    first_name = update[type]['from']['first_name']
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
    text = options[random.randint(0,len(options)-1)]
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def myinfo(update, type) -> None:
    text = time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime())
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def updater(update, type) -> None:
    if update[type]['from']['username'] == "Frigiii":
        text = time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime())
    else:
        text = "Sry, but i can\'t do this for u ;("
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})


functions = {
    '/roll' : roll,
    '/help' : help_command,
    '/time' : teletime,
    '/hello': hello,
    '/myinfo': myinfo,
    '/updater': updater,
}

async def handler(update) -> str:
    type = list(update)[1]

    msg = update[type]['text']   
    x = msg.split()
    msg = x[0]
    if type == 'message':
        text = "Got a chat: \"%s\". From %s (@%s)" % (update[type]['text'], update[type]['from']['first_name'], update[type]['from']['username'])
        await telegram.request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : text})
    if msg in functions:
        await functions[msg](update, type)
    else:
        text = "Isn\'t it nice to have someone, who always writes you back? But maybe it should be someone else than me (I\'m only a bot)"
        await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})
    return None

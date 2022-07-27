from itertools import count
from mimetypes import init
import time
from apikey import frigi_channel_id
from apikey import frigi_chat_id
import random
import asyncio
from typing import NoReturn
import telegram
import math


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

async def integrator(update, type) -> None:

    def simpson(f,a,b) -> float:
        x = a
        f1 = eval(f)
        #print(f1)
        x = b
        f2 = eval(f)
        #print(f2)
        x = (a+b)/2
        f3 = eval(f)
        #print(f3)
        return (f1 + 4*f3 + f2)/6*(b-a)
    

    def adaptint(a,b,edes,f) -> float:
        global counter
        counter += 1
        i1 = simpson(f,a,b)
        m = (a+b)/2
        i2 = simpson(f,a,m) + simpson(f,m,b)
        e = abs(i2-i1)/15
        print("Step: {}, Value: {}, accuracy: {}".format(counter,i2,e))
        if e > edes:
            return adaptint(a,m,edes/2,f) + adaptint(m,b,edes/2,f)
        else:
            return i2

    a = 0
    b = 10
    f = "x"
    e = 1e-6
    s_max = 1e100
    all_values = {
        'f(x)' : f,
        'a': a,
        'b': b,
        'e' : e,
        'smax' : s_max,
    }
    msg = update[type]['text'].split()
    msg.pop(0)
    given = {}
    while len(msg):
        if msg[0] in all_values:
            all_values[msg[0]] = format(msg[2])
            print('found {} = {}'.format(msg[0], all_values[msg[0]]))
        msg.pop(0)
    a = float(all_values['a'])
    b = float(all_values['b'])
    f = all_values['f(x)']
    e = float(all_values['e'])
    s_max = int(all_values['smax'])

    print(a,b,f,e,s_max)

    
    # if not (a and b and f):
    #     text = "Integration not correctly initialized. Please enter in following form: f(x) = your_function, a = starting_val, b = end_val."
    #     await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})
    global counter
    counter = 0
    text = adaptint(a,b,e,f)
    #text = simpson(f,a,b)
    #print(text)
    text = "Got the result : {}".format(text)
    await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})


        


functions = {
    '/roll' : roll,
    '/help' : help_command,
    '/time' : teletime,
    '/hello': hello,
    '/myinfo': myinfo,
    '/updater': updater,
    '/integrate': integrator,
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

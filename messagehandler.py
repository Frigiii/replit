from itertools import count
from mimetypes import init
from sqlite3 import Timestamp
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
    

    def adaptint(a,b,edes,f) -> list:
        global counter
        counter += 1
        i1 = simpson(f,a,b)
        m = (a+b)/2
        i2 = simpson(f,a,m) + simpson(f,m,b)
        e = abs(i2-i1)/15
        #print("Step: {}, Value: {}, relative error: {}%".format(counter,i2, e/edes*100))
        if counter > s_max:
              print("Max_steps reached.")
              return [i2,e]
        if e > edes:
            r1 = adaptint(a,m,edes/2,f)
            r2 = adaptint(m,b,edes/2,f)
            return [r1[0] + r2[0], r1[1] + r2[1]]
        else:
            return [i2,e]

    a = None
    b = None
    f = None
    e = 1e-3
    s_max = int(1e3)
    all_values = {
        'a' : a,
        'f(x)' : f,
        'b' : b,
        'e' : e,
        'smax': s_max,
    }
    msg = update[type]['text'].split()
    msg.pop(0)
    given = {}
    while len(msg):
        if msg[0] in all_values:
            var = msg[0]
            if var == 'a':
                if not msg[2] == '-':
                    a = float(msg[2])
                else:
                    a = float(msg[2]+msg[3])
            elif var == 'b':
                if not msg[2] == '-':
                    b = float(msg[2])
                else:
                    b = float(msg[2]+msg[3])
            elif var == 'f(x)':
                f = str(msg[2])
            elif var == 'e':
                e = float(msg[2])
            elif var == 'smax':
                s_max = int(float(msg[2]))
        msg.pop(0)

    print(a,b,f,e,s_max)
    
    if not (a - b and f):
        text = "Integration not correctly initialized. Please enter in following form: \nf(x) = your_function, a = starting_val, b = end_val. \nAlternative Values:\ne = max_error, smax = max_steps"
        await telegram.request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})
        return
    
    global counter
    counter = 0
    timestamp = time.time()
    text = adaptint(a,b,e,f)
    timestamp = int(round((time.time() - timestamp)*1000000)) 
    text = "Result : {}\nEstimated error : {}\nSteps taken : {}\nTime needed : {}s, {}ms, {}ns".format(text[0], text[1], counter, timestamp // 1000000, (timestamp % 1000000) // 1000, timestamp % 1000)
    if counter > s_max:
         text = "Reached steps-limit!\n" + text
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

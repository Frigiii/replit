import time
from apikey import API_KEY
from apikey import frigi_channel_id
from apikey import frigi_chat_id
import random
import requests
import asyncio
from typing import NoReturn

async def telegram_request(method, param) -> dict:
    url = 'https://api.telegram.org/bot{API_KEY}/{method}'.format(API_KEY = API_KEY, method = method)
#    print('Making request to : {} {}'.format(url, param))

    r = requests.get(url, params=param)
    #print(r.headers['Content-Type'])
    r_dic = r.json() 
    if (len(r_dic['result'])):
    #    print ('Response of request: {}'.format(r_dic['result']))
        return r_dic['result']
    else:
        return None


async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    #async with request() as r:
    try:
        response = await telegram_request('getUpdates', {})
        if(response):
    #        print('Received {} new Updates'.format(len(response)))
            update_id = (await telegram_request('getUpdates', {}))[0]['update_id']
    #        print('Current update-id: {}'.format(update_id))
        else:
    #        print('Got no new Updates')
            update_id = None
    except BaseException as error:
        print('Error occured: {}'.format(error))
        update_id = None
        

    await telegram_request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : 'I\'m alive!'})

    while True:
        try:
            update_id = await echo(update_id)
        except BaseException as error:
            # skips the current message
            text = "Oops! In Main Function \"" + format(error) + "\" occurred."
            print(text)
            await telegram_request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : text})
            update_id += 1
            

async def echo(update_id: int) -> int:
    # Request updates after the last update_id
    #updates = await bot.get_updates(offset=update_id, timeout=10)
    updates = await telegram_request('getUpdates', {'offset' : update_id, 'timeout' : 10})
    if(updates):
        update_id = updates[0]['update_id']        
        for update in updates:
            next_update_id = update['update_id'] + 1
            # your bot can receive updates without messages
            # and not all messages contain text
    #        print('Next update-id: {}'.format(next_update_id))
            type = list(update)[1]
            if update[type]['text']:
                # Reply to the message
                try:
                    msg = update[type]['text']   
                    x = msg.split()
                    msg = x[0]
                    if type == 'message':
                        text = "Got a chat: \"%s\". From %s (@%s)" % (update[type]['text'], update[type]['from']['first_name'], update[type]['from']['username'])
                        await telegram_request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : text})
                    if msg == "/roll":
                        await roll(update, type)
                    elif msg == "/help":
                        await help_command(update, type)
                    elif msg == "/time":
                        await teletime(update, type)
                    elif msg == "/hello":
                        await hello(update, type)
                    elif msg == "/myinfo":
                        await myinfo(update, type)
                    elif msg == "/update":
                        await updater(update, type)
                    else:
                        text = "Isn\'t it nice to have someone, who always writes you back? But maybe it should be someone else than me (I\'m only a bot)"
                        await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})
                except BaseException as error:
                    text = "Oops! In Echo-Function \"{}\" occurred.".format(error)
                    print(text)
                    await telegram_request('sendMessage', {'chat_id' : frigi_channel_id, 'text' : text})
            return next_update_id
    return update_id


async def roll(update, type) -> None:
    text = random.randint(1,6)
    await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def help_command(update, type) -> None:
    """Send a message when the command /help is issued."""
    text = "Help mee!"
    await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def teletime(update, type) -> None:
    text = time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime())
    await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

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
    await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def myinfo(update, type) -> None:
    text = time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime())
    await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})

async def updater(update, type) -> None:
    if update[type]['from']['username'] == "Frigiii":
        text = time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime())
    else:
        text = "Sry, but i can\'t do this for u ;("
    await telegram_request('sendMessage', {'chat_id' : update[type]['chat']['id'], 'text' : text})


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
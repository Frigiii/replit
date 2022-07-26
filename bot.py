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
    print('Making request to : {} {}'.format(url, param))

    r = requests.get(url, params=param)
    #print(r.headers['Content-Type'])
    r_dic = r.json() 
    if (len(r_dic['result'])):
        print ('Response of request: {}'.format(r_dic['result']))
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
            print('Received {} new Updates'.format(len(response)))
            update_id = (await telegram_request('getUpdates', {}))[0]['update_id']
            print('Current update-id: {}'.format(update_id))
        else:
            print('Got no new Updates')
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
            print('Next update-id: {}'.format(next_update_id))
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
    #await eval('update.' + type + '.reply_text(random.randint(1,6))')
    #await update(type).reply_text(random.randint(1,6))
'''
async def help_command(bot: Bot, update: update, type) -> None:
    """Send a message when the command /help is issued."""
    await eval('update.' + type + '.reply_text("Help mee!")')

async def teletime(bot: Bot, update: update, type) -> None:
    await eval('update.' + type + '.reply_text(time.strftime("%a, %d.%m.%y, %H:%M:%S", time.localtime()))')

async def hello(bot: Bot, update: update, type) -> None:
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
    await eval('update.' + type + '.reply_text(options[random.randint(0,len(options)-1)])')

async def myinfo(bot: Bot, update: update, type) -> None:
    await eval('update.' + type + '.reply_text(random.randint(1,6))')

async def updater(bot: Bot, update: update, type, update_id) -> None:
    if(update.effective_user.username) == "Frigiii":
        await eval('update.' + type + '.reply_text("Gimme a second.")')
        try:
            (await bot.get_updates(offset=update_id + 1, timeout=1))[0].update_id #skip current update id
        except IndexError:
            None
        subprocess.call('git -C /home/frigi/raspberrypi4 pull ' + GIT_URL, shell=True)
        subprocess.call('sudo systemctl restart bot', shell=True)
        await eval('update.' + type + '.reply_text("Done.")')
    else:
        await eval('update.' + type + '.reply_text("Sry, but i can\'t do this for u ;(")')

async def shell(bot: Bot, update: update, type, x) -> None:
    cont = True
    for i in x:
        if i in ['restart','stop']:
            cont = False
    if(update.effective_user.username) == "Frigiii" and cont:
        x.pop(0)
        if len(x):
            await eval('update.' + type + '.reply_text("There we go:")')
            response = str(subprocess.check_output(' '.join(x), shell=True))
            await eval('update.' + type + '.reply_text("Got a response:")')
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
                await eval('update.' + type + '.reply_text(format(i))')
        else:
            await eval('update.' + type + '.reply_text("At least tell me what to do!")')
    else:
        await eval('update.' + type + '.reply_text("Why u even trying?")')

async def status(bot: Bot, update: update, type) -> None:
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
        await eval('update.' + type + '.reply_text("Sry, got no Infos for you.")')

async def rebootpi(bot: Bot, update: update, type, update_id) -> None:
    if(update.effective_user.username) == "Frigiii":
        await eval('update.' + type + '.reply_text("Ok, cya.")')
        try:
            (await bot.get_updates(offset=update_id + 1, timeout=1))[0].update_id #skip current update id
        except IndexError:
            None
        subprocess.Popen("sudo reboot", shell=True)
    else:
        await eval('update.' + type + '.reply_text("Ha! U thought so, but i won\'t allow you ;)')

async def impossible(bot: Bot, update: update, type) -> None:
    #await bot.send_message(chat_id=frigi_channel_id, text="Dis Working?")
    try:
        await eval('update.' + type + '.reply_text("Whyyyyyy")')
        raise NameError('MyBad')
    except BaseException as error:
        await eval('update.' + type + '.reply_text(format(error))')
    raise NameError('AlsoMyBad')
'''


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
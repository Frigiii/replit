from ctypes import sizeof
from html import entities
from nis import match
import re
import time
import random
import datetime
from unittest import case
import telepot
from telepot.loop import MessageLoop

"""
After **inserting token** in the source code, run it:
```
$ python2.7 diceyclock.py
```
[Here is a tutorial](http://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/)
teaching you how to setup a bot on Raspberry Pi. This simple bot does nothing
but accepts two commands:
- `/roll` - reply with a random integer between 1 and 6, like rolling a dice.
- `/time` - reply with the current time, like a clock.
"""
def myInfo(msg):
    message_id = msg['message_id']
    """from"""
    chat_id = msg['from']['id']
    is_bot = msg['from']['is_bot']
    first_name = msg['from']['first_name']
    username = msg['from']['username']
    language_code = msg['from']['language_code']
    """chat"""
    chat_id_2 = msg['chat']['id']
    first_name_2 = msg['chat']['first_name']
    username_2 = msg['chat']['username']
    chat_type = msg['chat']['type']

    message_date = msg['date']
    text = msg['text']
    text_offset = msg['entities']['offset']
    text_length = msg['entities']['length']
    text_type = msg['entities']['type']

    return("Here's, what informations I received with your message:\n - The message id is" + message_id +
        "\n - Our chat id is " + chat_id + ", you're " + "a" if is_bot else "no" + " bot."
        )
def greetingGenerator(msg):
    first_name = msg['chat']['first_name']

    options = {
        1 : "Sry but i got no 'Hi' left over for you.",
        2 : "Hello there " + first_name + "!",
        3 : "There we go again... \nHi stranger!"
    }

    return options[random.randint(1,len(options))]

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    first_name = msg['chat']['first_name']

    print ("Got command: %s" % (command))

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/hello':
        bot.sendMessage(chat_id, greetingGenerator(msg))
    elif command == '/myInfo':
        bot.sendMessage(chat_id, myInfo(msg))

bot = telepot.Bot('5457885103:AAGxW8IXcX-VtAKbWQgxh_vKKZu5_-J0UP4')

MessageLoop(bot, handle).run_as_thread()
print ("I am listening ...")

while 1:
    time.sleep(10)

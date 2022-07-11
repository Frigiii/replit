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
from apikey import API_KEY
from apikey import frigi_chat_id
from subprocess import call

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
    ]

    return options[random.randint(0,len(options) - 1)]

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    first_name = msg['chat']['first_name']
    username = msg['from']['username']

    print ("Got command: %s" % (command))
    bot.sendMessage(frigi_chat_id, "Got a chat: %s. From %s (@%s)" % (command, first_name, username))

    try:
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
            bot.sendMessage(chat_id, "hello")
            bot.sendMessage(chat_id, 1/0)
            raise NameError('HiThere')
        elif command[0] == '/':
            bot.sendMessage(chat_id, "You want more functions? Just send your suggestion to @frigiii")
            bot.sendMessage(frigi_chat_id, "Oy look at this: %s (@%s) Just typed %s." % (first_name, username, command))
        else:
            bot.sendMessage(chat_id, "Isn't it nice to have someone, who always writes you back? But maybe it should be someone else than me (I'm only a bot)")
    except BaseException as error:
        bot.sendMessage(frigi_chat_id, format(error))
        bot.sendMessage(frigi_chat_id, "Oops!", format(error), "occurred on %s. From %s (@%s)" % (command, first_name, username))
        print("Oops!", format(error), "occurred.")

bot = telepot.Bot(API_KEY)

MessageLoop(bot, handle).run_as_thread()
print ("I am listening ...")
bot.sendMessage(frigi_chat_id, "Startup finished")

while 1:
    time.sleep(10)
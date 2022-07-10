import time
import random
import datetime
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
        bot.sendMessage('Hello there %s' % (first_name))

bot = telepot.Bot('5457885103:AAGxW8IXcX-VtAKbWQgxh_vKKZu5_-J0UP4')

MessageLoop(bot, handle).run_as_thread()
print ("I am listening ...")

while 1:
    time.sleep(10)

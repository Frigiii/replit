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
import subprocess


p = subprocess.Popen("/home/frigi/raspberrypi4", shell= True)

p.communicate("sudo systemctl stop bot.service")
time.sleep(1)
p.communicate("git pull")
time.sleep(5)
p.communicate("sudo systemctl start bot.service")
p.kill


"""

call("sudo systemctl stop bot.service", shell=True)
time.sleep(1)
call("cd /home/frigi/raspberrypi4", shell=True)
call("git pull", shell = True)
time.sleep(10)
call("sudo systemctl start bot.service", shell=True)
"""
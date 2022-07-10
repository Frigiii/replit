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
from subprocess import call


call("sudo systemctl stop bot.service", shell=True)
time.sleep(1)
call("cd /home/frigi/raspberrypi4", shell=True)
call("git pull", shell = True)
time.sleep(10)
call("sudo systemctl start bot.service", shell=True)

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
from subprocess import call

call("sudo /home/frigi/raspberrypi4/rebootpi.sh", shell=True)


"""
p = subprocess.Popen("cd /home/frigi/raspberrypi4", shell= True)

p.communicate("sudo systemctl stop bot.service")
time.sleep(1)
p.communicate("git pull")
time.sleep(5)
p.communicate("sudo systemctl start bot.service")
p.kill()


Versuch 19:53


call("sudo systemctl stop bot.service", shell=True)
time.sleep(1)
call("cd /home/frigi/raspberrypi4", shell=True)
call("git pull", shell = True)
time.sleep(10)
call("sudo systemctl start bot.service", shell=True)
"""
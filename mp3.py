from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from io import BytesIO

from PIL import Image
import numpy as np
import cv2

import matplotlib.pyplot as plt

from javascript import require, On, off
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
#mineflayerViewer = require('prismarine-viewer').headless
mineflayerViewer = require('prismarine-viewer').mineflayer

# to record POV
firefox_options = Options()
driver = webdriver.Firefox( options = firefox_options)

RANGE_GOAL = 1
BOT_USERNAME = 'python'

plist=[]

def getpov():    
    png=driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png)).convert('RGB')
    return np.asarray(im)
    
bot = mineflayer.createBot({
  'host': '127.0.0.1',
  'username': 'python'
})
# this part must be in the same cell as bot so that it is executed once the bot is generated.

#register an event handler with the @On or @Once decorator. This decorator takes two arguments, 
#first it's the Event Emitter (the object that is sending events) and the second is the event name, 
#what event you want to listen to. Do not use the .on or .once methods on bot, use the decorators instead.
@On(bot, 'login')
def handle(*args):
    mineflayerViewer(bot,{'port':3007,'firstPerson':True})


# main part of the function.  
@On(bot,'spawn')
def handle(*args):
    bot.chat('I spawned!')
    # load pov in the hidden firefox window
    driver.get('http://127.0.0.1:3007')
    # wait until firefox finishes rendering
    sleep(5)
    
    bot.chat(bot.username+': Ready.')
    # start recording

# Need to think about how to use it.    
@On(bot, 'whisper')
def breakListener(this, sender, message, *args):
    if sender and (sender != BOT_USERNAME):
        # receive the signal to start
        if 'Go' in message:
            bot.setControlState('forward', True)
            plist.append(getpov())
            sleep(10)
            plist.append(getpov())
            sleep(5)
            plist.append(getpov())
            bot.setControlState('forward', False)
        
        #1d grayscale arrays
        img1 = np.array(cv2.cvtColor(plist[0], cv2.COLOR_RGB2GRAY)).flatten()
        img2 = np.array(cv2.cvtColor(plist[1], cv2.COLOR_RGB2GRAY)).flatten()
        img3 = np.array(cv2.cvtColor(plist[2], cv2.COLOR_RGB2GRAY)).flatten()
        #ideally, img1 and img2 are the same


        sum1 = np.sum(np.abs(img1 - img2))
        sum2 = np.sum(np.abs(img2 - img3)) #this should be super close to 0
        print(sum1)
        print(sum2)
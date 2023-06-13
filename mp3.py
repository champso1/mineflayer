'''
script for just mineflayer

from javascript import require, On
mineflayer = require('mineflayer')
mineflayerViewer = require('prismarine-viewer').mineflayer

bot = mineflayer.createBot({
  'host': '127.0.0.1', #can be 'localhost' as well
  'username': 'python' #can be whatever you want
})

@On(bot, 'login') #can also be @On(bot, 'spawn') i think, but 'login' works for me so you can probably just leave it like that
def handle(*args):
    mineflayerViewer(bot,{'port':3007,'firstPerson':True}) 

this is really all you need, do the require command for both regular mineflayer to get the bot as well as prismarine-viewer
i guess python will automatically query some online database somewhere to get whatever files/packages or whatever, no need for npm
you gotta also ensure that your server is running, i know thats self explanatory but twice ive spent like 10 mins trying to debug only to find that the server just wasnt running
then you just add an event listener when the bot logs in, and execute mineflayerViewer(), 'firstPerson':False makes it a birds eye view
port can be whatever, just put 'localhost:<port>' or '127.0.0.1:<port>' in browser, im sure you already knew that though, im just covering all the bases
if you are having problems with just this, then maybe its OS related, in which case i can't really help, unfortunately

'''

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

all_frames = []

def getpov():    
    png=driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png)).convert('RGB')
    return np.array(im)

def testImage(img1, img2):
    #convert to grayscale to remove channels, flatten to made 1d
    arr1 = np.array(cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)).flatten()
    arr2 = np.array(cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)).flatten()
    #sum of absolute value of difference of all corresponding points
    sum1 = np.sum(np.abs(arr1 - arr2))
    return True if sum1 == 0 else False #true if images are identical
    
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
            test_frames = []
            i = 0
            for _ in range(100): #change this number to have it record/test for longer
                #every 20 iterations, test two evenly spaced (in time) frames, if they are equal, jump, otherwise, do nothing
                #this entire thing is done weirdly and probably really poorly i think but hey it works
                i += 1
                frame = getpov()
                all_frames.append(frame)
                if i == 10:
                    test_frames.append(frame)
                elif i == 20:
                    test_frames.append(frame)
                    if testImage(test_frames[0], test_frames[1]):
                        bot.setControlState('jump', True)
                        bot.setControlState('jump', False)

                    test_frames.clear()
                    i = 0

            
            #after loop, put everything into a file
            out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mpv4'), 10, (all_frames[0].shape[1], all_frames[0].shape[0]), True) #my computer gathers the frames too slowly, framerate has to be astoundingly low to be at the correct speed
            for frame in all_frames:
                out.write(frame)
            out.release()
            

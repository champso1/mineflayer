#import everything needed
from javascript import require, On
mineflayer = require('mineflayer')
mineflayerViewer = require('prismarine-viewer').mineflayer
pathfinder = require('mineflayer-pathfinder')
#python automatically queries whatever database to get this stuff, no need for npm or anything

#need to create the bot and tell it how to connect
bot = mineflayer.createBot({
    'host': 'localhost', 
    'username': 'Kevin' #can rename this if you want lol
})

#these 4 lines are entirely for pathfinder, it just tells the bot how to move, if it can break blocks, etc., just leave it as is
bot.loadPlugin(pathfinder.pathfinder)
mcData = require('minecraft-data')(bot.version)
movements = pathfinder.Movements(bot, mcData)
RANGE_GOAL = 1

target = None

@On(bot, 'spawn') #can also be @On(bot, 'login'), either works it seems
def func(this, *rest):
    bot.chat('I joined')
    mineflayerViewer(bot, {'port':3007, 'firstPerson': True}) #put 'localhost:<port>' in browser

#give it an event listener when someone chats to do commands
@On(bot, 'chat')
def handleChat(this, sender, message, *args):
    if sender == bot.username: return #ensure it doesn't read its own chat message and screw something up
    if sender and (sender != 'Kevin'): #this is redundant now that i look at it, but its whatever
        match message:
            case 'forward': #if someone chats "forward", we set the bots movement to move forward, we can set it to false later to stop it from moving forward
                bot.chat('moving forward')
                bot.setControlState('forward', True)
            case 'come to me': #this one is a bit complicated, but it basically grabs the position of the person who sent the message, and tells it to get within 1 block of the player's position
                target = bot.players[sender].entity
                if not target:
                    bot.chat('can\'t see you')
                    return
                pos = target.position
                bot.pathfinder.setMovements(movements)
                bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z))
                
                
                
            #can add all sorts of movements
                
'''
to actually send a message in the chat, you go to the minecraft server terminal and type "say forward", for instance.
the say command will chat a message as if you were a player, and you can replace forward with "come to me" or any other message you make in the chat event handler
hope this helps!

'''

import sys
import telnetlib
import time
import random
import asyncio

# Author: a4blue
#This is a python script to make a player automatically explore a random gen world in 7dtd
#Requires Python 3, Allocs Server Fixes and 7dtd


#Function defs

#Removes Negative Buffs from Teleporting player
def removeBuffs(PLAYER,tn):
    cmd = "debuffplayer "+PLAYER+" "
    debuffs = ["internalBleeding","brokenLeg","splint","sprainedLeg","burningSmall","burning","hungry","hungry2","thirsty","thirsty2","freezing","hypo1","hypo2","hypo3","overheated","heat1","heat2","wet","drowning","criticalBleedout","bleeding"]
    for x in debuffs:
        s = cmd+x+"\n"
        tn.write(str.encode(s))
    return
#Teleports Player
def tele(x,y,PLAYER,tn):
    removeBuffs(PLAYER,tn)
    s = "tele "+PLAYER+" "+str(x)+" 0 "+str(y)+"\n"
    print(s)
    tn.write(str.encode(s))
    time.sleep(1)
    return

#Teleports player along the spiral
def spiral(xs,ys,it,step,PLAYER,tn):
    xs = int(xs)
    ys = int(ys)
    it = int(it)*2
    step = int(step)
    x = xs
    y = ys
    for i in range(0,it,2):
        for xt in range(x-step,xs-((i+1)*step),-step):
            x=xt
            tele(x,y,PLAYER,tn)
        for yt in range(y-step,ys-((i+1)*step),-step):
            y=yt
            tele(x,y,PLAYER,tn)
        for xt in range(x+step,xs+((i+1)*step),step):
            x=xt
            tele(x,y,PLAYER,tn)
        for yt in range(y+step,ys+((i+1)*step),step):
            y=yt
            tele(x,y,PLAYER,tn)
    return

#Main Program starts here
#TODO Error handling
#TODO more customization
#TODO define values in a file and load it if available
HOST = input('Telnet Host:')
PORT = input('Telnet Port:')
PASSWORD = input('Telnet Passwort(if set):')
tn =  telnetlib.Telnet(HOST,PORT)
if PASSWORD:
    tn.read_until(b"Please enter password:")
    tn.write(str.encode(PASSWORD+"\n"))
tn.read_until(b"Press 'help' to get a list of all commands. Press 'exit' to end session.",10)
PLAYER = input('Player(must be online):')
MODE = input('Select mode(0=Start spiral at 0,0;1=Random then choose coordinates to start spiral;2=Double spiral at Ccordinates;3=Spral at coordinates):')

if MODE == '0':
    LOCx = 0
    LOCy = 0
    spiral(LOCx,LOCy,100,80,PLAYER,tn)
elif MODE == '1':
    RandNum = input('How many random locations to visit:')
    i = 0
    while i<int(RandNum):
        tele(random.randrange(-5000,5000,1),random.randrange(-5000,5000,1),PLAYER,tn)
        i = i+1
    print("For Coordinates look on the map !")
    LOCx = input('Choose x-Coord:')
    LOCy = input('Choose y-Coord:')
    spiral(LOCx,LOCy,100,80,PLAYER,tn)
elif MODE == '2':
    LOCx = input('Choose x-Coord:')
    LOCy = input('Choose y-Coord:')
    xs = LOCx
    ys = LOCy
    for i in range(0,200,2):
        for xt in range(LOCx-640,xs-((i+1)*640),-640):
            LOCx = xt
            tele(LOCx,LOCy,PLAYER,tn)
            spiral(LOCx,LOCy,4,80,PLAYER,tn)
        for yt in range(LOCy-640,ys-((i+1)*640),-640):
            LOCxy = yt
            tele(LOCx,LOCy,PLAYER,tn)
            spiral(LOCx,LOCy,4,80,PLAYER,tn)
        for xt in range(LOCx+640,xs+((i+1)*640),640):
            LOCx = xt
            tele(LOCx,LOCy,PLAYER,tn)
            spiral(LOCx,LOCy,4,80,PLAYER,tn)
        for yt in range(LOCy+640,ys+((i+1)*640),640):
            LOCy = yt
            tele(LOCx,LOCy,PLAYER,tn)
            spiral(LOCx,LOCy,4,80,PLAYER,tn)
elif MODE =='3':
    LOCx = input('Choose x-Coord:')
    LOCy = input('Choose y-Coord:')
    tele(LOCx,LOCy,PLAYER,tn)
    spiral(LOCx,LOCy,100,80,PLAYER,tn)
tn.write(b"exit\n")
input('Enter for exit')
import pygame, gif_pygame, time as t, os,random as r
from pygame import mixer
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
resolution = [512,512]
temp_res = resolution
mode = [pygame.RESIZABLE]
screen = pygame.display.set_mode(resolution,mode[0])
pygame.display.set_caption("Dungeon")
icon = pygame.image.load('assets\\player\\player_F.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
running = True

levels = ["level", "level1","level2","level3"]
lvlname = 1

volume = [50]
sound = []

all_keys = 0

ENTLIST = []
Low = 0.0167
High = 0.1


CurTime = clock.get_time()
LastTime =  CurTime
file = open("assets\\loadlvl.txt","w")
file.write("1")
file.close()

dttime = 0

def GetTime():
    return CurTime

def GetDTTime():
    return dttime 

def UpdateTime(time):
    global CurTime,LastTime,dttime
    dttime = time 
    CurTime += clock.get_time() / 1000

def SetVolume(vol):
    global volume
    volume + vol

    
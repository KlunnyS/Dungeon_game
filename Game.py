import basedef
import entdef
import Menu
import Menu_pause

from basedef import *
from entdef import *
from Menu import *
from Menu_pause import *

# import math
# import multiprocessing

# TO DO: Make a game pls ty :3
def LoadSave():
    UnloadLevel()
    global lvlname,resolution,all_keys
    pygame.display.set_mode((512,512),pygame.RESIZABLE)
    

    lvlload = "assets\\levelsave.txt"
    boss_found = False
    file = open(lvlload,"r")
    file_found = False
    for i in file:
        if not boss_found:    
            boss,num,keys = i.split()
            if boss == "BOSS":
                all_keys = keys
                lvlname = num
                file2 = open("assets\\loadlvl.txt","w")
                file2.write(str(lvlname))
                file2.close()
                boss_found = True
        if i.strip() == "SAVEFILE" and file_found == False:
            print("file found")
            file_found = True
        elif file_found & True and i != "\n":
            Object_type, Object_path, Object_pos_x, Object_pos_y, Object_width, Object_height, Object_rotation = i.split()

            obj = Object()
            obj.type = Object_type
            obj.img_path = Object_path.strip("\"")
            obj.width = int(Object_width)
            obj.height = int(Object_height)
            obj.pos = [float(Object_pos_x), float(Object_pos_y)]
            obj.rotation = int(Object_rotation)

            obj.GenRect()
            obj.AddToObjList()

    CenterStuff()
    file.close()

def LoadWorld():
    UnloadLevel()
    global lvlname,resolution
    pygame.display.set_mode((512,512),pygame.RESIZABLE)
    
    file = open("assets\\loadlvl.txt")
    lvlname = file.readline()
    file.close()
    

    if os.path.exists("assets"+"\\"+lvlname+".txt"):
        lvlload = "assets"+"\\"+lvlname+".txt"
        file = open(lvlload,"r")
        file_found = False
    else:    
        if int(lvlname) >= len(levels):
            lvlname = len(levels)-1
            t.sleep(2)
        lvlload = "assets"+"\\"+levels[int(lvlname)]+".txt"
        
        file = open(lvlload,"r")
        file_found = False
    

    for i in file:
        if i.strip() == "SAVEFILE" and file_found == False:
            print("file found")
            file_found = True
        elif file_found & True and i != "\n":
            Object_type, Object_path, Object_pos_x, Object_pos_y, Object_width, Object_height, Object_rotation = i.split()

            obj = Object()
            obj.type = Object_type
            obj.img_path = Object_path.strip("\"")
            obj.width = int(Object_width)
            obj.height = int(Object_height)
            obj.pos = [float(Object_pos_x), float(Object_pos_y)]
            obj.rotation = int(Object_rotation)

            obj.GenRect()
            obj.AddToObjList()

    CenterStuff()
    file.close()

def UnloadLevel():
    ENTLIST[0].OBJECTS = []

def LoadSettings():
        global volume
        settings = []
        res = False
        vol = False
        file = open("settings.txt","r")
        for i in file:
            if res == True:
                width,height,mode = i.split()
                resolution = (int(width),int(height))
                if mode == "resize":
                    mode = pygame.RESIZABLE
                elif mode == "full":
                    mode = pygame.FULLSCREEN
                else:
                    mode = pygame.FULLSCREEN
                pygame.display.set_mode(resolution,mode)
                res = False

            if vol:
                volume[0] = int(i.strip())
                # print(vol,volume)
                vol = False

            if i.strip() == "Resolution":
                res = True

            if i.strip() == "VOL":
                vol = True

        sound[0].SetVolume()
        CenterStuff()
        file.close()
  
def StartUp():
    global ENTLIST
    ENTLIST.clear()
    Entity()
    World()
    Player()
    Sounds()


def UpdateThings():
    global running,ENTLIST
    for x in ENTLIST:
        if x.Update():
            running = False
            save()
            ENTLIST[0].OBJECTS.clear()
            pygame.display.set_mode((512,512),pygame.RESIZABLE)
    UpdateText()

def HandleKeys():
    global ENTLIST
    self = ENTLIST[1]

    # if True not in pygame.key.get_pressed(): # -Almix
    #     return

    key = pygame.key.get_pressed()

    posx = 0
    posy = 0

    self.sprint()

    # print("updating position")

    self.moving = True

    if key[pygame.K_w] & True:
        self.image = self.anim_B
        posy += self.speed * GetDTTime() 
        if self.speed == 0.4:
            sound[0].PlayWalking()
        else:
            sound[0].PlayRunning()
        self.last_movedir = "B"

    if key[pygame.K_s] & True:
        self.image = self.anim_F
        posy -= self.speed * GetDTTime() 
        if self.speed == 0.4:
            sound[0].PlayWalking()
        else:
            sound[0].PlayRunning()
        self.last_movedir = "F"

    if key[pygame.K_a] & True:
        self.image = self.anim_L
        posx += self.speed * GetDTTime() 
        if self.speed == 0.4:
            sound[0].PlayWalking()
        else:
            sound[0].PlayRunning()
        self.last_movedir = "L"

    if key[pygame.K_d] & True:
        self.image = self.anim_R
        posx -= self.speed * GetDTTime() 
        if self.speed == 0.4:
            sound[0].PlayWalking()
        else:
            sound[0].PlayRunning()
        self.last_movedir = "R"

    x_blocked = False
    y_blocked = False

    if posx == 0 and posy == 0: # ak sa nehybem vobec
        if self.last_movedir == "B":
            self.image = self.img_B

        if self.last_movedir == "F":
            self.image = self.img_F

        if self.last_movedir == "L":
            self.image = self.img_L

        if self.last_movedir == "R":
            self.image = self.img_R

        self.moving = False
    
    for x in ENTLIST[0].OBJECTS + ENTLIST:
        
        if x == self or x.name == "!WORLD!": 
            continue
        
        if x.ShouldCollide() == False:
            continue

        mypos = pygame.Vector2(self.rect.center)
        opos = pygame.Vector2(x.rect.center)
        

        if (mypos - opos).length() > 512:
            continue

        # print(x.rect)
        
        rect_predict = x.rect.copy()
        rect_predict.x += posx
        if ENTLIST[1].rect.colliderect(rect_predict):
            if x.HandleInteraction(ENTLIST[1]):
                x_blocked = True
                # print(rect_predict.center)
                # print(ENTLIST[1].rect.center) 
            # print(self.name, "Coliding with", x.type, x.name)
            # print(self.rect.center, x.rect.center)
            
        rect_predict.x -= posx
        rect_predict.y += posy
        if ENTLIST[1].rect.colliderect(rect_predict):
            if x.HandleInteraction(ENTLIST[1]):
                y_blocked = True
                # print("idk2")
            # print(self.name, "Coliding with", x.type, x.name)
            # print(self.rect.center, x.rect.center)            

    for x in ENTLIST[0].OBJECTS + ENTLIST:
        if x.name == "!WORLD!" or x.name == "!PLAYER!":
            continue

        if y_blocked == False:
            x.rect.y += round(posy,0) 
        if x_blocked == False:
            x.rect.x += round(posx,0)


time_elapsed_FS = None
time_FS = None
can_FS = None

def screen_size():
    global mode,screen,resolution,temp_res,ENTLIST,time_elapsed_FS,time_FS,can_FS
    key = pygame.key.get_pressed()

    if can_FS == False:
        time_elapsed_FS = t.time() - time_FS
        # print(t.time() - time_FS)

    if time_elapsed_FS == None or time_elapsed_FS >= 1:
        can_FS = True

    if key[pygame.K_F11] and can_FS == True:
        if mode[0] == pygame.RESIZABLE:
            mode[0] = pygame.FULLSCREEN
            screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),mode[0])
            ENTLIST[1].CenterPlayer()
            can_FS = False
            time_FS = t.time()

        elif mode[0] == pygame.FULLSCREEN:
            mode[0] = pygame.RESIZABLE
            screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),mode[0])
            ENTLIST[1].CenterPlayer()
            can_FS = False
            time_FS = t.time()

time_elapsed_show = None
time_show = None
can_show = None

def ShowColl():
    global can_show,time_elapsed_show,time_show
    key = pygame.key.get_pressed()

    if can_show == False:
        time_elapsed_show = t.time() - time_show

    if time_elapsed_show == None or time_elapsed_show >= 0.25:
        can_show = True

    if key[pygame.K_F8] and can_show == True:
        if "DRAWRECT" not in ENTLIST[1].tags:
            ENTLIST[1].tags.append("DRAWRECT")
            for object in ENTLIST[0].OBJECTS + ENTLIST:
                if object.name == "!WORLD!" or object.name == "!PLAYER!":
                    continue
                
                if object.ShouldCollide():
                    if "DRAWRECT" not in object.tags:
                        object.tags.append("DRAWRECT")

            can_show = False
            time_show = t.time()
        else:
            ENTLIST[1].tags.remove("DRAWRECT")
            for object in ENTLIST[0].OBJECTS:
                for object in ENTLIST[0].OBJECTS + ENTLIST:
                    if object.name == "!WORLD!" or object.name == "!PLAYER!":
                        continue

                    if "DRAWRECT" in object.tags:
                        object.tags.remove("DRAWRECT")

            can_show = False
            time_show = t.time()

# print(ENTLIST[0].OBJECTS[4].type)
            
width_now = 256
height_now = 256
            
def CenterStuff():
    global width_now, height_now

    width_current = screen.get_width()
    height_current = screen.get_height()

    center_org_x = width_now
    center_org_y = height_now

    center_x = width_current / 2
    center_y = height_current / 2

    centerx_now = center_x - center_org_x
    centery_now = center_y - center_org_y

    for x in ENTLIST[0].OBJECTS + ENTLIST:
        if x.name == "!WORLD!" or x.name == "!PLAYER!":
            continue

        x.rect.move_ip(centerx_now, centery_now)

    width_now = center_x
    height_now = center_y
    ENTLIST[1].CenterPlayer()

saved = False

def save():
    global lvlname,saved,all_keys
    width_now = screen.get_width()
    height_now = screen.get_height()
    #checkni levelname kk
    
    if (not saved) and (lvlname != "0" and lvlname != "1" and lvlname != "2" and lvlname != "3") :
        return
    
    if (not saved) and int(lvlname) > 0:
        pygame.display.set_mode((512,512),pygame.RESIZABLE)
        CenterStuff()
        file = open("assets\\levelsave.txt","w")
        file.write("BOSS "+str(lvlname)+" "+str(all_keys)+"\n")
        file.write("SAVEFILE\n\n")
        for i in ENTLIST[0].OBJECTS:
            file.write(i.type+" "+"\""+i.img_path+"\""+" "+str(i.rect.center[0])+" "+str(i.rect.center[1])+" "+str(i.width)+" "+str(i.height)+" "+str(i.rotation)+"\n")
        file.close()
        LoadSettings()
        saved = True
    if (not saved) and int(lvlname) == 0:
        file = open("assets\\levelsave.txt","w")
        file2 = open("assets\\level1.txt","r")
        file.write("BOSS "+str(1)+" "+str(all_keys)+"\n")
        for i in file2:
            file.write(i)
        file.close()    
        file2.close()
        saved = True    

def SpawnEnemies():
    enemy = Goblin()

def SpawnBoss():    
    BOSS = "sans"
    file = open("assets\\loadlvl.txt")
    lvlname = file.readline()
    file.close()
    if lvlname == "0" or lvlname == "1" or lvlname == "2" or lvlname == "3":
        if int(lvlname) >= len(levels):
            lvlname = len(levels)-1

        if int(lvlname) == 2: 
            BOSS = "ghost"
        if int(lvlname) == 3: 
            BOSS = "god"

    boss = Boss(type=BOSS)

click = GetTime()
def GetDistance(self, other):

    mypos = pygame.Vector2(self.rect.center)
    opos = pygame.Vector2(other.rect.center)
    return (mypos - opos).length()

def Interaction():
    global click,all_keys
    key = pygame.key.get_pressed()
    player = ENTLIST[1]

    if key[pygame.K_e] and click + 0.07 < GetTime():
        for object in ENTLIST[0].OBJECTS:
            if object.rect.collidepoint(pygame.mouse.get_pos()) and GetDistance(ENTLIST[1],object) <= 320:
                if object.type == "CHEST":
                    object.image = pygame.image.load("assets\\object\\misc\\key.png")
                    object.image = pygame.transform.rotate(object.image,object.rotation)
                    object.type = "KEY"
                    click = GetTime()
                    return

                elif object.type == "KEY":
                    for items in player.inventory.items():
                        item,value = items
                        if value == False:
                            player.inventory[item] = True
                            object.Kill()
                            all_keys = int(all_keys) + 1
                            break
                    click = GetTime()
                    return

                if object.type == "DOOR" and GetDistance(ENTLIST[1],object) <= 320:
                    if object.img_path == "assets\\floor\\big_door_locked.png":              
                        if int(all_keys) >= 3 and object.type == "DOOR":
                            object.type = "DOOR_O"
                            object.image = pygame.image.load("assets\\floor\\big_door_open.png")   
                            object.image = pygame.transform.rotate(object.image,object.rotation)
                            click = GetTime()  
                            return
                    
                    else:
                        object.type = "DOOR_O"
                        object.image = pygame.image.load("assets\\floor\\big_door_open.png")   
                        object.image = pygame.transform.rotate(object.image,object.rotation)
                        click = GetTime()
                        return 

                if object.type == "DOOR_O":
                    object.type = "DOOR"
                    object.image = pygame.image.load("assets\\floor\\big_door_closed.png")   
                    object.image = pygame.transform.rotate(object.image,object.rotation)
                    click = GetTime()
                    return
                
def DevMode():
    global ENTLIST,all_keys,click
    key = pygame.key.get_pressed()
    if key[pygame.K_F9] and click + 0.5 < GetTime():
        all_keys = 3
        ENTLIST[1].stamina = 10000
        ENTLIST[1].health = 10000

        click = GetTime()


font = pygame.font.Font(None,40)
text = font.render("keys "+str(all_keys)+"\\"+str(3),True,(255,255,255))
text_rect = text.get_rect()

def UpdateText():
    global text
    text = font.render("keys "+str(all_keys)+"\\"+str(3),True,(255,255,255))

menu2 = PauseMenu_()
menu = MainMenu()
menu.load()
continue_game = menu.MenuLoop()
menu2.load()

def MainLoop():
    global running, all_keys,text,text_rect,continue_game,saved
    StartUp()
    running = True
    all_keys = 0
    if continue_game:
        LoadSave()
        continue_game = False
    else:    
        LoadWorld()

    LoadSettings()  
    
    SpawnBoss()

    while running:
        key = pygame.key.get_pressed()
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                save()
                pygame.quit()
                os._exit(0)
            if event.type == pygame.VIDEORESIZE:
                CenterStuff()
                menu2.CenterStuff()
                menu2.save()

            if menu2.paused == True: 
                menu2.PauseMenuEvent(event)
                menu2.CenterStuff()
                sound[0].SetVolume()

        menu2.PauseMenuToggle()


        if menu2.paused == False:
            HandleKeys()
            UpdateThings()
            ShowColl()
            SpawnEnemies()
            Interaction()
            DevMode()

            ENTLIST[1].DrawHealthRect()
            ENTLIST[1].DrawStaminaRect()

        screen_size()

        if menu2.paused == True: 
            menu2.PauseMenuRender()
            save()
        else:
            CenterStuff()
            saved = False

        screen.blit(text,(screen.get_width()-(text_rect.width+50),text_rect.height))

        pygame.display.flip() 

        clock.tick(120)

        UpdateTime(clock.tick(120))
        # print(clock.get_fps())

        pygame.display.update()
        
    return

while 1:
    MainLoop()


pygame.quit()
os._exit(0)

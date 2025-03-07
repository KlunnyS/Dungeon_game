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

def LoadWorld():
    UnloadLevel()
    global lvlname,resolution
    pygame.display.set_mode((512,512),pygame.RESIZABLE)
    
    file = open("assets\\loadlvl.txt")
    lvlname = file.readline()
    file.close()

    if int(lvlname) >= len(levels):
        lvlname = len(levels)-1
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


def UnloadLevel():
    ENTLIST[0].OBJECTS = []

def LoadSettings():
    settings = []
    res = False
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
        if i.strip() == "Resolution":
            res = True
    CenterStuff()
    file.close()

# menu2 = PauseMenu_()
# menu = MainMenu()
# menu.load()
# menu.MenuLoop()
  
def StartUp():
    global ENTLIST
    ENTLIST.clear()
    Entity()
    World()
    Player()

# StartUp()

# LoadWorld()

# ufo = Object()
# ufo.name = "ufo"
# ufo.img_path = "assets\\ufo.png"
# ufo.type = "WALL"
# ufo.pos = 64, 64
# ufo.width = 64
# ufo.height = 64
# ufo.health = 1
# ufo.health_max = 1000
# ufo.GenRect()
# ufo.AddToObjList()

# checkp = Decoration()
# checkp.img_path = "assets\\checkpoint.gif"
# checkp.type = "WALL"
# checkp.name = "ORB"
# checkp.isgif = True
# checkp.width = 64
# checkp.height = 64
# checkp.pos = 128, 128
# # checkp.animate = True
# checkp.frame = 3
# checkp.GenRect()
# checkp.AddToObjList()

# zatial nie
# p = MagicBall()
# p.GenRect()
# p.AddToList()



# def UpdateWorld():
#     global ENTLIST
#     ENTLIST[0].Update()

# def UpdateEntities():
#     global ENTLIST
#     for x in range(1, len(ENTLIST)): # uz aj player!
#         ENTLIST[x].Update()

def UpdateThings():
    global running,ENTLIST
    for x in ENTLIST:
        if x.Update():
            running = False
            save()
            ENTLIST[0].OBJECTS.clear()
            pygame.display.set_mode((512,512),pygame.RESIZABLE)
            # MainLoop()
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

    # if key[pygame.K_0] & True:
    #     p = Enemy()

    if key[pygame.K_w] & True:
        self.image = self.anim_B
        posy += self.speed
        self.last_movedir = "B"

    if key[pygame.K_s] & True:
        self.image = self.anim_F
        posy -= self.speed
        self.last_movedir = "F"

    if key[pygame.K_a] & True:
        self.image = self.anim_L
        posx += self.speed
        self.last_movedir = "L"

    if key[pygame.K_d] & True:
        self.image = self.anim_R
        posx -= self.speed
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

    # TO DO: vymaz asi?
    # if y_blocked and y_blocked: # ani do jedneho smeru nemozem
    #     return

    for x in ENTLIST[0].OBJECTS + ENTLIST:
        if x.name == "!WORLD!" or x.name == "!PLAYER!":
            continue

        if y_blocked == False:
            x.rect.y += posy
        if x_blocked == False:
            x.rect.x += posx

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
        if mode == pygame.RESIZABLE:
            mode = pygame.FULLSCREEN
            screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),mode)
            ENTLIST[1].CenterPlayer()
            can_FS = False
            time_FS = t.time()

        elif mode == pygame.FULLSCREEN:
            mode = pygame.RESIZABLE
            screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),mode)
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

def save():
    RESOLUTION = (screen.get_width(),screen.get_height())
    file = open("settings.txt","w")
    file.write("Resolution\n")
    file.write(str(RESOLUTION[0])+" "+str(RESOLUTION[1])+" "+"resize")
    file.close()


img = pygame.image.load("assets/menu/New Piskel (1).png")
def DrawMask():
    # maskw = img.get_width()
    # maskh = img.get_height()

    # win_w = screen.get_width()
    # win_h = screen.get_height()

    # f_w = (win_w - maskw) / 2
    # f_h = (win_h - maskh) / 2

    # screen.blit(img, (f_w, f_h))
    pass

def SpawnEnemies():
    enemy = Enemy()


def SpawnBoss():
    boss = Boss()

click = GetTime()

def Interaction():
    global click,all_keys
    key = pygame.key.get_pressed()
    player = ENTLIST[1]

    if key[pygame.K_e] and click + 0.5 < GetTime():
        for object in ENTLIST[0].OBJECTS:
            if object.rect.collidepoint(pygame.mouse.get_pos()):
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
                            all_keys += 1
                            break
                    click = GetTime()
                    return

                if object.type == "DOOR":
                    if object.img_path == "assets\\floor\\big_door_locked.png":
                        # for keys in player.inventory.items():
                        #     item,value = keys
                        #     if value == True:
                        #         all_keys += 1                
                        if all_keys >= 3 and object.type == "DOOR":
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
menu.MenuLoop()
menu2.load()

def MainLoop():
    global running, all_keys,text,text_rect
    StartUp()
    running = True
    
    LoadWorld()
    LoadSettings()  
    
    SpawnBoss()

    while running:
        key = pygame.key.get_pressed()
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                os._exit(0)
            if event.type == pygame.VIDEORESIZE:
                # screen = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
                # ENTLIST[1].CenterPlayer()
                CenterStuff()
                menu2.CenterStuff()

            if menu2.paused == True: 
                menu2.PauseMenuEvent(event)
                menu2.CenterStuff()

        menu2.PauseMenuToggle()


        if menu2.paused == False:
            HandleKeys()
            UpdateThings()
            ShowColl()
            # DrawMask()
            SpawnEnemies()
            Interaction()
            DevMode()

            ENTLIST[1].DrawHealthRect()
            ENTLIST[1].DrawStaminaRect()

        screen_size()

        if menu2.paused == True: 
            menu2.PauseMenuRender()
        else:
            CenterStuff()

        screen.blit(text,(screen.get_width()-(text_rect.width+50),text_rect.height))

        pygame.display.flip() 

        clock.tick(120)
        # float(int(value*1en))*1e-n

        UpdateTime(clock.get_time())
        # print(clock.get_fps())

        pygame.display.update()

    return

while 1:
    MainLoop()

pygame.quit()
os._exit(0)

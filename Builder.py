import pygame as py,os,time as t

#L-click - place
#1 - Floor
#2 - Wall
#delete - closes program without saving
#esc - closes program and saves level

action = input("load/create: ")
action = action.strip()
action = action.lower()
while action != "load" and action != "create" and action != "c" and action != "l":
    action = input("load/create: ")
    action = action.strip()
    action = action.lower()

 
os.chdir(os.path.dirname(os.path.abspath(__file__)))
py.init()
resolution = [512,512]
screen = py.display.set_mode(resolution)
py.display.set_caption("Level Builder")
icon = py.image.load('assets\\player\\player_F.png')
py.display.set_icon(icon)
clock = py.time.Clock()
running = True

multi = 1
ASSETS = ['FLOOR assets\\floor\\floor_dungeon_v2_Floor.png 0 0 256 256 0' ,'WALL assets\\floor\\wall.png 0 0 40 256 0'
,'DOOR assets\\floor\\big_door_locked.png 0 0 256 115 0','WALL assets\\object\\crate\\crate.png 0 0 64 64 0','WALL assets\\object\\crate\\crate32.png 0 0 32 32 0'
,'MULTI assets\\object\\vase\\vase-'+str(multi)+'.png 0 0 64 64 0','MULTI assets\\object\\torch\\torch-'+str(multi)+'.png 0 0 32 32 0'
,'SPAWNER assets\\enemy\\spawner\\spawner_base.png 0 0 64 64 0','BOSS assets\\enemy\\spawner\\spawner_base.png 0 0 64 64 0','CHEST assets\\object\\misc\\chest.png 0 0 64 35 0']
OBJECTS = []
ENTITIES = []
using = None
rot = 0
file_found = False
GRID = []


class Object():
    def __init__(self):
        self.name = ""
        self.path = ""
        self.multiple = []
        self.pos_x = int()
        self.pos_y = int()
        self.width = int()
        self.height = int()
        self.rotation = int()
        self.pos = []
        self.layer = 0
        self.image = None
        self.rect = None
        
    def CalcInitPos(self): self.pos = [self.pos_x - self.width / 2, self.pos_y - self.height / 2]

    def CalcBlitPos(self): self.pos = [self.pos[0] - self.width / 2, self.pos[1] - self.height / 2]

    def CalcSavePos(self): self.pos = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]

    def SnapToGrid_X(self):
        for i in range(len(GRID)):
            if self.pos[0] > GRID[len(GRID)-1]:
                self.pos[0] = GRID[len(GRID)-1]
            if self.pos[0] <= GRID[i]:

                self.pos[0] = GRID[i]
                return
            
    def SnapToGrid_Y(self):
        for i in range(len(GRID)):
            if self.pos[1] > GRID[len(GRID)-1]:
                self.pos[1] = GRID[len(GRID)-1]
            if self.pos[1] <= GRID[i]:
                self.pos[1] = GRID[i]
                return

    def SnapToGrid(self):
        self.SnapToGrid_X()
        self.SnapToGrid_Y()

    def CreateRect(self):
        self.rect = py.rect.Rect(self.pos[0],self.pos[1],self.width,self.height)
        
if action == "load" or action == "l":
    file_name = input("Enter name of the file: ")
    name = file_name
    file = open("assets\\"+file_name+".txt","r")
    for i in file:
        if i.strip() == "SAVEFILE" and file_found == False:
            print("file found")
            file_found = True
        elif file_found & True and i != "\n":
            Object_type, Object_path, Object_pos_x, Object_pos_y, Object_width, Object_height, Object_rotation = i.split()
            obj = Object()
            obj.layer = 0
            obj.name = Object_type
            obj.path = Object_path.strip("\"")
            obj.width = int(Object_width)
            obj.height = int(Object_height)
            obj.pos_x = float(Object_pos_x)
            obj.pos_y = float(Object_pos_y)
            obj.rotation = int(Object_rotation)
            obj.image = py.image.load(obj.path)
            obj.image = py.transform.rotate(obj.image, int(obj.rotation))
            if obj.rotation == 90 or obj.rotation == 270:
                temp = obj.width
                obj.width = obj.height
                obj.height = temp
            obj.CalcInitPos()
            obj.CreateRect()
            ENTITIES.append(obj)
    file.close()
elif action == "create" or action == "c":
    name = input("Enter name for the save file: ")

def LoadObjects():
    global multi     
    for i in range(len(ASSETS)):
        obj = Object()
        Object_type, Object_path, Object_pos_x, Object_pos_y, Object_width, Object_height, Object_rotation = ASSETS[i].split() 
        obj.name = Object_type
        if obj.name == "MULTI":
            for j in range(1,5):
                multi = j
                Object_type, Object_path, Object_pos_x, Object_pos_y, Object_width, Object_height, Object_rotation = ASSETS[i].split()
                temp = Object_path.split("-")
                temp2 = temp[1].split(".")
                temp.pop(1)
                temp.append(temp2[0])
                temp.append(temp2[1])
                temp[1] = multi
                Object_path = str(temp[0])+"-"+str(temp[1])+"."+str(temp[2])
                obj.multiple.append(Object_path)
            multi = 0

        if obj.name == "DOOR":
            obj.multiple = ["assets\\floor\\big_door_locked.png","assets\\floor\\big_door_closed.png","assets\\floor\\big_door_locked.png","assets\\floor\\big_door_closed.png"]
            
   
        obj.path = Object_path.strip("\"")
        obj.width = int(Object_width)
        obj.height = int(Object_height)
        obj.pos_x = float(Object_pos_x)
        obj.pos_y = float(Object_pos_y)
        obj.rotation = int(Object_rotation)
        obj.image = py.image.load(obj.path)
        obj.image = py.transform.rotate(obj.image, int(obj.rotation))
        obj.CalcInitPos()
        OBJECTS.append(obj)

LoadObjects()
        
def RenderObject():
    if len(ENTITIES) > 0:
        for i in ENTITIES:
            screen.blit(i.image,i.pos)

def CreateAndAddEnt():
    obj = Object()
    obj.rotation = using.rotation
    obj.image = using.image
    obj.image = py.transform.rotate(obj.image, int(obj.rotation))
    obj.pos_x = using.pos[0]
    obj.pos_y = using.pos[1]
    obj.name = using.name
    obj.path = using.path
    obj.multiple = using.multiple
    if using.name == "MULTI" or using.name == "DOOR":
        obj.path = obj.multiple[multi]
        obj.image = py.image.load(obj.path)
        obj.image = py.transform.rotate(obj.image,obj.rotation)
    obj.width = using.width
    obj.height = using.height
    if obj.rotation == 90 or obj.rotation == 270:
        temp = obj.width
        obj.width = obj.height
        obj.height = temp
    obj.pos = using.pos
    obj.CalcBlitPos()
    obj.SnapToGrid()
    obj.CreateRect()
    for i in ENTITIES:
        if obj.rect.colliderect(i.rect):
            obj.layer = i.layer + 1
            # je to teplé fixni neskorej
    print(obj.layer,obj.name)
    ENTITIES.append(obj)

time_elapsed_rot = None
time_rot = None
can_rot = None

def rotate():
    global rot,time_elapsed_rot,time_rot,can_rot

    if can_rot == False:
        time_elapsed_rot = t.time() - time_rot

    if time_elapsed_rot == None or time_elapsed_rot >= 0.25:
        can_rot = True

    if key[py.K_r] and can_rot == True:
        rot += 90
        if rot == 360:
            rot = 0
        can_rot = False
        time_rot = t.time()


def HandleMove():
    global ENTLIST
    key = py.key.get_pressed()

    if key[py.K_a] & True:
        for x in ENTITIES:
            x.pos[0] += 4

    elif key[py.K_d] & True:
        for x in ENTITIES:
            x.pos[0] -= 4

    if key[py.K_w] & True:
        for x in ENTITIES:
            x.pos[1] += 4

    elif key[py.K_s] & True:
        for x in ENTITIES:
            x.pos[1] -= 4 

# for small adjustment of final pos
    if key[py.K_LEFT] & True:
        for x in ENTITIES:
            x.pos[0] += 0.5

    elif key[py.K_RIGHT] & True:
        for x in ENTITIES:
            x.pos[0] -= 0.5

    if key[py.K_UP] & True:
        for x in ENTITIES:
            x.pos[1] += 0.5

    elif key[py.K_DOWN] & True:
        for x in ENTITIES:
            x.pos[1] -= 0.5

def sort():
    global ENTITIES
    temp1 = []
    temp2 = []
    for x in range(len(ENTITIES)):
        if ENTITIES[x].layer == 0:
            temp1.append(ENTITIES[x])
        elif ENTITIES[x].layer > 0:
            temp2.append(ENTITIES[x])
    temp1 = temp1 + temp2

def Preview():
    global using
    if using == None:
        using = OBJECTS[0]
    using.pos = list(py.mouse.get_pos())
    surf = py.Surface((using.width, using.height))
    surf.fill((0, 255, 0))
    surf.set_alpha(32)
    width = using.width
    height = using.height
    if rot == 90 or rot == 270:
        temp = width
        width = height
        height = temp
    using.pos = [using.pos[0] - width / 2, using.pos[1] - height / 2]
    surf.fill((0, 255, 0))
    surf.set_alpha(32)
    surf = py.transform.rotate(surf, rot)
    using.SnapToGrid()
    if (using.pos[0]+width) > 512 or (using.pos[1]+height) > 512:
        surf.fill((255, 0, 0))
    screen.blit(surf, using.pos)
    if using.name == "MULTI":
        screen.blit(py.transform.rotate(py.image.load(using.multiple[multi]),rot),using.pos)
    elif using.name == "DOOR":
        screen.blit(py.transform.rotate(py.image.load(using.multiple[multi]),rot),using.pos)
    elif using.name == "CHEST":
        screen.blit(py.transform.rotate(using.image,rot),using.pos)

def GenGrid():
    for i in range(0,512,4):
        GRID.append(i)
GenGrid()

def DeletObj():
    pos = py.mouse.get_pos()
    obj_list = []
    obj_del = None
    if len(ENTITIES) > 0 :
        for i in reversed(ENTITIES):
            if (pos[0] >= i.pos[0] and pos[0] <= i.pos[0]+i.width) and (pos[1] >= i.pos[1] and pos[1] <= i.pos[1]+i.height):
                obj_list.append(i)
                print(i.name,i.layer)
        
        if len(obj_list) > 0:
            for x in obj_list:
                if obj_del == None:
                    obj_del = x
                if x.layer >= obj_del.layer:
                    obj_del = x
            ENTITIES.remove(obj_del)              

def save():
    file = open("assets\\"+name+".txt","w")
    file.write("SAVEFILE\n\n")
    sort()
    for i in ENTITIES:
        i.CalcSavePos()
        if i.rotation == 90 or i.rotation == 270:
            temp = i.width
            i.width = i.height
            i.height = temp
        file.write(i.name+" "+"\""+i.path+"\""+" "+str(i.pos[0])+" "+str(i.pos[1])+" "+str(i.width)+" "+str(i.height)+" "+str(i.rotation)+"\n")
    file.close()

time_elapsed_switch = None
time_switch = None
can_switch = None

def bind():
    global using,running,multi,time_elapsed_switch,time_switch,can_switch
    if key[py.K_1]:
        using = OBJECTS[0]
        print("Floor")

    if key[py.K_2]:
        using = OBJECTS[1]
        print("Wall")

    if key[py.K_3]:
        using = OBJECTS[2]
        print("Door")

    if key[py.K_4]:
        using = OBJECTS[3]
        print("CrateBig")

    if key[py.K_5]:
        using = OBJECTS[4]
        print("CrateSmall")

    if key[py.K_6]:
        using = OBJECTS[5]
        print("Vase")

    if key[py.K_7]:
        using = OBJECTS[6]
        print("Torch")

    if key[py.K_8]:
        using = OBJECTS[7]
        print("Spawner")

    if key[py.K_9]:
        using = OBJECTS[8]
        print("Boss")

    if key[py.K_0]:
        using = OBJECTS[9]
        print("Chest")
    
    if can_switch == False:
        time_elapsed_switch = t.time() - time_switch

    if time_elapsed_switch == None or time_elapsed_switch >= 0.25:
        can_switch = True

    if key[py.K_q] and len(using.multiple) > 0 and can_switch == True:
        multi += 1
        time_switch = t.time()
        can_switch = False
        print(multi)
        if multi == 4:
            multi = 0

    if key[py.K_DELETE]:
        running = False

player = py.image.load("assets\\player\\player_F.png")

while running:
    key = py.key.get_pressed()
    screen.fill((0,0,0))
    for event in py.event.get():
        if event.type == py.QUIT or key[py.K_ESCAPE]:
            save()
            running = False

        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                if using == None:
                    using = OBJECTS[0]
                using.pos = py.mouse.get_pos()
                using.rotation = rot
                CreateAndAddEnt()  
            elif event.button == 3:
                DeletObj() 

    RenderObject()
    rotate()
    HandleMove()
    Preview()
    bind()

    screen.blit(player,(224,224))

    
    py.display.flip() 

    clock.tick(120)
    py.display.update()

py.quit()
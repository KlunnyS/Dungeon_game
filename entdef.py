from pygame import Vector2
import basedef
from basedef import *

class Entity():
    def __init__(self):
        self.name = ""
        self.id = self.GenID() #neopakovatelne id tejto entity

        self.pos = pygame.Vector2()

        self.width = 0
        self.height = 0

        self.tags = []

        self.image = None

        self.rect = None # collision

        self.type = ""

        self.rotation = 0

        self.img_path = ""
        self.adjustment = 0

        self.health = 0
        self.health_max = 0

        self.time_stamp = 0
        self.touch_timestamp = 0

        self.render = True

        self.dead = False

        self.last_movedir = ''

        self.speed = 0.4

        self.think = int()


    def AddToList(self):
        global ENTLIST

        ENTLIST.append(self)

        print("Entity:", self.name, "id:", self.id, "added to the entlist.")

    def GetKillList(self):
        global ENTLIST # ?
        return ENTLIST

    def Kill(self):
        if self.dead:
            return
        
        self.dead = True

        arr = self.GetKillList()
        arr.pop(arr.index(self))

        print("Killed entity:", self.name, "id:", self.id, "!!!")

        del self

    def GenID(self):
        return id(self)

    def GetID(self):
        return self.id

    def DrawHealthRect(self):
        if self.health <= 0:
            return

        pos = self.rect.x, self.rect.y - 10
        color = None

        if self.health > ((self.health_max / 3) * 2):
            color = (0, 255, 0)
        elif self.health > ((self.health_max / 3) * 1):
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)


        if self.name != "!PLAYER!":
            hp_w = (self.rect.w / self.health_max) * self.health
            if hp_w <= 1:
                hp_w = 1
            hp_rect = pygame.surface.Surface((hp_w, 5))
        else:
            hp_rect = pygame.surface.Surface((256 / 100 * self.health, 12.5))

        hp_rect.fill(color)
        hp_rect.set_alpha(192)

        if self.name != "!PLAYER!":
            screen.blit(hp_rect, pos)
        else:
            screen.blit(hp_rect, (10, 10))

    def DrawBBOX(self):
        if "DRAWRECT" in self.tags:
            bbox = pygame.surface.Surface((self.rect.w, self.rect.h))
            if self.name == "!PLAYER!":
                bbox.fill((0, 255, 0))
            else:
                bbox.fill((255, 0, 0))
            bbox.set_alpha(64)

            screen.blit(bbox, self.rect.topleft)

    def CanRender(self):
        global ENTLIST
        p1 = pygame.Vector2(self.rect.center)
        p2 = pygame.Vector2(ENTLIST[1].rect.center)

        len =  (p1 - p2).length()

        return self.render and len < 1920

    def MakeImage(self):
        if self.image == None and self.img_path != None:
            self.image = pygame.image.load(self.img_path)
            self.image = pygame.transform.rotate(self.image, self.rotation)

    def RenderObject(self):
        if self.CanRender() == False:
            return

        self.MakeImage()

        screen.blit(self.image, self.rect.topleft)

        self.DrawBBOX()
        self.DrawHealthRect()

    def HasRect(self):
        return self.rect != None

    def ShouldCollide(self):
        return False

    def GenRect(self):
        if self.HasRect() == False:
            surf = pygame.Surface((self.width, self.height))
            surf = pygame.transform.rotate(surf, self.rotation)
            self.rect = surf.get_rect()
            self.rect.center = self.pos

    def HandleInteraction(self, other) -> bool:
        return False

    def Heal(self):
        return

    def Update(self):
        if self.dead:
            return
        
        if self.health <= 0 and self.health_max >= 1:
            self.Kill()
            return True

        self.RenderObject()


    def GetDir(self, other):
        mypos = pygame.Vector2(self.rect.center)
        opos = pygame.Vector2(other.rect.center)

        h = pygame.Vector2(opos[0] - mypos[0], opos[1] - mypos[1])
        if h.length() > 0:
            h.normalize_ip()

        return h
    
    def CheckCollision(self, vec = pygame.Rect(0, 0, 0, 0)):
        colliding = False

        if vec.w != 0 and vec.h != 0:
            for x in ENTLIST[0].OBJECTS + ENTLIST:
                if x == self or x.name == "!WORLD!": 
                    continue

                if type(self) == type(x):
                    continue
                
                if x.ShouldCollide() == False:
                    continue

                if x.rect.colliderect(vec):
                    if x.HandleInteraction(self):
                        colliding = True

                    # intersect = x.rect.clip(self.rect)
                    # self.rect.x -= intersect.w
                    # self.rect.y -= intersect.y
        else:
            for x in ENTLIST[0].OBJECTS + ENTLIST:
                if x == self or x.name == "!WORLD!": 
                    continue

                if type(self) == type(x):
                    continue
                
                if x.ShouldCollide() == False:
                    continue

                mypos = pygame.Vector2(self.rect.center)
                opos = pygame.Vector2(x.rect.center)
                
                if (mypos - opos).length() > 512:
                    continue

                if x.rect.colliderect(self.rect):
                    if x.HandleInteraction(self):
                        colliding = True

                    if type(x) == Object:
                        overlap_x = min(self.rect.right - x.rect.left, x.rect.right - self.rect.left)
                        overlap_y = min(self.rect.bottom - x.rect.top, x.rect.bottom - self.rect.top)

                        if overlap_x < overlap_y:
                            if self.rect.centerx < x.rect.centerx:
                                self.rect.right = x.rect.left
                            else:
                                self.rect.left = x.rect.right
                        else:
                            if self.rect.centery < x.rect.centery:
                                self.rect.bottom = x.rect.top
                            else:
                                self.rect.top = x.rect.bottom
                        

                    # intersect = x.rect.clip(self.rect)
                    # self.rect.x -= intersect.w
                    # self.rect.y -= intersect.y

                    # if type(self) == Projectile or type(self) == Boss:
                    #     continue
                        
                    # overlap_x = min(self.rect.right - x.rect.left, x.rect.right - self.rect.left)
                    # overlap_y = min(self.rect.bottom - x.rect.top, x.rect.bottom - self.rect.top)
                    
                    # # Resolve the collision in the axis with the smallest overlap
                    # if overlap_x < overlap_y:
                    #     if self.rect.centerx < x.rect.centerx:
                    #         self.rect.right = x.rect.left
                    #     else:
                    #         self.rect.left = x.rect.right
                    # else:
                    #     if self.rect.centery < x.rect.centery:
                    #         self.rect.bottom = x.rect.top
                    #     else:
                    #         self.rect.top = x.rect.bottom

        return colliding


    def TryMove(self, vec: pygame.Vector2):
        x_blocked = False
        y_blocked = False

        for x in ENTLIST[0].OBJECTS + ENTLIST:
            if x == self or x.name == "!WORLD!": 
                continue
            
            if x.ShouldCollide() == False:
                continue

            if x.rect == None:
                continue

            mypos = pygame.Vector2(self.rect.center)
            opos = pygame.Vector2(x.rect.center)
            

            if (mypos - opos).length() > 512:
                continue

            # print(x.rect)
            
            rect_predict = self.rect.copy()
            rect_predict.x += vec[0] * self.speed * GetDTTime()
            x_blocked = self.CheckCollision(rect_predict)
                    # print(rect_predict.center)
                    # print(ENTLIST[1].rect.center) 
                # print(self.name, "Coliding with", x.type, x.name)
                # print(self.rect.center, x.rect.center)
                
            rect_predict = self.rect.copy()
            rect_predict.y += vec[1] * self.speed * GetDTTime()
            y_blocked = self.CheckCollision(rect_predict)

        if x_blocked == False:
            self.rect.x += self.speed * vec[0] * GetDTTime()
        if y_blocked == False:
            self.rect.y += self.speed * vec[1] * GetDTTime()

    def GetDistance(self, other):
        mypos = pygame.Vector2(self.rect.center)
        opos = pygame.Vector2(other.rect.center)

        return (mypos - opos).length()


class Player(Entity):
    def __init__(self):
        super().__init__()

        self.name = "!PLAYER!"
        self.type = "!PLAYER!"
        self.img_F_path = 'assets\\player\\player_F.png'
        self.anim_F = gif_pygame.load('assets\\player\\player_F_animat.gif')
        self.img_L_path = 'assets\\player\\player_L.png'
        self.anim_L = gif_pygame.load('assets\\player\\player_L_animat.gif')
        self.img_R_path = 'assets\\player\\player_R.png'
        self.anim_R = gif_pygame.load('assets\\player\\player_R_animat.gif')
        self.img_B_path = 'assets\\player\\player_B.png'
        self.anim_B = gif_pygame.load('assets\\player\\player_B_aniamt.gif')

        self.img_F = pygame.image.load(self.img_F_path)
        self.img_B = pygame.image.load(self.img_B_path)
        self.img_L = pygame.image.load(self.img_L_path)
        self.img_R = pygame.image.load(self.img_R_path)

        self.image = self.img_F # little hack

        self.sprint_start = None
        self.sprint_stop = None
        self.moving = False
        self.speed = 0.4
        self.stamina = 100
        self.staminatimer = None
        self.adjx = 0
        self.adjy = 0

        self.pos = [screen.get_width()/2, screen.get_height()/2]
        self.width = 40
        self.height = 64

        self.health = 100
        self.health_max = 100

        self.clickstamp = int()

        self.inventory = {"key1": False,"key2": False,"key3": False}

        self.GenRect()
        self.AddToList()

    def AddToList(self):
        global ENTLIST

        ENTLIST.insert(1,self)

        print("Entity:", self.name, "id:", self.id, "added to the entlist.")

    def ClearInv(self):
        self.inventory = {"key1": False,"key2": False,"key3": False}

    def Kill(self):
        global sound
        print("Player died!")
        # arr = self.GetKillList()
        # arr.pop(arr.index(self))
        # print("Killed entity:", self.name, "id:", self.id, "!!!")
        screen.blit(pygame.transform.scale(pygame.image.load('assets\\enemy\\god\\god_animat.gif'),(screen.get_width(),screen.get_height())),(0,0))
        pygame.display.update()
        sound[0].PlayDeath()
        t.sleep(4)

        del self
        return True

    def CenterPlayer(self):
        self.pos = [screen.get_width()/2, screen.get_height()/2]
        self.rect.center = self.pos

    def Heal(self):
        # print(self.touch_timestamp)
        if (self.touch_timestamp + 2 < GetTime()) and self.health < self.health_max:
            self.health += 5 / 120

    def RenderObject(self):
        pos = self.rect.x - 12, self.rect.y

        if self.moving:
            if type(self.image) != gif_pygame.GIFPygame:
                print("Neni to gif ale surface!")
                return
            screen.blit(self.image.blit_ready(), pos)
        else:
            if type(self.image) == gif_pygame.GIFPygame:
                print("Je to gif a nie surface!")
                return
            screen.blit(self.image, pos)

        self.DrawBBOX()

    def Update(self):
        if self.health <= 0:
            if self.Kill(): return True


        self.Heal()
        self.StaminaRegain()
        self.RenderObject()

        if pygame.mouse.get_pressed()[0] and self.clickstamp <= GetTime():
            self.clickstamp = GetTime() + 0.4

            pos_m = pygame.Vector2(pygame.mouse.get_pos())
            ang = (pos_m - self.pos).normalize()
            MagicBall(self.rect.center, ang)
            sound[0].PlayShot()

        if pygame.mouse.get_pressed()[2] and self.clickstamp <= GetTime():
            self.clickstamp = GetTime() + .25
            Goblin()

        # print("direction to", ENTLIST[0].OBJECTS[-1].name, self.GetDir(ENTLIST[0].OBJECTS[-1]))
    def StaminaDrain(self):
        if self.sprint_start + 0.1 < GetTime():
            self.stamina -= 8
            self.sprint_start = GetTime()

    def StaminaRegain(self):
        if self.stamina < 100 and self.speed == 0.4 and self.sprint_stop + 0.7 < GetTime() and self.staminatimer + 0.15 < GetTime():
            self.stamina += 8
            self.staminatimer = GetTime()

    def sprint(self):
        key = pygame.key.get_pressed()
        # print(self.stamina)
        if key[pygame.K_LSHIFT] and self.stamina > 0:
            self.speed = 0.8
            self.sprint_stop = None
            if self.sprint_start == None: self.sprint_start = GetTime()
            self.StaminaDrain()
        else:
            self.speed = 0.4
            self.sprint_start = None
            if self.sprint_stop == None: self.sprint_stop = GetTime() ; self.staminatimer = GetTime()

    def DrawStaminaRect(self):
        if self.stamina <= 0:
            return

        stamina_rect = pygame.surface.Surface((256 / 100 * self.stamina, 12.5))

        stamina_rect.fill((0,0,255))
        stamina_rect.set_alpha(192)

        screen.blit(stamina_rect, (10, 25))

class World(Entity):
    def __init__(self):
        super().__init__()
        self.OBJECTS = []
        self.name = "!WORLD!"
        self.render = False
        self.AddToList()

    def Update(self):
        for x in self.OBJECTS:
            x.Update()

class Object(Entity):
    global ENTLIST
    def __init__(self,enemy:str = None):
        super().__init__()
        self.enemy_num = int()
        self.enemy_type = enemy

    def AddToObjList(self):
        return ENTLIST[0].OBJECTS.append(self)

    def HandleInteraction(self, other) -> bool: # HACK
        if type(other) == MagicBall or type(other) == Projectile:
            other.Kill()
        return self.ShouldCollide()

    def GetKillList(self):
        global ENTLIST
        return ENTLIST[0].OBJECTS

    def ShouldCollide(self):
        return (self.type == "WALL") or (self.type == "MULTI") or (self.type == "DOOR") or (self.type == "CHEST")

class Decoration(Object):
    def __init__(self):
        super().__init__()

        self.animate = False
        self.image = None
        self.isgif = False
        self.frame = None

    def RenderObject(self):
        if self.image == None and self.img_path != None:
                if self.isgif == False:
                    self.image = pygame.image.load(self.img_path)
                    self.image = pygame.transform.rotate(self.image, self.rotation)
                else:
                    self.image = gif_pygame.load(self.img_path)
        else:
            if self.isgif:
                if self.animate:
                    img = self.image.blit_ready()
                else:
                    img = self.image.get_surfaces()

                    if self.frame != None:
                        img = img[self.frame]
                    else:
                        img = img[0]


                screen.blit(img, self.rect.topleft)
                self.DrawBBOX()
                return


            screen.blit(self.image, self.rect.topleft)

        self.DrawBBOX()



class MagicBall(Entity):
    def __init__(self, pos: pygame.Vector2, ang: pygame.Vector2):
        super().__init__()

        self.name = "boolet"

        self.img_path = "assets\\player\\bullet1.png"
        self.width = 64
        self.height = 64

        self.pos[0] = pos[0] #- self.width / 2
        self.pos[1] = pos[1] #- self.height / 2

        self.angle = ang

        self.img_path = "assets\\bullet\\ball.png"

        self.GenRect()
        self.AddToList()

    def HandleInteraction(self, other) -> bool:
        if self.type != other.type and other.type != "!PLAYER!":
            other.health -= 10
            self.Kill()

        return False

    def ShouldCollide(self):
        return True

    def Update(self):
        if self.dead:
            return
        
        if self.CheckCollision():
            self.DrawBBOX()
            return

        self.rect.center += self.angle * 1.5 * GetDTTime()

        # print("zijem", self.id)

        self.RenderObject()

class Enemy(Entity):
    def GetSpawnPos(self,spawner,spawnnum):
        return (spawner.rect.center[0]-128+(spawnnum*64),spawner.rect.center[1]-128+(spawnnum*64))
        # print(self.pos,spawnnum)

    def GetSpawner(self):
        for x in ENTLIST[0].OBJECTS:
            if x.type == "SPAWNER" and x.enemy_num < 3:
                x.enemy_num += 1
                return self.GetSpawnPos(x,x.enemy_num),x

        return 0,0

    def RemoveSpawner(self):
        self.spawn.enemy_num -= 1

    def __init__(self):
        super().__init__()

        self.anim_F = None
        self.anim_B = None
        self.anim_L = None
        self.anim_R = None

        self.img_F = None
        self.img_B = None
        self.img_L = None
        self.img_R = None

        self.last_movedir = 'F'

    def Update(self):
        if self.health <= 0:
            self.Kill()
            self.RemoveSpawner()

        else:
            pos = self.GetDir(ENTLIST[1])

            if self.GetDistance(ENTLIST[1]) <= 384 and self.CheckCollision() == False:
                self.TryMove(pos)

            self.RenderObject()

    def ShouldCollide(self):
        return True
    

    def TryMove(self, vec: Vector2):
        self.SwapImage(vec)
        super().TryMove(vec)

    
    def SwapImage(self, vec: pygame.Vector2):
        if vec[0] == 0 and vec[1] == 0:
            if vec[1] < 0:
                self.image = self.img_B
                self.last_movedir = 'B'

            elif vec[1] > 0:
                self.image = self.img_F
                self.last_movedir = 'F'

            elif vec[0] < 0:
                self.image = self.img_L
                self.last_movedir = 'L'

            elif vec[0] > 0:
                self.image = self.img_R
                self.last_movedir = 'R'
        else:
            if vec[1] < 0:
                self.image = self.anim_B
                self.last_movedir = 'B'

            elif vec[1] > 0:
                self.image = self.anim_F
                self.last_movedir = 'F'

            elif vec[0] < 0:
                self.image = self.anim_L
                self.last_movedir = 'L'

            elif vec[0] > 0:
                self.image = self.anim_R
                self.last_movedir = 'R'

    def RenderObject(self):
        if self.CanRender() == False:
            return
        
        if self.image == None:
            return
        
        if type(self.image) != gif_pygame.GIFPygame:
            # print(self.image)
            # print(self.last_movedir)
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(self.image.blit_ready(), self.rect.topleft)

        self.DrawBBOX()
        self.DrawHealthRect()

    def HandleInteraction(self, other) -> bool:
        if type(other) == type(self):
            return False

        if (type(other) == Player) and (GetTime() > self.touch_timestamp):
            sound[0].PlayEnemyAttack()
            other.health -= 10
            other.touch_timestamp = GetTime()
            self.touch_timestamp = GetTime() + 0.5

        if other != self:
            pos = self.GetDir(other)
            self.rect.center += pos * -2

        return False

    def GetKillList(self):
        global ENTLIST
        return ENTLIST


class Goblin(Enemy):
    def __init__(self):
        super().__init__()

        self.spawner = self.GetSpawner()
        self.pos = self.spawner[0]
        self.spawn = self.spawner[1]

        self.name = "ENEMS"
        self.type = "WALL"
        self.width = 64
        self.height = 64
        self.img_path = "assets\\enemy\\goblin_F.png"
        self.health = 100
        self.health_max = 100

        self.img_F = pygame.image.load("assets\\enemy\\goblin_F.png")
        self.img_B = pygame.image.load("assets\\enemy\\goblin_B.png")
        self.img_L = pygame.image.load("assets\\enemy\\goblin_L.png")
        self.img_R = pygame.image.load("assets\\enemy\\goblin_R.png")

        self.anim_F = gif_pygame.load("assets\\enemy\\goblin_F_animat.gif")
        self.anim_B = gif_pygame.load("assets\\enemy\\goblin_B_animat.gif")
        self.anim_L = gif_pygame.load("assets\\enemy\\goblin_L_animat.gif")
        self.anim_R = gif_pygame.load("assets\\enemy\\goblin_R_animat.gif")

        if self.pos != 0:
            self.GenRect()
            self.AddToList()
            if self.CheckCollision():
                self.rect.y += 64

class Boss(Enemy):
    def GetSpawner(self):
        for x in ENTLIST[0].OBJECTS:
            if x.type == "BOSS" and x.enemy_num == 0:
                x.enemy_num += 1
                return x.rect.center,x

        return 0,0

    def __init__(self,type:str = "sans"):
        super().__init__()

        self.font = pygame.font.Font(None,60)
        self.text = self.font.render("Great Enemy Defeated",True,(255,0,0))
        self.name = type
        self.health = 100
        self.health_max = 100
        self.type = "WALL"
        self.width = 96
        self.height = 96
        self.img_path = "assets\\enemy\\"+self.name+"\\"+self.name+".png"
        self.image = pygame.image.load(self.img_path)
        self.attack_melee = False
        self.attack_projectile = False
        self.shot_timestamp = 0
        if type == "sans": 
            self.attack_melee = True
            self.health = 250
            self.health_max = 250
        elif type == "ghost":
            self.attack_projectile = True
            self.health = 150
            self.health_max = 150
        elif type == "god":
            self.attack_projectile = True
            self.attack_melee = True
            self.health = 300
            self.health_max = 300
            self.image = gif_pygame.load("assets\\enemy\\"+self.name+"\\"+self.name+"_animat.gif")
            self.width = 128
            self.height = 128

        self.img_F = pygame.image.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_F.png")
        self.img_B = pygame.image.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_B.png")
        self.img_L = pygame.image.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_L.png")
        self.img_R = pygame.image.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_R.png")

        self.anim_F = gif_pygame.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_F_animat.gif")
        self.anim_B = gif_pygame.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_B_animat.gif")
        self.anim_L = gif_pygame.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_L_animat.gif")
        self.anim_R = gif_pygame.load("assets\\enemy\\"+str(type)+"\\"+str(type)+"_R_animat.gif")

        self.spawner = self.GetSpawner()
        self.pos = self.spawner[0]
        self.spawn = self.spawner[1]

        if self.pos != 0:
            self.pos = (self.pos[0] + r.randrange(-100,100,50),self.pos[1])
            self.GenRect()
            self.AddToList()

    def Update(self):
        if self.health <= 0:
            screen.fill((0,0,0))
            screen.blit(self.text,(screen.get_width()/2-225,screen.get_height()/2-50))
            pygame.display.update()
            t.sleep(2)
            if self.Kill(): 
                return True
            
            
        pos = self.GetDir(ENTLIST[1])

        if self.GetDistance(ENTLIST[1]) <= 1080:
            self.TryMove(pos)

        self.RenderObject()
        self.CheckCollision()
        self.ShootProjectile()

    def ShouldCollide(self):
        return True

    def HandleInteraction(self, other) -> bool:
        if type(other) == type(self):
            return False

        if type(other) == Player and self.attack_melee:
            other.health -= 50 / 120
            sound[0].PlayEnemyAttack()
            other.touch_timestamp = GetTime()

        if other != self:
            pos = self.GetDir(other)
            self.rect.center += pos * -2

        return False
    
    def ShootProjectile(self):
        if self.attack_projectile:
            if self.shot_timestamp <= GetTime() and self.GetDistance(ENTLIST[1]) < 384:
                pos_p = pygame.Vector2(ENTLIST[1].rect.center)
                pos_m = pygame.Vector2(self.rect.center)

                ang = (pos_p - pos_m)
                ang = ang.normalize()

                niga = Projectile(pos_m, ang)

                self.shot_timestamp = GetTime() + 0.5

    def GetKillList(self):
        global ENTLIST
        return ENTLIST
    
    def Kill(self):
        global ENTLIST,sound
        sound[0].PlayEnemyDeath()
        if self.dead:
            return

        self.dead = True

        arr = self.GetKillList()
        arr.pop(arr.index(self))

        print("Killed entity:", self.name, "id:", self.id, "!!!")

        file = open("assets\\loadlvl.txt")
        lvlname = int(file.readline())
        lvlname += 1
        file.close()
        file = open("assets\\loadlvl.txt","w")
        file.write(str(lvlname))
        file.close()

        del self
        
        return True

class Projectile(Entity):
    def __init__(self, pos, ang):
        super().__init__()
        global lvlname
        sound[0].PlayShot()
        self.image = pygame.image.load("assets\\bullet\\Ball.png")
        if int(lvlname) == 2:
            self.img_path = "assets\\enemy\\ghost\\ghost_ball.gif"
            self.image = pygame.image.load(self.img_path)
            self.image = pygame.transform.scale(self.image,(96,96))
        elif int(lvlname) == 3:
            self.img_path = "assets\\enemy\\god\\god_bullet.png"
            self.image = pygame.image.load(self.img_path)
            

        self.name = "projectile"

        self.width = 60
        self.height = 60

        self.pos = pos
        self.angle = ang

        self.GenRect()
        self.AddToList()


    def HandleInteraction(self, other) -> bool:
        if other == self:
            return False
        
        if type(other) == Boss:
            return False

        if other.name == "projectile":
            return False
        
        if other.name == "boolet":
            return False

        other.health -= 10
        self.Kill()
        return False

    def ShouldCollide(self):
        return True

    def Update(self):
        if self.CheckCollision():
            self.DrawBBOX()
            return

        self.rect.center += self.angle * 1.5 * GetDTTime()

        # print("zijem", self.id)

        self.RenderObject()

    
         
class Sounds():
    def __init__(self):
        global sound
        self.shot = mixer.Sound("assets\\sounds\\cast_magic.mp3") 
        self.enemy_death = mixer.Sound("assets\\sounds\\goblin_death.mp3")
        self.enemy_attack = mixer.Sound("assets\\sounds\\attack.mp3")
        self.walking = mixer.Sound("assets\\sounds\\walk.mp3")
        self.running = mixer.Sound("assets\\sounds\\run.mp3")
        self.death = mixer.Sound("assets\\sounds\\static.mp3")
        sound.append(self)
        self.timestamp1 = 0
        self.timestamp2 = 0
        self.timestamp3 = 0
        self.timestamp4 = 0
        self.timestamp5 = 0
        self.timestamp6 = 0

    def SetVolume(self):
        global volume
        self.shot.set_volume(volume[0]/100)
        self.enemy_death.set_volume(volume[0]/100)
        self.enemy_attack.set_volume(volume[0]/100)
        self.running.set_volume(volume[0]/100)
        self.walking.set_volume(volume[0]/100)
        self.death.set_volume(volume[0]/100)

    def PlayShot(self):
        if self.timestamp1 + 0.3 < GetTime(): 
            self.shot.play()
            self.timestamp1 = GetTime()

    def PlayEnemyDeath(self):
        if self.timestamp2 + 0.3 < GetTime(): 
            self.enemy_death.play()
            self.timestamp2 = GetTime()

    def PlayWalking(self):
        if self.timestamp3 + 0.2 < GetTime(): 
            self.walking.play()
            self.timestamp3 = GetTime()

    def PlayRunning(self):
        if self.timestamp4 + 0.2 < GetTime(): 
            self.running.play()
            self.timestamp4 = GetTime()

    def PlayEnemyAttack(self):
        if self.timestamp5 + 0.3 < GetTime(): 
            self.enemy_attack.play()
            self.timestamp5 = GetTime()

    def PlayDeath(self):
        if self.timestamp6 + 0.3 < GetTime(): 
            self.death.play()
            self.timestamp6 = GetTime()

    def Kill(self):
        del self


    

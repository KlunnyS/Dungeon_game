import basedef
from basedef import *

class Buttons():
    def __init__(self,path:str,posx:float,posy:float,width:float = None,height:float = None): 
        self.width_now = 256
        self.height_now = 256
        self.button_image = pygame.image.load(path)
        self.posx = posx
        self.posy = posy
        if width == None: self.width = 139
        else: self.width = width
        if height == None: self.height = 43
        else: self.height = height
        self.pos = [round(self.posx - self.width / 2), round(self.posy - self.height / 2)]
        self.rect = pygame.rect.Rect(self.pos[0],self.pos[1],self.width,self.height)

    def center(self):
        width_current = screen.get_width()
        height_current = screen.get_height()

        center_org_x = self.width_now
        center_org_y = self.height_now

        center_x = width_current / 2
        center_y = height_current / 2

        centerx_now = center_x - center_org_x
        centery_now = center_y - center_org_y

        self.rect.move_ip(centerx_now,centery_now)

        self.width_now = center_x
        self.height_now = center_y
        
class TextInput:
    def __init__(self):
        self.font = pygame.font.Font(None,32)
        self.text = ''
        self.color_passive = pygame.Color('gray15')
        self.color_active = pygame.Color('lightskyblue3')
        self.color = self.color_passive
        self.active = False
        
    def renderText(self):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive

        self.comm_line = pygame.Rect(15,screen.get_height()-45,screen.get_width()/3,32)
        self.bg = pygame.Rect(15,screen.get_height()-45,screen.get_width()/3,32)
        pygame.draw.rect(screen,(255,255,255),self.bg,0)
        pygame.draw.rect(screen,self.color,self.comm_line,2)
        text_surface = self.font.render(self.text,True,(0,0,0))
        screen.blit(text_surface,(20,screen.get_height()-40)) 
        self.comm_line.w = max(100,text_surface.get_width() + 10)

play = Buttons('assets\\menu\\button_play.png',256,128)
continueB = Buttons('assets\\menu\\button_continue.png',256,128)
new_game = Buttons('assets\\menu\\button_New_game.png',256,192)
levelB = Buttons('assets\\menu\\button_level.png',256,256)
B1 = Buttons('assets\\menu\\button_1.png',256,326,70,70)
B2 = Buttons('assets\\menu\\button_2.png',256,401,70,70) #216
B3 = Buttons('assets\\menu\\button_3.png',256,476,70,70) #296
B4 = Buttons('assets\\menu\\button_4.png',216,476,70,70)
B5 = Buttons('assets\\menu\\button_5.png',296,476,70,70)
quit = Buttons('assets\\menu\\button_quit.png',256,384)
settings = Buttons('assets\\menu\\button_settings.png',256,256)
sett_back = Buttons('assets\\menu\\button_back.png',100,50)
res = Buttons('assets\\menu\\button_resolution.png',100,100)
res_512 = Buttons('assets\\menu\\button_512x512.png',250,150)
res_1024 = Buttons('assets\\menu\\button_1024x1024.png',250,200)
res_1280 = Buttons('assets\\menu\\button_1280x720.png',250,250)
volumeB = Buttons('assets\\menu\\button_volume.png',100,150)
plus = Buttons('assets\\menu\\button_plus.png',100,200)
minus = Buttons('assets\\menu\\button_minus.png',294,200)
txtin = TextInput()

class MainMenu():
    def __init__(self):
        self.width_now = 256
        self.height_now = 256
        self.buttons = [volumeB,plus,minus,play,continueB,new_game,levelB,B1,B2,B3,B4,B5,quit,settings,sett_back,res,res_512,res_1024,res_1280]
        self.menu = True
        self.settings = False
        self.play = False
        self.background = pygame.image.load('assets\\menu\\menu_v2.png')
        self.surf = pygame.Surface((screen.get_width(),screen.get_height()))
        self.surf.fill((73, 6, 72))
        self.surf.set_alpha(128)
        self.button_overlay = pygame.Surface((139,43))
        self.button_overlay.fill((255,255,255))
        self.button_overlay.set_alpha(32)
        self.lvl_button_overlay = pygame.Surface((70,70))
        self.lvl_button_overlay.fill((255,255,255))
        self.lvl_button_overlay.set_alpha(32)
        self.show_res = False
        self.font = pygame.font.Font(None,40)
        self.text = self.font.render(str(screen.get_width())+" X "+str(screen.get_height()),True,(0,0,0))
        self.text_pos = (180,100)
        self.text_rect = self.text.get_rect()
        self.time_elapsed_FS = None
        self.time_FS = None
        self.can_FS = None
        self.show_lvls = False
        self.show_vol = False
        self.show_comm_line = False

    def screen_size(self):
        global mode
        key = pygame.key.get_pressed()

        if self.can_FS == False:
            self.time_elapsed_FS = t.time() - self.time_FS

        if self.time_elapsed_FS == None or self.time_elapsed_FS >= 1:
            self.can_FS = True

        if key[pygame.K_F11] and self.can_FS == True:
            if mode[0] == pygame.RESIZABLE:
                mode[0] = pygame.FULLSCREEN
                pygame.display.set_mode((screen.get_width(),screen.get_height()),mode[0])
                self.can_FS = False
                self.time_FS = t.time()
                self.CenterStuff()

            elif mode[0] == pygame.FULLSCREEN:
                mode[0] = pygame.RESIZABLE
                pygame.display.set_mode((screen.get_width(),screen.get_height()),mode[0])
                self.can_FS = False
                self.time_FS = t.time()
                self.CenterStuff()

    def load(self): 
        global volume,mode
        settings = []
        res = False
        vol = False
        file = open("settings.txt","r")
        for i in file:
            if res == True:
                width,height,mode_ = i.split()
                resolution = (int(width),int(height))
                if mode_ == "resize":
                    mode_ = pygame.RESIZABLE
                elif mode_ == "full":
                    mode_ = pygame.FULLSCREEN
                else:
                    mode_ = pygame.FULLSCREEN
                pygame.display.set_mode(resolution,mode_)
                mode[0] = mode_
                res = False

            if vol:
                volume[0] = int(i.strip())
                vol = False

            if i.strip() == "Resolution":
                res = True

            if i.strip() == "VOL":
                vol = True

        self.CenterStuff()
        file.close()

    def UpdateText(self):
        if self.show_res == True:
            self.text = self.font.render(str(screen.get_width())+" X "+str(screen.get_height()),True,(0,0,0))
            self.text_pos = (res_512.rect.topleft[0],res_512.rect.topleft[1]-40)
        elif self.show_vol == True:
            self.text = self.font.render(str(volume[0]),True,(0,0,0))
            self.text_pos = (plus.rect.topleft[0]+144,plus.rect.topleft[1]+10)

    def CenterText(self):
        self.UpdateText()
        width_current = screen.get_width()
        height_current = screen.get_height()

        center_org_x = self.width_now
        center_org_y = self.height_now

        center_x = width_current / 2
        center_y = height_current / 2

        centerx_now = center_x - center_org_x
        centery_now = center_y - center_org_y

        self.text_rect = (centerx_now,centery_now)

        self.width_now = center_x
        self.height_now = center_y       

    def CenterStuff(self):
        for i in self.buttons:
            i.center()
        self.CenterText()
        self.background = pygame.transform.scale(self.background,(screen.get_width(),screen.get_height()))
        self.surf = pygame.transform.scale(self.surf,(screen.get_width(),screen.get_height()))
    
    def save(self):
        global mode
        mode_save = "resize"
        if mode[0] == pygame.FULLSCREEN: mode_save = "full"
        RESOLUTION = (screen.get_width(),screen.get_height())
        file = open("settings.txt","w")
        file.write("VOL\n"+str(volume[0])+"\n")
        file.write("Resolution\n")
        file.write(str(RESOLUTION[0])+" "+str(RESOLUTION[1])+" "+mode_save)
        file.close()

    def MenuLoop(self):
        while self.menu:
            self.screen_size()
            key = pygame.key.get_pressed()
            screen.fill((73, 6, 72))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu = False
                    self.save()
                    pygame.quit()
                    os._exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play.rect.collidepoint(pygame.mouse.get_pos()):
                            self.play = True
                            self.menu = False
                            return self.PlayLoop()
                        if quit.rect.collidepoint(pygame.mouse.get_pos()):
                            self.menu = False
                            self.save()
                            pygame.quit()
                            os._exit(0)
                        if settings.rect.collidepoint(pygame.mouse.get_pos()):
                            self.settings = True
                            self.menu = False
                            self.SettingsLoop()

                if event.type == pygame.VIDEORESIZE:
                    self.CenterStuff()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.settings = True
                        self.menu = False
                        self.SettingsLoop()

            screen.blit(self.background,(0,0))
            screen.blit(self.surf,(0,0))
            screen.blit(play.button_image,play.rect.topleft)
            screen.blit(quit.button_image,quit.rect.topleft)
            screen.blit(settings.button_image,settings.rect.topleft)

            if play.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,play.rect.topleft)
            if settings.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,settings.rect.topleft)
            if quit.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,quit.rect.topleft)

            pygame.display.update()    

    def SettingsLoop(self):
        global volume
        self.show_res = False
        while self.settings:
            self.screen_size()
            key = pygame.key.get_pressed()
            screen.fill((73, 6, 72))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu = False
                    self.save()
                    pygame.quit()
                    os._exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if sett_back.rect.collidepoint(pygame.mouse.get_pos()):
                            self.menu = True
                            self.settings = False
                            self.save()
                            self.MenuLoop()
                        if res.rect.collidepoint(pygame.mouse.get_pos()):
                            if self.show_res == False:   
                                self.show_res = True
                                self.UpdateText()
                                self.CenterText()
                            else: 
                                self.show_res = False
                            if self.show_vol == True:
                                self.show_vol = False
                                self.UpdateText()
                                self.CenterText()

                        if volumeB.rect.collidepoint(pygame.mouse.get_pos()):
                            if self.show_vol == False:   
                                self.show_vol = True
                                self.UpdateText()
                                self.CenterText()
                            else: 
                                self.show_vol = False
                            if self.show_res == True:
                                self.show_res = False
                                self.UpdateText()
                                self.CenterText()

                        if self.show_res:
                            if res_512.rect.collidepoint(pygame.mouse.get_pos()):
                                pygame.display.set_mode((512,512),mode[0])
                                self.CenterStuff()
                            if res_1024.rect.collidepoint(pygame.mouse.get_pos()):
                                pygame.display.set_mode((1024,1024),mode[0])
                                self.CenterStuff()
                            if res_1280.rect.collidepoint(pygame.mouse.get_pos()):
                                pygame.display.set_mode((1280,720),mode[0])
                                self.CenterStuff()
                        if self.show_vol:
                            if plus.rect.collidepoint(pygame.mouse.get_pos()):
                                if volume[0] < 100:
                                    volume[0] += 5
                                    self.UpdateText()
                            if minus.rect.collidepoint(pygame.mouse.get_pos()):
                                if volume[0] > 0:
                                    volume[0] -= 5
                                    self.UpdateText()

                if event.type == pygame.VIDEORESIZE:
                    self.CenterStuff()
                    self.CenterText()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu = True
                        self.settings = False
                        self.save()
                        self.MenuLoop()

            screen.blit(self.background,(0,0))
            screen.blit(self.surf,(0,0))
            screen.blit(sett_back.button_image,sett_back.rect.topleft)
            screen.blit(res.button_image,res.rect.topleft)
            screen.blit(volumeB.button_image,volumeB.rect.topleft)

            if sett_back.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,sett_back.rect.topleft)
            if res.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,res.rect.topleft)
            if volumeB.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,volumeB.rect.topleft)

            if self.show_res:
                screen.blit(self.text,self.text_pos)
                screen.blit(res_512.button_image,res_512.rect.topleft)
                screen.blit(res_1024.button_image,res_1024.rect.topleft)
                screen.blit(res_1280.button_image,res_1280.rect.topleft)
                if res_512.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.button_overlay,res_512.rect.topleft)
                if res_1024.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.button_overlay,res_1024.rect.topleft)
                if res_1280.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.button_overlay,res_1280.rect.topleft)

            if self.show_vol:
                screen.blit(plus.button_image,plus.rect.topleft)
                screen.blit(minus.button_image,minus.rect.topleft)
                screen.blit(self.text,self.text_pos)
                if plus.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.button_overlay,plus.rect.topleft)
                if minus.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.button_overlay,minus.rect.topleft)

            pygame.display.update()    
    
    def PlayLoop(self):
        lvl = 1
        while self.play:
            self.screen_size()
            key = pygame.key.get_pressed()
            screen.fill((73, 6, 72))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu = False
                    self.save()
                    pygame.quit()
                    os._exit(0)

                if self.show_lvls:
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_F9 and self.show_comm_line == False:
                            self.show_comm_line = True
                            txtin.active =True
                        if txtin.active:        
                            if self.show_comm_line == True:
                                if event.key == pygame.K_BACKSPACE:
                                    txtin.text = txtin.text[:-1]    
                                else:    
                                    txtin.text += event.unicode
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            lvl = txtin.text.strip()  
                            if os.path.exists("assets"+"\\"+lvl+".txt"):   
                                self.save()
                                self.play = False
                                if lvl == "level" or lvl == "level1" or lvl == "level2" or lvl == "level3":
                                    if lvl == "level":
                                        lvl = "0"
                                    lvl = lvl.replace("level", "")
                                    print(lvl)
                                file = open("assets\\loadlvl.txt","w")
                                file.write(str(lvl))
                                file.close()
                                return False
                            else:
                                print("File not found")


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if sett_back.rect.collidepoint(pygame.mouse.get_pos()):
                            self.menu = True
                            self.settings = False
                            self.save()
                            self.MenuLoop()  
                        if continueB.rect.collidepoint(pygame.mouse.get_pos()):
                            self.save()
                            pygame.display.set_mode((512,512),pygame.RESIZABLE)
                            self.play = False
                            return True
                        if new_game.rect.collidepoint(pygame.mouse.get_pos()):
                            self.save()
                            pygame.display.set_mode((512,512),pygame.RESIZABLE)
                            self.play = False
                            return False
                        if levelB.rect.collidepoint(pygame.mouse.get_pos()):
                            if self.show_lvls == False:   
                                self.show_lvls = True
                            else: 
                                self.show_lvls = False   
                        if self.show_lvls:
                            if B1.rect.collidepoint(pygame.mouse.get_pos()):
                                lvl = 1  
                                self.save()
                                pygame.display.set_mode((512,512),pygame.RESIZABLE)
                                self.play = False
                                file = open("assets\\loadlvl.txt","w")
                                file.write(str(lvl))
                                file.close()
                            if B2.rect.collidepoint(pygame.mouse.get_pos()):
                                lvl = 2 
                                self.save()
                                pygame.display.set_mode((512,512),pygame.RESIZABLE)
                                self.play = False
                                file = open("assets\\loadlvl.txt","w")
                                file.write(str(lvl))
                                file.close()
                            if B3.rect.collidepoint(pygame.mouse.get_pos()):
                                lvl = 3 
                                self.save()
                                pygame.display.set_mode((512,512),pygame.RESIZABLE)
                                self.play = False
                                file = open("assets\\loadlvl.txt","w")
                                file.write(str(lvl))
                                file.close()
                            if self.show_comm_line and txtin.bg.collidepoint(pygame.mouse.get_pos()):
                                txtin.active = True
                            elif self.show_comm_line and not txtin.bg.collidepoint(pygame.mouse.get_pos()):
                                txtin.active = False
                            

                if event.type == pygame.VIDEORESIZE:
                    self.CenterStuff()
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu = True
                        self.settings = False
                        self.save()
                        self.MenuLoop()  

            screen.blit(self.background,(0,0))
            screen.blit(self.surf,(0,0))
            screen.blit(sett_back.button_image,sett_back.rect.topleft)
            screen.blit(continueB.button_image,continueB.rect.topleft)
            screen.blit(new_game.button_image,new_game.rect.topleft)
            screen.blit(levelB.button_image,levelB.rect.topleft)
            if sett_back.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,sett_back.rect.topleft)
            if continueB.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,continueB.rect.topleft)
            if new_game.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,new_game.rect.topleft)
            if levelB.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,levelB.rect.topleft)

            if self.show_lvls:
                screen.blit(B1.button_image,B1.rect.topleft)
                screen.blit(B2.button_image,B2.rect.topleft)
                screen.blit(B3.button_image,B3.rect.topleft)
                # screen.blit(B4.button_image,B4.rect.topleft)
                # screen.blit(B5.button_image,B5.rect.topleft)
                if B1.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.lvl_button_overlay,B1.rect.topleft)
                if B2.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.lvl_button_overlay,B2.rect.topleft)
                if B3.rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(self.lvl_button_overlay,B3.rect.topleft)
            
                if self.show_comm_line:
                    txtin.renderText()

            pygame.display.update()   
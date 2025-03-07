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

continueB = Buttons('assets\\menu\\button_resume.png',256,128)
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

class PauseMenu_():
    def __init__(self):
        self.width_now = 256
        self.height_now = 256 
        self.buttons = [volumeB,plus,minus,continueB,quit,settings,sett_back,res,res_512,res_1024,res_1280]
        self.time_elapsed_pause = None
        self.time_pause = None
        self.can_pause = None
        self.paused = False
        self.pauseSurf = pygame.surface.Surface((screen.get_width(),screen.get_height()))
        self.pauseSurf.fill((255,255,255))
        self.pauseSurf.set_alpha(128)
        self.button_overlay = pygame.Surface((139,43))
        self.button_overlay.fill((255,255,255))
        self.button_overlay.set_alpha(32)
        self.settings = False
        self.font = pygame.font.Font(None,40)
        self.text = self.font.render(str(screen.get_width())+" X "+str(screen.get_height()),True,(0,0,0))
        self.text_pos = (180,100)
        self.text_rect = self.text.get_rect()
        self.show_res = False
        self.show_vol = False
        self.hint = self.font.render("Interact with \"E\"\nShoot with \"LMB\"",True,(0,0,0))

    def load(self): 
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
        self.pauseSurf = pygame.transform.scale(self.pauseSurf,(screen.get_width(),screen.get_height()))

    def PauseMenuToggle(self): 
        key = pygame.key.get_pressed()

        if self.can_pause == False:
            self.time_elapsed_pause = t.time() - self.time_pause

        if self.time_elapsed_pause == None or self.time_elapsed_pause >= 0.25:
            self.can_pause = True

        if key[pygame.K_ESCAPE] and self.can_pause == True:
            if self.paused == False:
                self.paused = True
                self.can_pause = False
                self.time_pause = t.time()

            else: 
                self.paused = False  
                self.save()
                self.can_pause = False
                self.time_pause = t.time()

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

    def PauseMenuEvent(self,event):
        global volume
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.settings == False:    
                    if continueB.rect.collidepoint(pygame.mouse.get_pos()):
                        self.save()
                        self.paused = False
                    if quit.rect.collidepoint(pygame.mouse.get_pos()):
                        self.menu = False
                        pygame.quit()
                        os._exit(0)
                    if settings.rect.collidepoint(pygame.mouse.get_pos()):
                        self.settings = True

                if self.settings == True:
                    if sett_back.rect.collidepoint(pygame.mouse.get_pos()):
                        self.settings = False
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
                            self.save()
                            pygame.display.set_mode((512,512),mode[0])
                            self.CenterStuff()
                        if res_1024.rect.collidepoint(pygame.mouse.get_pos()):
                            self.save()
                            pygame.display.set_mode((1024,1024),mode[0])
                            self.CenterStuff()
                        if res_1280.rect.collidepoint(pygame.mouse.get_pos()):
                            self.save()
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

        
                

    def PauseMenuRender(self):

        if self.settings:
            screen.blit(self.pauseSurf,(0,0))
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

        else:
            
            screen.blit(self.pauseSurf,(0,0))
            screen.blit(continueB.button_image,continueB.rect.topleft)
            screen.blit(quit.button_image,quit.rect.topleft)
            screen.blit(settings.button_image,settings.rect.topleft)
            screen.blit(self.hint,(20,screen.get_height()-100))
            if continueB.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,continueB.rect.topleft)
            if settings.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,settings.rect.topleft)
            if quit.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(self.button_overlay,quit.rect.topleft)

import pygmi, pygame, os, sys, math
from pygame.locals import *

class Button(pygmi.Object):

    def __init__(self,spriteunlit,spritelit,x,y):
        self.spriteunlit = spriteunlit
        self.spritelit = spritelit
        super().__init__(self.spriteunlit,x,y)

    def mouseOver(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        if self.mouseX >= self.x and self.mouseX <= self.x+self.sprite.w and self.mouseY >= self.y and self.mouseY <= self.y+self.sprite.h:
            return True
        else:
            return False

    def event_pressed(self):
        pass

    def update(self):
        if self.mouseOver() == True:
            self.setSprite(self.spritelit)
            if pygame.mouse.get_pressed() == (True, False, False):
                self.event_pressed()
        if self.mouseOver() == False:
            self.setSprite(self.spriteunlit)

class PlayButton(Button):

    def __init__(self,x,y,game):
        self.sprPlay = pygmi.Sprite("img/hud/play.png",0,0,64,30)
        self.sprPlayLit = pygmi.Sprite("img/hud/playlit.png",0,0,64,30)
        self.game = game
        super().__init__(self.sprPlay,self.sprPlayLit,x,y)

    def event_pressed(self):
        self.game.gotoRoom("street")

    def update(self):
        super().update()

class QuitButton(Button):

    def __init__(self,x,y,game):
        self.sprQuit = pygmi.Sprite("img/hud/quit.png",0,0,64,30)
        self.sprQuitLit = pygmi.Sprite("img/hud/quitlit.png",0,0,64,30)
        self.game = game
        super().__init__(self.sprQuit,self.sprQuitLit,x,y)

    def event_pressed(self):
        self.game.quit()

    def update(self):
        super().update()
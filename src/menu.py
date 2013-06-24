import pygmi, pygame, os, sys, math
from pygame.locals import *

class Button(pygmi.Object):

    def __init__(self,x,y):
        super().__init__(x,y)

    def event_create(self,spriteunlit,spritelit):
        self.spriteunlit = spriteunlit
        self.spritelit = spritelit
        self.setSprite(self.spriteunlit)

    # The buttons are being added to the room (sprites and objects - even their positions - exist), but this code does not work
    def mouseOver(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        if self.mouseX >= self.x and self.mouseX <= self.x+self.sprite.w and self.mouseY >= self.y and self.mouseY <= self.y+self.sprite.h:
            return True
        else:
            return False

    # I don't think this is needed.
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
        self.game = game
        super().__init__(x,y)

    def event_create(self):
        self.sprPlay = pygmi.Sprite(self.assets.images["hud"]["play.png"],0,0,64,30)
        self.sprPlayLit = pygmi.Sprite(self.assets.images["hud"]["playlit.png"],0,0,64,30)
        super().event_create(self.sprPlay,self.sprPlayLit)

    def event_pressed(self):
        self.game.gotoRoom("street")

    def update(self):
        super().update()

class QuitButton(Button):

    def __init__(self,x,y,game):
        self.game = game
        super().__init__(x,y)

    def event_create(self):
        self.sprQuit = pygmi.Sprite(self.assets.images["hud"]["quit.png"],0,0,64,30)
        self.sprQuitLit = pygmi.Sprite(self.assets.images["hud"]["quitlit.png"],0,0,64,30)
        super().event_create(self.sprQuit,self.sprQuitLit)

    def event_pressed(self):
        self.game.quit()

    def update(self):
        super().update()
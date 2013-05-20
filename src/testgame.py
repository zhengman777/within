'''
Created on May 12, 2013

@author: Catt
'''
import pygmi, pygame, os, sys
from pygame.locals import *

class Button(pygmi.Object):

    def mouseOver(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        if self.mouseX >= self.x and self.mouseX <= self.x+self.sprite.w and self.mouseY >= self.y and self.mouseY <= self.y+self.sprite.h:
            return True
        else:
            return False

class PlayButton(Button):

    def __init__(self,x,y):
        self.sprPlay = pygmi.Sprite("img/hud/play.png",0,0,64,30)
        self.sprPlayLit = pygmi.Sprite("img/hud/playlit.png",0,0,64,30)
        super().__init__(self.sprPlay,x,y)

    def update(self):
        if self.mouseOver() == True:
            self.setSprite(self.sprPlayLit)
            if pygame.mouse.get_pressed() == (True, False, False):
                game.gotoRoom("combat")
        if self.mouseOver() == False:
            self.setSprite(self.sprPlay)

class QuitButton(Button):

    def __init__(self,x,y):
        self.sprQuit = pygmi.Sprite("img/hud/quit.png",0,0,64,30)
        self.sprQuitLit = pygmi.Sprite("img/hud/quitlit.png",0,0,64,30)
        super().__init__(self.sprQuit,x,y)

    def update(self):
        if oQuit.mouseOver() == True:
            oQuit.setSprite(self.sprQuitLit)
            if pygame.mouse.get_pressed() == (True, False, False):
                pygame.quit()
                sys.exit()
        if oQuit.mouseOver() == False:
            oQuit.setSprite(self.sprQuit)

class Background(pygmi.Object):

    def __init__(self,x,y,room):
        self.bgMainMenu = pygmi.Sprite("img/bg/title.png",0,0,800,600)
        self.setSolid(False)
        if room == mainmenu:
            super().__init__(self.bgMainMenu,x,y)

class Character(pygmi.Object):

    def __init__(self,x,y):
        self.xSpeed = 0
        self.ySpeed = 0
        sprBoy = pygmi.Sprite("img/char/boy_akick",0,0,64,64)
        sprBoy.setFrameTime(30)
        super().__init__(sprBoy,x,y)

    def event_keyDown(self,key):
        if key == K_w:
            self.ySpeed = -4
        elif key == K_s:
            self.ySpeed = 4
        if key == K_a:
            self.xSpeed = -4
        elif key == K_d:
            self.xSpeed = 4

    def event_collision(self,other):
        print("Ouch!")

    def update(self):
        keys = pygame.key.get_pressed()
        if not (keys[K_a] or keys[K_d]):
            self.xSpeed = 0
        if not (keys[K_w] or keys[K_s]):
            self.ySpeed = 0

        self.x += self.xSpeed
        self.y += self.ySpeed

class Ball(pygmi.Object):

    def __repr__(self):
        return "ball"
    def __init__(self,x,y):
        random.seed()
        self.xSpeed = random.randint(0,4)
        self.ySpeed = random.randint(0,4)
        sprBall = pygmi.Sprite("img/enemies/apathol_spawn/apathol_spawn_03.png",-32,-32,64,64)
        sprBall.setFrameTime(1)
        super().__init__(sprBall,x,y)

    def event_collision(self,other):

        if(bool(random.getrandbits(1))):
            self.xSpeed *= -1
        else:
            self.ySpeed *= -1

    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.x > x_dim or self.x < 0:
            self.xSpeed *= -1
        if self.y > y_dim or self.y < 0:
            self.ySpeed *= -1

        if random.randint(0,100) > 99:
            self.destroy()



if __name__ == '__main__':
    x_dim = 800
    y_dim = 600
    game = pygmi.Pygmi((x_dim,y_dim), "Test Game", 0)
    oBoy = Character(100,100)
    oPlay = PlayButton(x_dim-64,y_dim-60)
    oQuit = QuitButton(x_dim-64,y_dim-30)
    mainmenu = pygmi.Room("mainmenu",x_dim,y_dim)
    combat = pygmi.Room("combat",x_dim,y_dim)
    bgMainMenu = Background(0,0,mainmenu)
    mainmenu.addToRoom(bgMainMenu)
    mainmenu.addToRoom(oBoy)
    mainmenu.addToRoom(oPlay)
    mainmenu.addToRoom(oQuit)
    game.addRoom(mainmenu)
    game.addRoom(combat)
    game.gotoRoom("mainmenu")


    while(True):
        #update
        game.update()
        #render
        game.render()

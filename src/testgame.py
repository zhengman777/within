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
                game.gotoRoom("street")
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
        self.bgStreet = pygmi.Sprite("img/bg/street.png",0,0,800,600)
        self.setSolid(False)
        if room == mainmenu:
            super().__init__(self.bgMainMenu,x,y)
        if room == street:
            super().__init__(self.bgStreet,x,y)

class Character(pygmi.Object):

    def __init__(self,x,y):
        self.xSpeed = 0
        self.ySpeed = 0
        self.runModifier = 1
        self.dominantX = 0
        self.dominantY = 0
        self.running = 0
        self.listRunClock = [0, 0, 0, 0]
        sprBoyIdle = pygmi.Sprite("img/char/boy_idle",0,0,64,64)
        sprBoyIdle.setFrameTime(30)
        sprBoyWalk = pygmi.Sprite("img/char/boy_walk",0,0,64,66)
        sprBoyWalk.setFrameTime(8)
        sprBoyRun = pygmi.Sprite("img/char/boy_run",0,0,64,70)
        sprBoyRun.setFrameTime(5)
        self.boy = {'idle':sprBoyIdle,'walk':sprBoyWalk,'run':sprBoyRun}
        super().__init__(sprBoyIdle,x,y)

    def event_keyDown(self,key):
        if key == K_w:
            self.dominantY = 1
            if self.listRunClock[0] > 0:
                self.running = 1
                self.runModifier = 1.5
                self.listRunClock[0:3] = [0]*4
        if key == K_s:
            self.dominantY = 2
            if self.listRunClock[1] > 0:
                self.running = 1
                self.runModifier = 1.5
                self.listRunClock[0:3] = [0]*4
        if key == K_a:
            self.dominantX = 1
            if self.listRunClock[2] > 0:
                self.running = 1
                self.runModifier = 1.5
                self.listRunClock[0:3] = [0]*4
        if key == K_d:
            self.dominantX = 2
            if self.listRunClock[3] > 0:
                self.running = 1
                self.runModifier = 1.5
                self.listRunClock[0:3] = [0]*4
        if key == K_w and self.dominantY != 2:
            self.ySpeed = -2
            if self.running == 1:
                self.setSprite(self.boy['run'])
                self.boy['run'].index = 0
            elif self.running == 0:
                self.setSprite(self.boy['walk'])
                self.boy['walk'].index = 0
        if key == K_s and self.dominantY != 1:
            self.ySpeed = 2
            if self.running == 1:
                self.setSprite(self.boy['run'])
                self.boy['run'].index = 0
            elif self.running == 0:
                self.setSprite(self.boy['walk'])
                self.boy['walk'].index = 0
        if key == K_a and self.dominantX != 2:
            self.xSpeed = -3
            for key, value in self.boy.items():
                self.boy[key].setFlipped(1,0)
            if self.running == 1:
                self.setSprite(self.boy['run'])
                self.boy['run'].index = 0
            elif self.running == 0:
                self.setSprite(self.boy['walk'])
                self.boy['walk'].index = 0
        if key == K_d and self.dominantX != 1:
            self.xSpeed = 3
            for key, value in self.boy.items():
                self.boy[key].setFlipped(0,0)
            if self.running == 1:
                self.setSprite(self.boy['run'])
                self.boy['run'].index = 0
            elif self.running == 0:
                self.setSprite(self.boy['walk'])
                self.index = 0

    def event_keyUp(self,key):
        if key == K_w:
            self.dominantY = 0
            self.listRunClock[0] = 10
        if key == K_s:
            self.dominantY = 0
            self.listRunClock[1] = 10
        if key == K_a:
            self.dominantX = 0
            self.listRunClock[2] = 10
        if key == K_d:
            self.dominantX = 0
            self.listRunClock[3] = 10

    def event_collision(self,other):
        print("Ouch!")

    def update(self):
        keys = pygame.key.get_pressed()
        if not (keys[K_a] or keys[K_d] or keys[K_w] or keys[K_s]):
            self.runModifier = 1
        if self.dominantX == 0:
            self.xSpeed = 0
        if self.dominantY == 0:
            self.ySpeed = 0
        if self.xSpeed == 0 and self.ySpeed == 0:
            self.setSprite(self.boy['idle'])
            self.running = 0
        for i in range(0,len(self.listRunClock)):
            if self.listRunClock[i] > 0:
                self.listRunClock[i] -= 1
        self.x += self.xSpeed*self.runModifier
        self.y += self.ySpeed*self.runModifier

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
    oBoy = Character(100,400)
    oPlay = PlayButton(x_dim-64,y_dim-60)
    oQuit = QuitButton(x_dim-64,y_dim-30)
    mainmenu = pygmi.Room("mainmenu",x_dim,y_dim)
    street = pygmi.Room("street",1200,y_dim)
    bgMainMenu = Background(0,0,mainmenu)
    mainmenu.addToRoom(bgMainMenu)
    mainmenu.addToRoom(oPlay)
    mainmenu.addToRoom(oQuit)
    game.addRoom(mainmenu)
    bgStreet = Background(0,0,street)
    street.addToRoom(bgStreet)
    street.addToRoom(oBoy)
    game.addRoom(street)
    game.gotoRoom("mainmenu")


    while(True):
        #update
        game.update()
        #render
        game.render()

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
                game.quit()
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

class Shadow(pygmi.Object):

    def __init__(self,x,y,size):
        self.size = size
        self.sprShadowM = pygmi.Sprite("img/fx/shadowM.png",0,0,64,30)
        self.setSolid(False)
        self.sprShadowM.image.set_alpha(100)
        if self.size == "medium":
            super().__init__(self.sprShadowM,x,y)

class Character(pygmi.Object):

    def __init__(self,x,y,shadow):
        self.shadow = shadow
        self.xSpeed = 0
        self.ySpeed = 0
        self.z = y
        self.xDashSpeed = 0
        self.yDashSpeed = 0
        self.runModifier = 1
        self.dominantX = 0
        self.dominantY = 0
        self.running = 0
        self.listRunClock = [0, 0, 0, 0]
        self.attacking = 0
        self.moving = 0
        self.airborne = 0
        self.jumpRelease = 0
        self.jumpSpeed = 0
        self.maxJumpSpeed = 5
        self.gravity = .4
        self.punch1Anim = 0
        self.punch2Anim = 0
        self.kickAnim = 0
        self.datkAnim = 0
        sprBoyIdle = pygmi.Sprite("img/char/boy_idle",-18,-64,30,64)
        sprBoyIdle.setFrameTime(30)
        sprBoyWalk = pygmi.Sprite("img/char/boy_walk",-18,-66,64,66)
        sprBoyWalk.setFrameTime(8)
        sprBoyRun = pygmi.Sprite("img/char/boy_run",-22,-70,44,68)
        sprBoyRun.setFrameTime(5)
        sprBoyPunch1 = pygmi.Sprite("img/char/boy_punch1",-18,-64,40,64)
        sprBoyPunch1.setFrameTime(2)
        sprBoyPunch2 = pygmi.Sprite("img/char/boy_punch2",-20,-64,38,64)
        sprBoyPunch2.setFrameTime(2)
        sprBoyKick = pygmi.Sprite("img/char/boy_kick",-18,-64,40,64)
        sprBoyKick.setFrameTime(2)
        sprBoyDatk = pygmi.Sprite("img/char/boy_datk",-20,-66,40,64)
        sprBoyDatk.setFrameTime(3)
        sprBoyJump = pygmi.Sprite("img/char/boy_jump",-18,-66,32,66)
        sprBoyJump.setFrameTime(2)
        sprBoyLand = pygmi.Sprite("img/char/boy_land.png",-16,-66,30,66)
        self.boy = {'idle':sprBoyIdle,'walk':sprBoyWalk,'run':sprBoyRun,'punch1':sprBoyPunch1,
                    'punch2':sprBoyPunch2,'kick':sprBoyKick,'datk':sprBoyDatk,'jump':sprBoyJump,
                    'land':sprBoyLand}
        super().__init__(sprBoyIdle,x,y)

    def event_keyDown(self,key):
        if key == K_w:
            self.dominantY = 1
            if self.listRunClock[0] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_s:
            self.dominantY = 2
            if self.listRunClock[1] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_a:
            self.dominantX = 1
            if self.listRunClock[2] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_d:
            self.dominantX = 2
            if self.listRunClock[3] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_w and self.dominantY != 2 and self.attacking == 0:
            self.ySpeed = -2
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
        if key == K_s and self.dominantY != 1 and self.attacking == 0:
            self.ySpeed = 2
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
        if key == K_a and self.dominantX != 2 and self.attacking == 0:
            self.xSpeed = -3
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
            for key, value in self.boy.items():
                self.boy[key].setFlipped(1,0)
        if key == K_d and self.dominantX != 1 and self.attacking == 0:
            self.xSpeed = 3
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
            for key, value in self.boy.items():
                self.boy[key].setFlipped(0,0)
        self.moving = abs(self.xSpeed) + abs(self.ySpeed)
        if key == K_j:
            if self.z == self.y:
                if self.moving == 0:
                    if self.attacking == 0:
                        self.boy['punch1'].index = 0
                        self.punch1Anim = 18
                    if self.punch2Anim == 0 and self.punch1Anim <= 8 and self.punch1Anim > 0:
                        self.boy['punch2'].index = 0
                        self.punch2Anim = 24
                        self.punch1Anim = 0
                elif self.running == 1:
                    if self.attacking == 0:
                        self.boy['datk'].index = 0
                        self.datkAnim = 21
                        self.xDashSpeed = self.xSpeed
                        self.yDashSpeed = self.ySpeed
                        self.xSpeed = 0
                        self.ySpeed = 0
                        self.running = 0
        if key == K_k:
            if self.z == self.y and self.moving == 0 and self.attacking == 0:
                self.boy['kick'].index = 0
                self.kickAnim = 24
        if key == K_SPACE:
            if self.y == self.z:
                self.jumpRelease = 0
                self.jumpSpeed = self.maxJumpSpeed
                self.y -= self.jumpSpeed
                airborne = 1
                self.boy['jump'].index = 0

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
        if key == K_SPACE:
            self.jumpRelease = 1

    def event_collision(self,other):
        print("Ouch!")

    def update(self):
        keys = pygame.key.get_pressed()
        self.attacking = self.punch1Anim + self.punch2Anim + self.kickAnim + self.datkAnim
        if self.datkAnim == 0:
            if not (keys[K_a] or keys[K_d] or keys[K_w] or keys[K_s]):
                self.runModifier = 1
            if self.dominantX == 0:
                self.xSpeed = 0
            if self.dominantY == 0:
                self.ySpeed = 0
            if self.xSpeed == 0 and self.ySpeed == 0:
                self.moving = 0
            if self.moving == 0 and self.attacking == 0 and self.y == self.z:
                self.setSprite(self.boy['idle'])
                self.running = 0
            if self.running == 1 and self.datkAnim == 0:
                self.setSprite(self.boy['run'])
            elif self.running == 0 and self.moving > 0:
                self.setSprite(self.boy['walk'])
        if self.punch1Anim > 0:
            self.punch1Anim -= 1
            self.setSprite(self.boy['punch1'])
        if self.punch2Anim > 0:
            self.punch2Anim -= 1
            self.setSprite(self.boy['punch2'])
        if self.kickAnim > 0:
            self.kickAnim -= 1
            self.setSprite(self.boy['kick'])
        if self.datkAnim > 6:
            self.datkAnim -= 1
            self.setSprite(self.boy['datk'])
            self.x += self.xDashSpeed*self.runModifier
            self.y += self.yDashSpeed*self.runModifier
            self.z += self.yDashSpeed*self.runModifier
        elif self.datkAnim <= 6 and self.datkAnim > 0:
            self.datkAnim -= 1
            self.setSprite(self.boy['datk'])
        for i in range(0,len(self.listRunClock)):
            if self.listRunClock[i] > 0:
                self.listRunClock[i] -= 1
        if self.y < self.z:
            self.jumpSpeed -= self.gravity
            self. y -= self.jumpSpeed
            if self.jumpSpeed >= 0:
                self.setSprite(self.boy['jump'])
                if self.boy['jump'].index == 5:
                    self.boy['jump'].index = 4
            elif self.jumpSpeed < 0:
                self.setSprite(self.boy['land'])
        if self.y > self.z:
            self.y = self.z
        if keys[K_SPACE] and self.jumpRelease == 0 and self.jumpSpeed > 0:
            self.jumpSpeed += .2
        self.x += self.xSpeed*self.runModifier
        self.y += self.ySpeed*self.runModifier
        self.z += self.ySpeed*self.runModifier
        self.shadow.y = self.z-6
        self.shadow.sprite.setFlipped(self.sprite.flipx,self.sprite.flipy)
        if self.shadow.sprite.flipx == 0:
            self.shadow.x = self.x-19
        elif self.shadow.sprite.flipx == 1:
            self.shadow.x = self.x-21

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
    oShadow = Shadow(100-19,400-6,"medium")
    oBoy = Character(100,400,oShadow)
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
    street.addToRoom(oShadow)
    street.addToRoom(oBoy)
    game.addRoom(street)
    game.gotoRoom("mainmenu")


    while(True):
        #update
        game.update()
        print(oBoy.boy['jump'].index)
        #render
        game.render()

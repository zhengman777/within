'''
Created on May 12, 2013

@author: Catt
'''
import pygmi, pygame, os, sys,math
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
        if room == mainmenu:
            super().__init__(self.bgMainMenu,x,y)
        if room == street:
            super().__init__(self.bgStreet,x,y)

class HUD(pygmi.Object):

    def __init__(self,x,y,character):
        self.hp = str(character.hp)
        self.sprHP = pygmi.Sprite(pygmi.Tools.makeText(self.hp,None,None,None),0,0,0,0)
        super().__init__(self.sprHP,x,y)

    def update(self):
        self.setSprite(pygmi.Sprite(pygmi.Tools.makeText(self.hp,None,None,None),0,0,0,0))

class Shadow(pygmi.Object):

    def __init__(self,x,y,size):
        self.size = size
        self.sprShadowM = pygmi.Sprite("img/fx/shadowM.png",0,0,64,30)
        self.sprShadowM.setAlpha(100)
        if self.size == "medium":
            super().__init__(self.sprShadowM,x,y)

class Hitbox(pygmi.Object):

    def __init__(self,x,y,hitbox):
        self.power = 0
        self.hitbox = hitbox
        htbxBoyPunch = pygmi.Sprite("img/htbx/zPunch.png",0,0,17,12)
        htbxBoyKick = pygmi.Sprite("img/htbx/zKick.png",0,0,21,12)
        htbxBoyDatk = pygmi.Sprite("img/htbx/zDatk.png",0,0,19,7)
        self.htbxBoy = {'punch':htbxBoyPunch,'kick':htbxBoyKick,'datk':htbxBoyDatk}
        if hitbox == "punch":
            self.sprite = self.htbxBoy['punch']
            self.countdown = 8
        super().__init__(self.sprite,x,y)
        self.setSolid(True)
        #self.setVisible(False)

    def update(self):
        if self.hitbox == "punch":
            self.power = 1
        if self.countdown > 0:
            self.countdown -= 1
        if self.countdown == 0:
            self.destroy()

class Character(pygmi.Object):

    def __init__(self,x,y,shadow):
        self.shadow = shadow
        self.xSpeed = 0
        self.ySpeed = 0
        self.z = y
        self.x_scale = 1
        self.hp = 30
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
        self.akickAnim = 0
        sprIdle = pygmi.Sprite("img/char/boy_idle",-18,-64,30,64)
        sprIdle.setFrameTime(30)
        sprWalk = pygmi.Sprite("img/char/boy_walk",-18,-66,30,66)
        sprWalk.setFrameTime(8)
        sprRun = pygmi.Sprite("img/char/boy_run",-22,-70,44,68)
        sprRun.setFrameTime(5)
        sprPunch1 = pygmi.Sprite("img/char/boy_punch1",-18,-64,40,64)
        sprPunch1.setFrameTime(2)
        sprPunch2 = pygmi.Sprite("img/char/boy_punch2",-20,-64,38,64)
        sprPunch2.setFrameTime(2)
        sprKick = pygmi.Sprite("img/char/boy_kick",-18,-64,40,64)
        sprKick.setFrameTime(2)
        sprDatk = pygmi.Sprite("img/char/boy_datk",-20,-66,40,64)
        sprDatk.setFrameTime(3)
        sprJump = pygmi.Sprite("img/char/boy_jump",-18,-66,32,66)
        sprJump.setFrameTime(2)
        sprLand = pygmi.Sprite("img/char/boy_land.png",-16,-66,30,66)
        sprAkick = pygmi.Sprite("img/char/boy_akick",-12,-59,36,60)
        sprAkick.setFrameTime(2)
        self.boy = {'idle':sprIdle,'walk':sprWalk,'run':sprRun,'punch1':sprPunch1,
                    'punch2':sprPunch2,'kick':sprKick,'datk':sprDatk,'jump':sprJump,
                    'land':sprLand,'akick':sprAkick}
        super().__init__(self.boy['idle'],x,y)
        self.setSolid(True)

    def event_keyPressed(self,key):
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
            self.x_scale = -1
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
            for key, value in self.boy.items():
                self.boy[key].setFlipped(1,0)
        if key == K_d and self.dominantX != 1 and self.attacking == 0:
            self.xSpeed = 3
            self.x_scale = 1
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
                        for e in enemyList:
                            e.zPunchHit = 0
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
            elif self.y < self.z:
                if self.attacking == 0:
                    self.boy['akick'].index = 0
                    self.akickAnim = 14
                    print('hi')
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

    def event_keyReleased(self,key):
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
        if other == Apathol:
            print("ouch")

    def update(self):
        keys = pygame.key.get_pressed()
        self.attacking = (self.punch1Anim + self.punch2Anim + self.kickAnim + self.datkAnim
            + self.akickAnim)
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
        if self.punch1Anim == 18:
            oHtbxPunch = Hitbox(self.x+(4*self.x_scale),self.y-44,"punch")
            oHtbxPunch.sprite.setFlipped(self.sprite.flipx,0)
            game.activeRoom.addToRoom(oHtbxPunch)
        if self.punch1Anim > 0:
            self.punch1Anim -= 1
            self.setSprite(self.boy['punch1'])
        if self.punch2Anim > 0:
            self.punch2Anim -= 1
            self.setSprite(self.boy['punch2'])
        if self.kickAnim > 0:
            self.kickAnim -= 1
            self.setSprite(self.boy['kick'])
        if self.akickAnim > 0:
            self.akickAnim -= 1
            self.setSprite(self.boy['akick'])
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
            if self.jumpSpeed >= 0 and self.attacking == 0:
                self.setSprite(self.boy['jump'])
                if self.boy['jump'].index == 5:
                    self.boy['jump'].index = 4
            elif self.jumpSpeed < 0 and self.attacking == 0:
                self.setSprite(self.boy['land'])
        if self.y > self.z:
            self.y = self.z
            self.aKickAnim = 0
        if keys[K_SPACE] and self.jumpRelease == 0 and self.jumpSpeed > 0:
            self.jumpSpeed += .125
        self.x += self.xSpeed*self.runModifier
        self.y += self.ySpeed*self.runModifier
        self.z += self.ySpeed*self.runModifier
        self.setDepth(-self.z)
        self.shadow.y = self.z-6
        if self.sprite.flipx == 0:
            self.shadow.x = self.x-19
        elif self.sprite.flipx == 1:
            self.shadow.x = self.x-15


class Enemy(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.zPunchHit = 0
        self.recoilAnim = 0
        self.recoilSide = 0
        self.recoilCounter = 0
        self.recoilDistance = 0
        enemyList.append(self)
        super().__init__(sprite,x,y)

    def event_collision(self,other):
        if type(other) == Hitbox:
            if self.zPunchHit == 0 and other.sprite == other.htbxBoy['punch']:
                self.zPunchHit = 1
                self.hp -= 1
                self.recoilAnim = self.recoilTime
                if other.x < self.x:
                    self.recoilSide = 1
                elif other.x >= self.x:
                    self.recoilSide = -1
            self.recoilCounter = 4
            self.recoilDistance = other.power/self.weight
            print('ouch')

    def update(self):
        if self.recoilAnim > 0:
            self.recoilAnim -= 1
        if self.recoilCounter > 0:
            self.x += self.recoilDistance * self.recoilSide
            self.recoilCounter -= 1
        self.z = self.y
        self.setDepth(-self.z)

class Apathol(Enemy):

    def __init__(self,x,y):
        self.hp = 30
        self.recoilTime = 12
        self.weight = 1
        sprIdle = pygmi.Sprite("img/enemy/apathol_idle",-8,-38,16,18)
        sprIdle.setFrameTime(30)
        sprRecoil = pygmi.Sprite("img/enemy/apathol_recoil",-24,-52,42,44)
        sprRecoil.setFrameTime(4)
        self.apathol = {'idle':sprIdle,'recoil':sprRecoil}
        super().__init__(self.apathol['idle'],x,y)
        self.setSolid(True)

    def event_collision(self,other):
        super().event_collision(other)

    def update(self):
        if self.recoilAnim > 0:
            self.sprite = self.apathol['recoil']
            self.apathol['recoil'].index = 0
        else:
            self.sprite = self.apathol['idle']
        super().update()


#Retained for posterity, I suppose. -Ctt
#class Ball(pygmi.Object):
#
#    def __repr__(self):
#        return "ball"
#
#    def __init__(self,x,y):
#        random.seed()
#        self.xSpeed = random.randint(0,4)
#        self.ySpeed = random.randint(0,4)
#        sprBall = pygmi.Sprite("img/enemies/apathol_spawn/apathol_spawn_03.png",-32,-32,64,64)
#        sprBall.setFrameTime(1)
#        super().__init__(sprBall,x,y)
#
#    def event_collision(self,other):
#
#        if(bool(random.getrandbits(1))):
#            self.xSpeed *= -1
#        else:
#            self.ySpeed *= -1
#
#    def update(self):
#        self.x += self.xSpeed
#        self.y += self.ySpeed
#        if self.x > x_dim or self.x < 0:
#            self.xSpeed *= -1
#        if self.y > y_dim or self.y < 0:
#            self.ySpeed *= -1
#
#        if random.randint(0,100) > 99:
#            self.destroy()

if __name__ == '__main__':
    x_dim = 800
    y_dim = 600
    game = pygmi.Pygmi((x_dim,y_dim), "Test Game", 0)
    oShadow = Shadow(100-19,400-6,"medium")
    oBoy = Character(100,400,oShadow)
    oHUD = HUD(10,10,oBoy)
    enemyList = []
    oApathol = Apathol(200,400)
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
    street.addToRoom(oHUD)
    street.addToRoom(oApathol)
    game.addRoom(street)
    game.gotoRoom("mainmenu")


    while(True):
        #update
        game.update()
        #render
        game.render()
        #paint
        game.paint()

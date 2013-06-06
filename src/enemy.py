import pygmi, pygame, os, sys, math
from pygame.locals import *
from within import *

class Enemy(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.zPunch1Hit = 0
        self.zPunch2Hit = 0
        self.recoilAnim = 0
        self.recoilSide = 0
        self.recoilCounter = 0
        self.recoilDistance = 0
        self.enemyList.append(self)
        super().__init__(sprite,x,y)

    def event_collision(self,other):
        if type(other) == Hitbox:
            print(other)
            if self.zPunch1Hit == 0 and other.sprite == other.htbxBoy['punch1']:
                self.zPunch1Hit = 1
                self.hp -= 1
                self.recoilAnim = self.recoilTime
            if self.zPunch2Hit == 0 and other.sprite == other.htbxBoy['punch2']:
                self.zPunch2Hit = 1
                self.hp -= 1
                self.recoilAnim = self.recoilTime
            if other.sprite.flipx == 0:
                self.recoilSide = 1
            elif other.sprite.flipx == 1:
                self.recoilSide = -1
            self.recoilCounter = 4
            self.recoilDistance = other.power/self.weight


    def update(self):
        if self.recoilAnim > 0:
            self.recoilAnim -= 1
        if self.recoilCounter > 0:
            self.x += self.recoilDistance * self.recoilSide
            self.recoilCounter -= 1
        self.z = self.y
        self.setDepth(-self.z)

class Apathol(Enemy):

    def __init__(self,x,y,enemyList):
        self.hp = 30
        self.recoilTime = 12
        self.weight = 1
        self.enemyList = enemyList
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
        if self.recoilAnim == self.recoilTime:
            self.apathol['recoil'].index = 0
        if self.recoilAnim > 0:
            self.sprite = self.apathol['recoil']
        else:
            self.sprite = self.apathol['idle']
        super().update()
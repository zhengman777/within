import pygmi, pygame, os, sys, math
from pygame.locals import *

class Enemy(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.zPunch1Hit = 0
        self.zPunch2Hit = 0
        self.zKickHit = 0
        self.recoilAnim = 0
        self.recoilSide = 0
        self.recoilCounter = 0
        self.recoilDistance = 0
        super().__init__(sprite,x,y)

    def update(self):
        if self.recoilAnim > 0:
            self.recoilAnim -= 1
        if self.recoilCounter > 0:
            self.x += self.recoilDistance * self.recoilSide
            self.recoilCounter -= 1
        self.z = self.y
        self.setDepth(-self.z)

class Apathol(Enemy):

    def __init__(self,x,y,shadow):
        self.hp = 30
        self.recoilTime = 12
        self.weight = 1
        self.shadow = shadow
        self.z = y
        sprIdle = pygmi.Sprite("img/enemy/apathol_idle",-8,-38,16,18)
        sprIdle.setFrameTime(30)
        sprRecoil = pygmi.Sprite("img/enemy/apathol_recoil",-24,-52,42,44)
        sprRecoil.setFrameTime(4)
        self.apathol = {'idle':sprIdle,'recoil':sprRecoil}
        super().__init__(self.apathol['idle'],x,y)
        self.setSolid(True)

    def update(self):
        if self.recoilAnim == self.recoilTime:
            self.apathol['recoil'].index = 0
        if self.recoilAnim > 0:
            self.sprite = self.apathol['recoil']
        else:
            self.sprite = self.apathol['idle']
        self.shadow.x = self.x-8
        self.shadow.y = self.z
        super().update()
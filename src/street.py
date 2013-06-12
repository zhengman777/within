import pygmi, pygame, os, sys, math
from pygame.locals import *
from universal import Shadow, Hitbox
from player import Character, HUD
from enemy import Enemy, Apathol

class Street(pygmi.Room):

    def __init__(self,game):
        self.game = game
        oShadowBoy = Shadow(pygmi.Sprite("img/fx/shadowHuman.png",0,0,34,10),100-19,400-6)
        oBoy = Character(100,400,oShadowBoy,self.game)
        oHUD = HUD(10,10,oBoy)
        oShadowApathol = Shadow(pygmi.Sprite("img/fx/shadowApathol.png",0,0,16,6),200-8,400)
        oApathol = Apathol(200,400,oShadowApathol)
        bgStreet = pygmi.Object(pygmi.Sprite("img/bg/street.png",0,0,800,600),0,0)
        super().__init__("street",1200,600)
        self.addToRoom(bgStreet)
        self.addToRoom(oShadowBoy)
        self.addToRoom(oShadowApathol)
        self.addToRoom(oBoy)
        self.addToRoom(oHUD)
        self.addToRoom(oApathol)
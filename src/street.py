import pygmi, pygame, os, sys, math
from pygame.locals import *
from universal import *
from player import *

class Street(pygmi.Room):

    def __init__(self):
        oShadowBoy = Shadow(pygmi.Sprite("img/fx/shadowHuman.png",0,0,34,10),100-19,400-6)
        oBoy = Character(100,400,oShadowBoy)
        oHUD = HUD(10,10,oBoy)
        enemyList = []
        oShadowApathol = Shadow(pygmi.Sprite("img/fx/shadowApathol.png",0,0,16,6),200-8,400)
        oApathol = Apathol(200,400,enemyList,oShadowApathol)
        bgStreet = pygmi.Object(pygmi.Sprite("img/bg/street.png",0,0,800,600),0,0)
        street.addToRoom(bgStreet)
        street.addToRoom(oShadowBoy)
        street.addToRoom(oShadowApathol)
        street.addToRoom(oBoy)
        street.addToRoom(oHUD)
        street.addToRoom(oApathol)
        super().__init__("street",1200,600)
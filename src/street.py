import pygmi
from pygame.locals import *
from universal import Shadow, Hitbox
from player import Character, HUD
from enemies import Apathol
from flare import Flare

class Street(pygmi.Room):

    def __init__(self):
        self.boundX_min = 0
        self.boundX_max = 1200
        self.boundY_min = 344
        self.boundY_max = 514
        self.enemyCount = 0
        super().__init__("street",1200,600)

    def event_create(self):
        oShadowBoy = Shadow(pygmi.Sprite(self.assets.images["fx"]["shadowHuman.png"],34,10),100-19,400-6)
        self.oBoy = Character(100,400,oShadowBoy,self.game)
        oHUD = HUD(0,600-84,self.oBoy)
        self.setBackground(self.assets.images["bg"]["street.png"])
        self.game.createInstance(oShadowBoy)
        self.game.createInstance(self.oBoy)
        self.game.createInstance(oHUD)


    def update(self):
        if self.oBoy.x <= 400:
            self.setView(0,0,800,600)
        elif self.oBoy.x >= 800:
            self.setView(400,0,800,600)
        else:
            self.setView(self.oBoy.x - 400,0,800,600)
        if self.enemyCount < 1:
            self.oShadowApathol = Shadow(pygmi.Sprite(self.assets.images["fx"]["shadowApathol.png"],16,6),200-8,400)
            self.oApathol = Apathol(200,400,self.oShadowApathol)
            self.game.createInstance(self.oApathol)
            self.game.createInstance(self.oShadowApathol)
            self.enemyCount += 1
            print(self.oApathol)
        print(self.enemyCount)
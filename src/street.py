import pygmi
from pygame.locals import *
from universal import Shadow, Hitbox
from player import Character, HUD
from enemy import Enemy, Apathol
from flare import Flare

class Street(pygmi.Room):

    def __init__(self):
        super().__init__("street",1200,600)

    def event_create(self):
        oShadowBoy = Shadow(pygmi.Sprite(self.assets.images["fx"]["shadowHuman.png"],34,10),100-19,400-6)
        oBoy = Character(100,400,oShadowBoy,self.game)
        oHUD = HUD(10,10,oBoy)
        oShadowApathol = Shadow(pygmi.Sprite(self.assets.images["fx"]["shadowApathol.png"],16,6),200-8,400)
        oApathol = Apathol(200,400,oShadowApathol)
        self.setBackground(self.assets.images["bg"]["street.png"])
        self.game.createInstance(oShadowBoy)
        self.game.createInstance(oShadowApathol)
        self.game.createInstance(oBoy)
        self.game.createInstance(oHUD)
        self.game.createInstance(oApathol)
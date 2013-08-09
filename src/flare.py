import pygmi
from universal import Hitbox

class Flare(Hitbox):

    def __init__(self,x,y,flip,owner):
        self.flip = flip
        if flip == 0:
            self.direction = 1
        if flip == 1:
            self.direction = -1
        super().__init__(x,y,"flare",owner)
        self.setSolid(True)
        self.setVisible(True)

    def event_create(self):
        self.sprFlare = pygmi.Sprite(self.assets.images["fx"]["flare.png"],22,10,0,0)
        self.setSprite(self.sprFlare)
        self.setFlipped(self.flip,0)
        self.power = 3
        self.countdown = 80

    def event_collision(self,other):
        super().event_collision(other)

    def update(self):
        self.move(6*self.direction,0)
        super().update()
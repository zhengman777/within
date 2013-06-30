import pygmi

class Flare(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.spr = sprite
        super().__init__(x,y)
        self.setSolid(True)

    def event_create(self):
        self.sprFlare = pygmi.Sprite(self.assets.images["fx"]["flare.png"],22,10,0,0)

    def update(self):
        self.setSprite(self.sprFlare)
import pygmi

class Flare(pygmi.Object):

    def __init__(self,x,y,flip):
        self.flip = flip
        if flip == 0:
            self.direction = 1
        if flip == 1:
            self.direction = -1
        super().__init__(x,y)
        self.setSolid(True)

    def event_create(self):
        self.sprFlare = pygmi.Sprite(self.assets.images["fx"]["flare.png"],22,10,0,0)
        self.setSprite(self.sprFlare)
        self.setFlipped(self.flip,0)

    def event_collision(self,other):
        print(other)

    def update(self):
        self.move(6*self.direction,0)
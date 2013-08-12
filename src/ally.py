import pygmi

class Ally(pygmi.Object):

    def __init__(self,x,y):
        super().__init__(x,y)
        self.z = y
        self.recoilAnim = 0
        self.setSolid(True)

    def event_create(self):
        pass

    def update(self):
        pass
import pygmi

class Enemy(pygmi.Object):

    def __init__(self,x,y):
        self.side = "enemy"
        self.zPunch1Hit = 0
        self.zPunch2Hit = 0
        self.zKickHit = 0
        self.recoilAnim = 0
        self.recoilSide = 0
        self.recoilCounter = 0
        self.recoilDistance = 0
        super().__init__(x,y)
        self.setSolid(True)

    def event_create(self):
        pass

    def update(self):
        if self.recoilAnim > 0:
            self.recoilAnim -= 1
        if self.recoilCounter > 0:
            self.move(self.recoilDistance*self.recoilSide,0)
            self.recoilCounter -= 1
        self.z = self.y
        self.setDepth(-self.z)
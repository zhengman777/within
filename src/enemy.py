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
            if self.recoilSide == -1:
                if self.x + self.recoilDistance*self.recoilSide > self.room.boundX_min:
                    self.move(self.recoilDistance*self.recoilSide,0)
                    self.recoilCounter -= 1
                else:
                    self.x = self.room.boundX_min
            if self.recoilSide == 1:
                if self.x + self.recoilDistance*self.recoilSide < self.room.boundX_max:
                    self.move(self.recoilDistance*self.recoilSide,0)
                    self.recoilCounter -= 1
                else:
                    self.x = self.room.boundX_max
        self.z = self.y
        self.setDepth(-self.z)
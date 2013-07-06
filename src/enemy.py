import pygmi

class Enemy(pygmi.Object):

    def __init__(self,x,y):
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

class Apathol(Enemy):

    def __init__(self,x,y,shadow):
        self.hp = 30
        self.recoilTime = 12
        self.weight = 1
        self.shadow = shadow
        self.z = y
        super().__init__(x,y)

    def event_create(self):
        sprIdle = pygmi.Sprite(self.assets.images["enemy"]["apathol_idle"],16,18,-8,-38)
        sprIdle.setFrameTime(30)
        sprRecoil = pygmi.Sprite(self.assets.images["enemy"]["apathol_recoil"],42,44,-24,-52)
        sprRecoil.setFrameTime(4)
        self.apathol = {'idle':sprIdle,'recoil':sprRecoil}

    def update(self):
        if self.recoilAnim == self.recoilTime:
            self.apathol['recoil'].index = 0
        if self.recoilAnim > 0:
            self.setSprite(self.apathol['recoil'])
        else:
            self.setSprite(self.apathol['idle'])
        self.shadow.x = self.x-8
        self.shadow.y = self.z
        super().update()
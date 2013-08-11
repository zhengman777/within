import pygmi
from enemy import Enemy, Apathol

class Shadow(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.spr = sprite
        super().__init__(x,y)

    def event_create(self):
        self.setSprite(self.spr)
        self.sprite.setAlpha(50)
        print(self.sprite.image.get_alpha())

class Hitbox(pygmi.Object):

    def __init__(self,x,y,hitbox,owner):
        self.power = 0
        self.hitbox = hitbox
        self.owner = owner
        self.enemyList = []
        super().__init__(x,y)
        self.setSolid(True)
        self.setVisible(False)

    def event_create(self):
        htbxBoyPunch1 = pygmi.Sprite(self.assets.images["htbx"]["zPunch1.png"],17,14,0,0)
        htbxBoyPunch2 = pygmi.Sprite(self.assets.images["htbx"]["zPunch2.png"],17,14,0,0)
        htbxBoyKick = pygmi.Sprite(self.assets.images["htbx"]["zKick.png"],21,16,0,0)
        htbxBoyDatk = pygmi.Sprite(self.assets.images["htbx"]["zDatk.png"],19,30,0,0)
        htbxBoyAkick = pygmi.Sprite(self.assets.images["htbx"]["zAkick.png"],21,16,0,0)
        self.htbxBoy = {'punch1':htbxBoyPunch1,'punch2':htbxBoyPunch2,'kick':htbxBoyKick,
            'datk':htbxBoyDatk,'akick':htbxBoyAkick}
        if self.hitbox == "punch1":
            self.setSprite(self.htbxBoy['punch1'])
            self.countdown = 8
            self.power = 1
        if self.hitbox == "punch2":
            self.setSprite(self.htbxBoy['punch2'])
            self.countdown = 8
            self.power = 1
        if self.hitbox == "kick":
            self.setSprite(self.htbxBoy['kick'])
            self.countdown = 8
            self.power = 5
        if self.hitbox == "datk":
            self.setSprite(self.htbxBoy['datk'])
            self.countdown = 21
            self.power = 5
        if self.hitbox == 'akick':
            self.setSprite(self.htbxBoy['akick'])
            self.countdown = 10
            self.power = 8

    def event_collision(self,other):
        if type(other) == Apathol:
            if other not in self.enemyList:
                self.enemyList.append(other)
                other.recoilAnim = other.recoilTime
                other.hp -= 1
                if self._flipped_x == 0:
                    other.recoilSide = 1
                elif self._flipped_x == 1:
                    other.recoilSide = -1
                other.recoilCounter = 4
                other.recoilDistance = self.power/other.weight

    def update(self):
        if self.hitbox == "datk":
            self.x = self.owner.x
            self.y = self.owner.y-30
        if self.hitbox == "akick":
            self.x = self.owner.x+4*self.owner.x_scale
            self.setFlipped(self.owner._flipped_x,0)
            self.y = self.owner.y-30
        if self.countdown > 0:
            self.countdown -= 1
        if self.countdown == 0:
            self.destroy()
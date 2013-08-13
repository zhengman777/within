import pygmi
from enemy import Enemy
from ally import Ally

class Shadow(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.spr = sprite
        super().__init__(x,y)

    def event_create(self):
        self.setSprite(self.spr)
        self.sprite.setAlpha(50)

class Hitbox(pygmi.Object):

    def __init__(self,x,y,hitbox,owner):
        self.hitbox = hitbox
        self.power = 0
        self.countdown = 0
        self.owner = owner
        self.type = None
        if isinstance(self.owner, Ally):
            self.enemyList = []
        if isinstance(self.owner, Enemy):
            self.allyList = []
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
        htbxApatholAtk = pygmi.Sprite(self.assets.images["htbx"]["apatholAtk.png"],32,32,0,0)
        if self.hitbox == "boy_punch1":
            self.setSprite(self.htbxBoy['punch1'])
            self.countdown = 8
            self.power = 1
            self.type = 'uni'
        if self.hitbox == "boy_punch2":
            self.setSprite(self.htbxBoy['punch2'])
            self.countdown = 8
            self.power = 1
            self.type = 'uni'
        if self.hitbox == "boy_kick":
            self.setSprite(self.htbxBoy['kick'])
            self.countdown = 8
            self.power = 5
            self.type = 'uni'
        if self.hitbox == "boy_datk":
            self.setSprite(self.htbxBoy['datk'])
            self.countdown = 21
            self.power = 5
            self.type = 'uni'
        if self.hitbox == 'boy_akick':
            self.setSprite(self.htbxBoy['akick'])
            self.countdown = 10
            self.power = 8
            self.type = 'uni'
        if self.hitbox == 'apathol_atk':
            self.setSprite(htbxApatholAtk)
            self.countdown = 28
            self.power = 1
            self.type = 'bi'

    def event_collision(self,other):
        if isinstance(other, Enemy) and isinstance(self.owner, Ally):
            if other not in self.enemyList:
                self.enemyList.append(other)
                other.recoilAnim = other.recoilTime
                other.hp -= 1
                if self.type == 'uni':
                    if self._flipped_x == 0:
                        other.recoilSide = 1
                    elif self._flipped_x == 1:
                        other.recoilSide = -1
                other.recoilCounter = 4
                other.recoilDistance = self.power/other.weight
        if isinstance(other, Ally) and isinstance(self.owner, Enemy):
            if other not in self.allyList:
                if other.guarding == 0:
                    self.allyList.append(other)
                    other.recoilAnim = other.recoilTime
                    other.hp -= 1
                    if self.type == 'uni':
                        if self._flipped_x == 0:
                            other.recoilSide = 1
                        elif self._flipped_x == 1:
                            other.recoilSide = -1
                    if self.type == 'bi':
                        if self.owner.x <= other.x:
                            other.recoilSide = 1
                        if self.owner.x > other.x:
                            other.recoilSide = -1
                    other.recoilCounter = 4
                    other.recoilDistance = self.power/other.weight

    def update(self):
        if self.hitbox == "boy_datk":
            self.x = self.owner.x
            self.y = self.owner.y-30
        if self.hitbox == "boy_akick":
            self.x = self.owner.x+4*self.owner.x_scale
            self.setFlipped(self.owner._flipped_x,0)
            self.y = self.owner.y-30
        if self.countdown > 0:
            self.countdown -= 1
        if self.countdown == 0:
            self.destroy()
        if self.owner.recoilAnim > 0:
            self.destroy()
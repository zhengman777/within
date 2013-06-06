import pygmi, pygame, os, sys, math

class Shadow(pygmi.Object):

    def __init__(self,sprite,x,y):
        self.sprite = sprite
        self.sprite.setAlpha(100)
        super().__init__(self.sprite,x,y)

class Hitbox(pygmi.Object):

    def __init__(self,x,y,hitbox,owner):
        self.power = 0
        self.hitbox = hitbox
        self.owner = owner
        htbxBoyPunch1 = pygmi.Sprite("img/htbx/zPunch1.png",0,0,17,14)
        htbxBoyPunch2 = pygmi.Sprite("img/htbx/zPunch2.png",0,0,17,14)
        htbxBoyKick = pygmi.Sprite("img/htbx/zKick.png",0,0,21,16)
        htbxBoyDatk = pygmi.Sprite("img/htbx/zDatk.png",0,0,19,30)
        htbxBoyAkick = pygmi.Sprite("img/htbx/zAkick.png",0,0,21,16)
        self.htbxBoy = {'punch1':htbxBoyPunch1,'punch2':htbxBoyPunch2,'kick':htbxBoyKick,
            'datk':htbxBoyDatk,'akick':htbxBoyAkick}
        if hitbox == "punch1":
            self.sprite = self.htbxBoy['punch1']
            self.countdown = 8
            self.power = 1
        if hitbox == "punch2":
            self.sprite = self.htbxBoy['punch2']
            self.countdown = 8
            self.power = 1
        if hitbox == "kick":
            self.sprite = self.htbxBoy['kick']
            self.countdown = 8
            self.power = 4
        if hitbox == "datk":
            self.sprite = self.htbxBoy['datk']
            self.countdown = 21
            self.power = 4
        if hitbox == 'akick':
            self.sprite = self.htbxBoy['akick']
            self.countdown = 10
            self.power = 1
        super().__init__(self.sprite,x,y)
        self.setSolid(True)
        #self.setVisible(False)

    def update(self):
        if self.hitbox == "datk":
            self.x = self.owner.x
            self.y = self.owner.y-30
        if self.hitbox == "akick":
            self.x = self.owner.x+4*self.owner.x_scale
            self.y = self.owner.y-30
        if self.countdown > 0:
            self.countdown -= 1
        if self.countdown == 0:
            self.destroy()

import pygmi
from universal import Hitbox
from enemy import Enemy

class Apathol(Enemy):

    def __init__(self,x,y,shadow):
        self.hp = 10
        self.power = 3
        self.timer = 100
        self.recoilTime = 12
        self.spawnTime = 24
        self.atkAnim = 0
        self.weight = 1
        self.shadow = shadow
        self.z = y
        super().__init__(x,y)
        self.alpha = 255

    def event_create(self):
        sprSpawn = pygmi.Sprite(self.assets.images["enemy"]["apathol_spawn"],40,38,-24,-48)
        sprSpawn.setFrameTime(6)
        sprIdle = pygmi.Sprite(self.assets.images["enemy"]["apathol_idle"],16,18,-8,-38)
        sprIdle.setFrameTime(30)
        sprRecoil = pygmi.Sprite(self.assets.images["enemy"]["apathol_recoil"],42,44,-24,-52)
        sprRecoil.setFrameTime(4)
        sprAtk = pygmi.Sprite(self.assets.images["enemy"]["apathol_atk"],32,32,-16,-46)
        sprAtk.setFrameTime(4)
        sprDeath = pygmi.Sprite(self.assets.images["enemy"]["apathol_death"],40,38,-24,-48)
        sprDeath.setFrameTime(6)
        self.apathol = {'idle':sprIdle,'recoil':sprRecoil,'atk':sprAtk,'spawn':sprSpawn,
                'death':sprDeath}

    def update(self):
        if self.dead == 0:
            if self.spawnTime > 0:
                self.setSprite(self.apathol['spawn'])
                self.spawnTime -= 1
            if self.timer > 0 and self.spawnTime == 0:
                self.timer -= 1
            if self.timer == 0 and self.recoilAnim == 0:
                self.timer = 100
                self.atkAnim = 44
            if self.recoilAnim == 0:
                if self.atkAnim == 36:
                    oHtbxAtk = Hitbox(self.x-16,self.y-46,'apathol_atk',self)
                    self.game.createInstance(oHtbxAtk)
                    oHtbxAtk.setFlipped(self._flipped_x,0)
                if self.atkAnim > 0:
                    self.atkAnim -= 1
                    self.setSprite(self.apathol['atk'])
            if self.recoilAnim == self.recoilTime:
                self.apathol['recoil'].index = 0
                self.atkAnim = 0
            if self.recoilAnim > 0:
                self.setSprite(self.apathol['recoil'])
            if self.recoilAnim == 0 and self.atkAnim == 0:
                self.setSprite(self.apathol['idle'])
        if self.hp <= 0:
            if self.dead == 0:
                self.dead = 1
                self.deathAnim = 24
            if self.deathAnim > 0:
                self.deathAnim -= 1
                self.setSprite(self.apathol['death'])
                self.alpha -= 10
                self.sprite.setAlpha(self.alpha)
            if self.deathAnim == 0 and self.dead == 1:
                self.destroy()
                self.shadow.destroy()
                self.room.enemyCount -= 1
        self.shadow.x = self.x-8
        self.shadow.y = self.z
        super().update()
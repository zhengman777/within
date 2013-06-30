import pygmi, pygame, os, sys, math
from pygame.locals import *
from universal import Hitbox

class Character(pygmi.Object):

    def __init__(self,x,y,shadow,game):
        self.game = game
        self.shadow = shadow
        self.xSpeed = 0
        self.ySpeed = 0
        self.z = y
        self.x_scale = 1
        self.hp = 30
        self.xDashSpeed = 0
        self.yDashSpeed = 0
        self.runModifier = 1
        self.dominantX = 0
        self.dominantY = 0
        self.stillHolding = [0, 0, 0, 0]
        self.running = 0
        self.listRunClock = [0, 0, 0, 0]
        self.attacking = 0
        self.moving = 0
        self.airborne = 0
        self.jumpRelease = 0
        self.jumpSpeed = 0
        self.maxJumpSpeed = 5
        self.gravity = .4
        self.punch1Anim = 0
        self.punch2Anim = 0
        self.kickAnim = 0
        self.datkAnim = 0
        self.akickAnim = 0
        super().__init__(x,y)
        self.setSolid(True)

    def event_create(self):
        sprIdle = pygmi.Sprite(self.assets.images["char"]["boy_idle"],30,64,-18,-64)
        sprIdle.setFrameTime(30)
        sprWalk = pygmi.Sprite(self.assets.images["char"]["boy_walk"],30,66,-18,-66)
        sprWalk.setFrameTime(8)
        # Idle and Walk do not jump around - this is because their X and W differ
        # by exactly the same amount.
        sprRun = pygmi.Sprite(self.assets.images["char"]["boy_run"],44,68,-22,-70)
        sprRun.setFrameTime(5)
        # For example, if you change Punch1's W to be -28 (so that the X-W differences are
        # the same across Idle, Walk, and Punch1), then using punch when facing left
        # is perfectly fine, though facing right is now messed up.
        # Also notice how the hitboxes are not aligned anymore when facing left.
        sprPunch1 = pygmi.Sprite(self.assets.images["char"]["boy_punch1"],40,64,-18,-64)
        sprPunch1.setFrameTime(2)
        sprPunch2 = pygmi.Sprite(self.assets.images["char"]["boy_punch2"],38,64,-20,-64)
        sprPunch2.setFrameTime(2)
        sprKick = pygmi.Sprite(self.assets.images["char"]["boy_kick"],40,64,-18,-64)
        sprKick.setFrameTime(2)
        sprDatk = pygmi.Sprite(self.assets.images["char"]["boy_datk"],40,64,-20,-66)
        sprDatk.setFrameTime(3)
        sprJump = pygmi.Sprite(self.assets.images["char"]["boy_jump"],32,66,-18,-66)
        sprJump.setFrameTime(2)
        sprLand = pygmi.Sprite(self.assets.images["char"]["boy_land.png"],30,66,-16,-66)
        sprAkick = pygmi.Sprite(self.assets.images["char"]["boy_akick"],36,60,-12,-59)
        sprAkick.setFrameTime(2)
        self.boy = {'idle':sprIdle,'walk':sprWalk,'run':sprRun,'punch1':sprPunch1,
                    'punch2':sprPunch2,'kick':sprKick,'datk':sprDatk,'jump':sprJump,
                    'land':sprLand,'akick':sprAkick}

    def event_keyPressed(self,key):
        if key == K_w:
            self.dominantY = 1
            self.stillHolding[0] = 1
            if self.listRunClock[0] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_s:
            self.dominantY = 2
            self.stillHolding[1] = 1
            if self.listRunClock[1] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_a:
            self.dominantX = 1
            self.stillHolding[2] = 1
            if self.listRunClock[2] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_d:
            self.dominantX = 2
            self.stillHolding[3] = 1
            if self.listRunClock[3] > 0 and self.attacking == 0:
                self.running = 1
                self.runModifier = 2
                self.listRunClock[0:3] = [0]*4
        if key == K_w and self.dominantY != 2 and self.attacking == 0:
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
        if key == K_s and self.dominantY != 1 and self.attacking == 0:
            if self.running == 0:
                self.boy['walk'].index = 0
            elif self.running == 1:
                self.boy['run'].index = 0
        if key == K_a and self.dominantX != 2:
            self.x_scale = -1
            self.setFlipped(1,0)
            if self.attacking == 0:
                if self.running == 0:
                    self.boy['walk'].index = 0
                elif self.running == 1:
                    self.boy['run'].index = 0
        if key == K_d and self.dominantX != 1:
            self.x_scale = 1
            self.setFlipped(0,0)
            if self.attacking == 0:
                if self.running == 0:
                    self.boy['walk'].index = 0
                elif self.running == 1:
                    self.boy['run'].index = 0
        if key == K_j:
            if self.z == self.y:
                if self.moving == 0:
                    if self.attacking == 0:
                        self.boy['punch1'].index = 0
                        self.punch1Anim = 18
                    if self.punch2Anim == 0 and self.punch1Anim <= 8 and self.punch1Anim > 0:
                        self.boy['punch2'].index = 0
                        self.punch2Anim = 24
                        self.punch1Anim = 0
                elif self.running == 1:
                    if self.attacking == 0:
                        self.boy['datk'].index = 0
                        self.datkAnim = 21
                        self.xDashSpeed = self.xSpeed
                        self.yDashSpeed = self.ySpeed
                        self.xSpeed = 0
                        self.ySpeed = 0
                        self.running = 0
                elif self.moving != 0 and self.running == 0:
                    if self.attacking == 0:
                        self.boy['kick'].index = 0
                        self.kickAnim = 24
                        self.xSpeed = 0
                        self.ySpeed = 0
            elif self.y < self.z:
                if self.attacking == 0:
                    self.boy['akick'].index = 0
                    self.akickAnim = 14
        if key == K_SPACE and self.attacking == 0:
            if self.y == self.z:
                self.jumpRelease = 0
                self.jumpSpeed = self.maxJumpSpeed
                self.move(0,-self.jumpSpeed)
                airborne = 1
                self.boy['jump'].index = 0

    def event_keyReleased(self,key):
        if key == K_w:
            self.stillHolding[0] = 0
            if self.stillHolding[1] == 1:
                self.dominantY = 2
            self.listRunClock[0] = 10
        if key == K_s:
            self.stillHolding[1] = 0
            if self.stillHolding[0] == 1:
                self.dominantY = 1
            self.listRunClock[1] = 10
        if key == K_a:
            self.stillHolding[2] = 0
            if self.stillHolding[3] == 1:
                self.dominantX = 2
            self.listRunClock[2] = 10
        if key == K_d:
            self.stillHolding[3] = 0
            if self.stillHolding[2] == 1:
                self.dominantX = 1
            self.listRunClock[3] = 10
        if key == K_SPACE:
            self.jumpRelease = 1

    def event_collision(self,other):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.attacking = (self.punch1Anim + self.punch2Anim + self.kickAnim + self.datkAnim
            + self.akickAnim)
        if keys[K_w] and self.dominantY != 2 and self.stillHolding[0] == 1 and self.attacking == 0:
            self.ySpeed = -2
        if keys[K_s] and self.dominantY != 1 and self.stillHolding[1] == 1 and self.attacking == 0:
            self.ySpeed = 2
        if keys[K_a] and self.dominantX != 2 and self.stillHolding[2] == 1 and self.attacking == 0:
            self.xSpeed = -3
            self.x_scale = -1
        if keys[K_d] and self.dominantX != 1 and self.stillHolding[3] == 1 and self.attacking == 0:
            self.xSpeed = 3
            self.x_scale = 1
        self.moving = abs(self.xSpeed) + abs(self.ySpeed)
        if self.datkAnim == 0:
            if not (keys[K_a] or keys[K_d] or keys[K_w] or keys[K_s]) and self.y == self.z:
                self.runModifier = 1
            if self.stillHolding[0] == 0 and self.stillHolding[1] == 0:
                self.ySpeed = 0
            if self.stillHolding[2] == 0 and self.stillHolding[3] == 0:
                self.xSpeed = 0
            if self.xSpeed == 0 and self.ySpeed == 0:
                self.moving = 0
            if self.moving == 0 and self.attacking == 0 and self.y == self.z:
                self.setSprite(self.boy['idle'])
                self.running = 0
            if self.running == 1 and self.datkAnim == 0:
                self.setSprite(self.boy['run'])
            elif self.running == 0 and self.moving > 0:
                self.setSprite(self.boy['walk'])
        if self.punch1Anim == 18:
            oHtbxPunch1 = Hitbox(self.x+4*self.x_scale,self.y-44,"punch1",self)
            self.game.createInstance(oHtbxPunch1)
            oHtbxPunch1.setFlipped(self._flipped_x,0)
        if self.punch1Anim > 0:
            self.punch1Anim -= 1
            self.setSprite(self.boy['punch1'])
        if self.punch2Anim == 24:
            oHtbxPunch2 = Hitbox(self.x+4*self.x_scale,self.y-44,"punch2",self)
            self.game.createInstance(oHtbxPunch2)
            oHtbxPunch2.setFlipped(self._flipped_x,0)
        if self.punch2Anim > 0:
            self.punch2Anim -= 1
            self.setSprite(self.boy['punch2'])
        if self.kickAnim == 24:
            oHtbxKick = Hitbox(self.x+4*self.x_scale,self.y-32,"kick",self)
            self.game.createInstance(oHtbxKick)
            oHtbxKick.setFlipped(self._flipped_x,0)
        if self.kickAnim > 0:
            self.kickAnim -= 1
            self.setSprite(self.boy['kick'])
        if self.akickAnim == 14:
            oHtbxAkick = Hitbox(self.x+4*self.x_scale,self.y-30,"akick",self)
            self.game.createInstance(oHtbxAkick)
            oHtbxAkick.setFlipped(self._flipped_x,0)
        if self.akickAnim > 0:
            self.akickAnim -= 1
            self.setSprite(self.boy['akick'])
        if self.datkAnim == 21:
            oHtbxDatk = Hitbox(self.x,self.y-30,"datk",self)
            self.game.createInstance(oHtbxDatk)
            oHtbxDatk.setFlipped(self._flipped_x,0)
        if self.datkAnim > 6:
            self.datkAnim -= 1
            self.setSprite(self.boy['datk'])
            self.move(self.xDashSpeed*self.runModifier,self.yDashSpeed*self.runModifier)
            self.z += self.yDashSpeed*self.runModifier
        elif self.datkAnim <= 6 and self.datkAnim > 0:
            self.runModifier = 1
            self.datkAnim -= 1
            self.setSprite(self.boy['datk'])
        for i in range(0,len(self.listRunClock)):
            if self.listRunClock[i] > 0:
                self.listRunClock[i] -= 1
        if self.y < self.z:
            self.jumpSpeed -= self.gravity
            self.move(0,-self.jumpSpeed)
            if self.jumpSpeed >= 0 and self.attacking == 0:
                self.setSprite(self.boy['jump'])
                if self.boy['jump'].index == 5:
                    self.boy['jump'].index = 4
            elif self.jumpSpeed < 0 and self.attacking == 0:
                self.setSprite(self.boy['land'])
        if self.y > self.z:
            self.y = self.z
            self.aKickAnim = 0
        if keys[K_SPACE] and self.jumpRelease == 0 and self.jumpSpeed > 0:
            self.jumpSpeed += .125
        self.move(self.xSpeed*self.runModifier,self.ySpeed*self.runModifier)
        self.z += self.ySpeed*self.runModifier
        self.setDepth(-self.z)
        self.shadow.y = self.z-6
        if self.sprite.flipx == 0:
            self.shadow.x = self.x-19
        elif self.sprite.flipx == 1:
            self.shadow.x = self.x-15

class HUD(pygmi.Object):

    def __init__(self,x,y,character):
        self.hp = str(character.hp)
        self.character = character
        self.sprHP = pygmi.Sprite(pygmi.Tools.makeText(self.hp,None,None,None),0,0,0,0)
        super().__init__(x,y)

    def event_create(self):
        self.setSprite(self.sprHP)

    def update(self):
        if self.character.hp != self.hp:
            self.setSprite(pygmi.Sprite(pygmi.Tools.makeText(self.character.hp,None,None,None),0,0,0,0))
            self.hp = self.character.hp
import pygmi, pygame
from pygame.locals import *
from universal import Hitbox
from flare import Flare
from enemies import Apathol
from ally import Ally

class Character(Ally):

    def __init__(self,x,y,shadow,game):
        self.game = game
        self.shadow = shadow
        self.xSpeed = 0
        self.ySpeed = 0
        self.x_scale = 1
        self.weight = 1
        self.hp = 25
        self.maxHP = 30
        self.wp = 25
        self.maxWP = 30
        self.wpRegen = .01
        self.emp = 30
        self.maxEMP = 30
        self.ally = None
        self.xDashSpeed = 0
        self.yDashSpeed = 0
        self.runModifier = 1
        self.dominantX = 0
        self.dominantY = 0
        self.stillHolding = [0, 0, 0, 0]
        self.running = 0
        self.listRunClock = [0, 0, 0, 0]
        self.attacking = 0
        self.recoilTime = 15
        self.guard = 25
        self.maxGuard = 30
        self.guardRegen = .01
        self.guarding = 0
        self.moving = 0
        self.jumpRelease = 0
        self.jumpSpeed = 0
        self.maxJumpSpeed = 5
        self.gravity = .4
        self.punch1Anim = 0
        self.punch2Anim = 0
        self.kickAnim = 0
        self.datkAnim = 0
        self.akickAnim = 0
        self.throwAnim = 0
        self.guardAnim = 0
        super().__init__(x,y)

    def event_create(self):
        sprIdle = pygmi.Sprite(self.assets.images["char"]["boy_idle"],30,64,-18,-64)
        sprIdle.setFrameTime(30)
        sprWalk = pygmi.Sprite(self.assets.images["char"]["boy_walk"],30,66,-18,-66)
        sprWalk.setFrameTime(8)
        sprRun = pygmi.Sprite(self.assets.images["char"]["boy_run"],44,68,-22,-70)
        sprRun.setFrameTime(5)
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
        sprThrow = pygmi.Sprite(self.assets.images["char"]["boy_throw"],30,64,-18,-64)
        sprThrow.setFrameTime(2)
        sprGuard = pygmi.Sprite(self.assets.images["char"]["boy_guard"],30,62,-18,-62)
        sprGuard.setFrameTime(0)
        sprRecoilB = pygmi.Sprite(self.assets.images["char"]["boy_recoilb"],36,62,-22,-62)
        sprRecoilB.setFrameTime(5)
        sprRecoilF = pygmi.Sprite(self.assets.images["char"]["boy_recoilf"],36,64,-16,-64)
        sprRecoilF.setFrameTime(5)
        sprDeath = pygmi.Sprite(self.assets.images["char"]["boy_death"],68,64,-18,-64)
        sprDeath.setFrameTime(8)
        self.sprShadowLoss = pygmi.Sprite(self.assets.images["char"]["boy_shadowloss.png"],70,10,0,0)
        self.boy = {'idle':sprIdle,'walk':sprWalk,'run':sprRun,'punch1':sprPunch1,
                    'punch2':sprPunch2,'kick':sprKick,'datk':sprDatk,'jump':sprJump,
                    'land':sprLand,'akick':sprAkick,'throw':sprThrow,'guard':sprGuard,
                    'recoilb':sprRecoilB,'recoilf':sprRecoilF,'death':sprDeath}

    def event_keyPressed(self,key):
        if self.recoilAnim == 0 and self.dead == 0:
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
            if key == K_k:
                if self.y == self.z:
                    if self.moving == 0:
                        if self.attacking == 0 and self.wp >= 5:
                            self.boy['throw'].index = 0
                            self.throwAnim = 20
                            self.wp -= 5
            if key == K_LSHIFT:
                if self.y == self.z and self.moving == 0 and self.attacking == 0:
                    self.boy['guard'].index = 0
                    self.guarding = 1
                    self.guardAnim = 6
            if key == K_SPACE and self.attacking == 0:
                if self.y == self.z:
                    self.jumpRelease = 0
                    self.jumpSpeed = self.maxJumpSpeed
                    self.move(0,-self.jumpSpeed)
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
        if key == K_LSHIFT:
            self.guarding = 0
            self.guardAnim = 0
        if key == K_SPACE:
            self.jumpRelease = 1

    def event_collision(self,other):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.attacking = (self.punch1Anim + self.punch2Anim + self.kickAnim + self.datkAnim
            + self.akickAnim + self.throwAnim + self.guarding)
        if self.recoilAnim == 0 and self.attacking == 0 and self.dead == 0:
            if keys[K_w] and self.dominantY != 2 and self.stillHolding[0] == 1:
                if self.z + self.ySpeed*self.runModifier > self.room.boundY_min:
                    self.ySpeed = -2
                else:
                    self.ySpeed = 0
                    if self.y < self.z:
                        self.z = self.room.boundY_min
                    if self.y >= self.z:
                        self.z = self.y = self.room.boundY_min
                        self.moving = 0
                        self.running = 0
                        self.runModifier = 1
                    if self.moving == 0:
                        self.setSprite(self.boy['idle'])
            if keys[K_s] and self.dominantY != 1 and self.stillHolding[1] == 1:
                if self.z + self.ySpeed*self.runModifier < self.room.boundY_max:
                    self.ySpeed = 2
                else:
                    self.ySpeed = 0
                    if self.y < self.z:
                        self.z = self.room.boundY_max
                    if self.y >= self.z:
                        self.z = self.y = self.room.boundY_max
                        self.moving = 0
                        self.running = 0
                        self.runModifier = 1
                    if self.moving == 0:
                        self.setSprite(self.boy['idle'])
            if keys[K_a] and self.dominantX != 2 and self.stillHolding[2] == 1:
                if self.x + self.xSpeed*self.runModifier > self.room.boundX_min:
                    self.xSpeed = -3
                    self.x_scale = -1
                else:
                    self.x = self.room.boundX_min
                    self.xSpeed = 0
                    if self.y >= self.z:
                        self.moving = 0
                        self.running = 0
                        self.runModifier = 1
                        self.setSprite(self.boy['idle'])
            if keys[K_d] and self.dominantX != 1 and self.stillHolding[3] == 1:
                if self.x + self.xSpeed*self.runModifier < self.room.boundX_max:
                    self.xSpeed = 3
                    self.x_scale = 1
                else:
                    self.x = self.room.boundX_max
                    self.xSpeed = 0
                    if self.y >= self.z:
                        self.moving = 0
                        self.running = 0
                        self.runModifier = 1
                        self.setSprite(self.boy['idle'])
        self.moving = abs(self.xSpeed) + abs(self.ySpeed)
        if self.recoilAnim == 0:
            if self.datkAnim == 0:
                if not (keys[K_a] or keys[K_d] or keys[K_w] or keys[K_s]) and self.y == self.z:
                    self.runModifier = 1
                if self.stillHolding[0] == 0 and self.stillHolding[1] == 0:
                    self.ySpeed = 0
                if self.stillHolding[2] == 0 and self.stillHolding[3] == 0:
                    self.xSpeed = 0
                if self.xSpeed == 0 and self.ySpeed == 0:
                    self.moving = 0
                if (self.moving == 0 and self.attacking == 0 and self.y == self.z and
                        not (keys[K_a] or keys[K_d] or keys[K_w] or keys[K_s])):
                    self.setSprite(self.boy['idle'])
                    self.running = 0
                if self.running == 1 and self.datkAnim == 0:
                    self.setSprite(self.boy['run'])
                elif self.running == 0 and self.moving > 0:
                    self.setSprite(self.boy['walk'])
            if self.punch1Anim == 18:
                oHtbxPunch1 = Hitbox(self.x+4*self.x_scale,self.y-44,"boy_punch1",self)
                self.game.createInstance(oHtbxPunch1)
                oHtbxPunch1.setFlipped(self._flipped_x,0)
            if self.punch1Anim > 0:
                self.punch1Anim -= 1
                self.setSprite(self.boy['punch1'])
            if self.punch2Anim == 24:
                oHtbxPunch2 = Hitbox(self.x+4*self.x_scale,self.y-44,"boy_punch2",self)
                self.game.createInstance(oHtbxPunch2)
                oHtbxPunch2.setFlipped(self._flipped_x,0)
            if self.punch2Anim > 0:
                self.punch2Anim -= 1
                self.setSprite(self.boy['punch2'])
            if self.kickAnim == 18:
                oHtbxKick = Hitbox(self.x+4*self.x_scale,self.y-32,"boy_kick",self)
                self.game.createInstance(oHtbxKick)
                oHtbxKick.setFlipped(self._flipped_x,0)
            if self.kickAnim > 0:
                self.kickAnim -= 1
                self.setSprite(self.boy['kick'])
            if self.akickAnim == 14:
                oHtbxAkick = Hitbox(self.x+4*self.x_scale,self.y-30,"boy_akick",self)
                self.game.createInstance(oHtbxAkick)
                oHtbxAkick.setFlipped(self._flipped_x,0)
            if self.akickAnim > 0:
                self.akickAnim -= 1
                self.setSprite(self.boy['akick'])
            if self.datkAnim == 21:
                oHtbxDatk = Hitbox(self.x,self.y-30,"boy_datk",self)
                self.game.createInstance(oHtbxDatk)
                oHtbxDatk.setFlipped(self._flipped_x,0)
            if self.datkAnim > 6:
                self.datkAnim -= 1
                self.setSprite(self.boy['datk'])
                if self.x + self.xDashSpeed*self.runModifier > self.room.boundX_max:
                    self.x = self.room.boundX_max
                elif self.x + self.xDashSpeed*self.runModifier < self.room.boundX_min:
                    self.x = self.room.boundX_min
                else:
                    self.move(self.xDashSpeed*self.runModifier,0)
                if self.y + self.yDashSpeed*self.runModifier > self.room.boundY_max:
                    self.z = self.y = self.room.boundY_max
                elif self.y + self.yDashSpeed*self.runModifier < self.room.boundY_min:
                    self.z = self.y = self.room.boundY_min
                else:
                    self.move(0,self.yDashSpeed*self.runModifier)
                    self.z += self.yDashSpeed*self.runModifier
            elif self.datkAnim <= 6 and self.datkAnim > 0:
                self.runModifier = 1
                self.datkAnim -= 1
                self.setSprite(self.boy['datk'])
            if self.throwAnim == 20:
                oFlare = Flare(self.x,self.y-34,self._flipped_x,self)
                self.game.createInstance(oFlare)
            if self.throwAnim > 0:
                self.throwAnim -= 1
                self.setSprite(self.boy['throw'])
            if self.guarding == 1 and self.guard >= .1:
                self.setSprite(self.boy['guard'])
                self.guard -= .1
                if self.guardAnim > 0:
                    self.guardAnim -= 1
                    self.boy['guard'].index = 0
                if self.guardAnim == 0:
                    self.boy['guard'].index = 1
            if self.guarding == 1 and self.guard < .1:
                self.guarding = 0
                self.guardAnim = 0
        for i in range(0,len(self.listRunClock)):
            if self.listRunClock[i] > 0:
                self.listRunClock[i] -= 1
        if self.y < self.z:
            self.jumpSpeed -= self.gravity
            self.move(0,-self.jumpSpeed)
            if self.recoilAnim == 0 and self.attacking == 0:
                if self.jumpSpeed >= 0:
                    self.setSprite(self.boy['jump'])
                    if self.boy['jump'].index == 5:
                        self.boy['jump'].index = 4
                elif self.jumpSpeed < 0:
                    self.setSprite(self.boy['land'])
        if self.y > self.z:
            self.y = self.z
            self.aKickAnim = 0
        if keys[K_SPACE] and self.jumpRelease == 0 and self.jumpSpeed > 0:
            self.jumpSpeed += .125
        if self.recoilAnim == self.recoilTime:
            if self.recoilSide == 1:
                self.boy['recoilf'].index = 0
            if self.recoilSide == -1:
                self.boy['recoilb'].index = 0
        if self.recoilAnim > 0:
            if (self.recoilSide == 1 and self._flipped_x == 0) or (self.recoilSide == -1 and self._flipped_x == 1):
                self.setSprite(self.boy['recoilf'])
            if (self.recoilSide == -1 and self._flipped_x == 0) or (self.recoilSide == 1 and self._flipped_x == 1):
                self.setSprite(self.boy['recoilb'])
            self.punch1Anim = 0
            self.punch2Anim = 0
            self.kickAnim = 0
            self.datkAnim = 0
            self.akickAnim = 0
            self.throwAnim = 0
            self.guardAnim = 0
            self.xSpeed = 0
        if self.hp <= 0:
            if self.dead == 0:
                self.dead = 1
                self.deathAnim = 88
                self.xSpeed = 0
                self.ySpeed = 0
            if self.z == self.y:
                if self.deathAnim > 0:
                    self.deathAnim -= 1
                if self.deathAnim == 0:
                    self.boy['death'].index = 80
                if self.deathAnim == 8:
                    self.shadow.setSprite(self.sprShadowLoss)
                self.setSprite(self.boy['death'])
        self.move(self.xSpeed*self.runModifier,self.ySpeed*self.runModifier)
        self.z += self.ySpeed*self.runModifier
        self.setDepth(-self.z)
        self.shadow.y = self.z-6
        if self._flipped_x == 0:
            self.shadow.x = self.x-19
        elif self._flipped_x == 1:
            self.shadow.x = self.x-15
        if self.wp <= self.maxWP - self.wpRegen:
            self.wp += self.wpRegen
        elif self.wp > self.maxWP - self.wpRegen:
            self.wp = self.maxWP
        if self.guard <= self.maxGuard - self.guardRegen and self.guarding == 0:
            self.guard += self.guardRegen
        elif self.guard > self.maxGuard - self.guardRegen and self.guarding == 0:
            self.guard = self.maxGuard
        super().update()


class HUD(pygmi.Object):

    def __init__(self,x,y,character):
        self.character = character
        super().__init__(x,y)

    def event_create(self):
        self.sprHUDfront = pygmi.Sprite(self.assets.images["hud"]["hudfront.png"],800,84,0,0)
        self.sprHUDback = pygmi.Sprite(self.assets.images["hud"]["hudback.png"],800,84,0,0)
        self.sprHeart = pygmi.Sprite(self.assets.images["hud"]["heart.png"],66,52,0,0)
        self.sprWillpower = pygmi.Sprite(self.assets.images["hud"]["willpower.png"],338,8,0,0)
        self.sprEmpathyLine = pygmi.Sprite(self.assets.images["hud"]["empathyline.png"],348,8,0,0)
        self.sprEmpathyTwist = pygmi.Sprite(self.assets.images["hud"]["empathytwist.png"],46,56,0,0)
        self.sprEmpathyJewel = pygmi.Sprite(self.assets.images["hud"]["empathyjewel.png"],10,14,0,0)
        self.sprGuard = pygmi.Sprite(self.assets.images["hud"]["guard.png"],46,16,0,0)
        self.sprClosed = pygmi.Sprite(self.assets.images["hud"]["closed.png"],62,22,0,0)

    def event_render(self):
        back = self.sprHUDback.image
        front = self.sprHUDfront.image
        heart = self.sprHeart.image
        willpower = self.sprWillpower.image
        empathyLine = self.sprEmpathyLine.image
        empathyTwist = self.sprEmpathyTwist.image
        empathyJewel = self.sprEmpathyJewel.image
        guard = self.sprGuard.image
        closed = self.sprClosed.image
        rectHeart = Rect(0,52-52*self.character.hp/self.character.maxHP,66,52)
        rectWillpower = Rect(338-338*self.character.wp/self.character.maxWP,0,338,8)
        if self.character.emp <= .8*self.character.maxEMP:
            rectEmpathyLine = Rect(0,0,348*self.character.emp/(self.character.maxEMP*.8),8)
            rectEmpathyTwist = Rect(0,0,0,0)
        if self.character.emp > .8*self.character.maxEMP:
            rectEmpathyLine = Rect(0,0,348,8)
            rectEmpathyTwist = Rect(0,56-56*(self.character.emp-self.character.maxEMP*.8)/(self.character.maxEMP*.2),46,56)
        rectGuard = Rect (0,16-16*self.character.guard/self.character.maxGuard,46,16)
        self.window.blit(back,(self.x,self.y))
        self.window.blit(heart,(self.x+366,self.y+22+52-52*self.character.hp/self.character.maxHP),rectHeart)
        self.window.blit(willpower,(self.x+12+338-338*self.character.wp/self.character.maxWP,self.y+18),rectWillpower)
        self.window.blit(empathyLine,(self.x+432,self.y+70),rectEmpathyLine)
        self.window.blit(empathyTwist,(self.x+744,self.y+16+56-56*(self.character.emp-self.character.maxEMP*.8)/(self.character.maxEMP*.2)),rectEmpathyTwist)
        if self.character.emp == self.character.maxEMP:
            self.window.blit(empathyJewel,(self.x+762,self.y+26))
        self.window.blit(guard,(self.x+376,self.y+8+16-16*self.character.guard/self.character.maxGuard),rectGuard)
        if self.character.ally == None:
            self.window.blit(closed,(self.x+620,self.y+46))
        if self.character.guarding == 1:
             self.window.blit(guard,(self.character.x-23-self.room.viewx,self.character.y-84+16-16*self.character.guard/self.character.maxGuard),rectGuard)
        self.window.blit(front,(self.x,self.y))

'''
Created on May 9, 2013

@author: Catt
@version: 1.000
'''

import pygame, os, sys, math
from pygame.locals import *

class Tools(object):

    C_BLACK = pygame.Color(0,0,0)
    C_WHITE = pygame.Color(255,255,255)
    C_YELLOW = pygame.Color(255,255,0)
    C_RED = pygame.Color(255,0,0)
    C_CKTRANSPARENT = pygame.Color(255,1,255)

    @staticmethod
    def isCollision(obj1,obj2):
        if obj1 == obj2:
            return False
        box1 = obj1.bbox
        box2 = obj2.bbox
        return not(obj1.y + box1.bottom() < obj2.y + box2.top()
                    or obj1.y + box1.top() > obj2.y + box2.bottom()
                    or obj1.x + box1.left() > obj2.x + box2.right()
                    or obj1.x + box1.right() < obj2.x + box2.left())

    @staticmethod
    def makeText(text,size,color,fontname):
        if not size:
            size = 15
        if not color:
            color = Tools.C_WHITE
        if not fontname:
            fontname = "monospace"
        if not text:
            raise Exception("(PyGMi Error) Tools.makeText must take a string as its first parameter.")
        font = pygame.font.SysFont(fontname, size)
        return font.render(str(text), 1, color)

class Pygmi(object):
    '''
    Pygmi represents your game. Creating a Pygmi object will automatically initialize pygame
    and create a window based on the parameters: Pygmi((w,h),caption,flags)
    Pygmi's main use is to store and control rooms.
    '''

    clrBlack = pygame.Color(0,0,0)

    def __init__(self,dimensions,caption, flags):
        pygame.init()
        self._debug = True
        self.rooms = {}
        self.activeRoom = None
        self.fpsmax = 60
        self.window = pygame.display.set_mode(dimensions,flags)
        self.fpsClock = pygame.time.Clock()
    def addRoom(self,room):
        self.rooms[room.name] = room
    def gotoRoom(self,roomName):
        self.activeRoom = self.rooms[roomName]
    def createInstance(self,obj):
        self.activeRoom.addToRoom(obj)
        obj.event_create()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        if self.activeRoom:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == MOUSEBUTTONDOWN:
                    self.activeRoom.event_mouseDown(event.button,event.pos)
                if event.type == MOUSEBUTTONUP:
                    self.activeRoom.event_mouseUp(event.button,event.pos)
                if event.type == KEYDOWN:
                    self.activeRoom.event_keyPressed(event.key)
                if event.type == KEYUP:
                    self.activeRoom.event_keyReleased(event.key)
            self.activeRoom.update()
        self.fpsClock.tick(self.fpsmax)

    def render(self):
        self.window.fill(Pygmi.clrBlack)
        if self.activeRoom:
            self.activeRoom.render()
        if self._debug:
            self.window.blit(Tools.makeText("FPS:"+str(int(self.fpsClock.get_fps())),None,None,None),(0,0))

    def paint(self):
        pygame.display.update()



class Room(object):
    '''
    The room is the stage on which all objects interact.
    Use addToRoom(obj) to add an object to the room. Once the room is active,
    it will call the update and render functions of all objects, as well as
    event functions.
    '''

    def __init__(self,name,w,h):
        self.name = name
        self.w = w
        self.h = h
        self.viewx = 0
        self.viewy = 0
        self.vieww = 0
        self.viewh = 0
        self.lRender = []
        self.lUpdate = []
        self.coltree = CollisionTree(0,Bbox(0,0,w,h))
        self.lCollision = []
        self.renderCulling = False

    def addToRoom(self,obj):
        self.lUpdate.append(obj)
        if obj.isVisible():
            self.lRender.append(obj)
            obj._visiblechange = False
        if obj.isSolid():
            self.lCollision.append(obj)
            obj._solidchange = False

    def setView(self,x,y,w,h):
        self.viewx = x
        self.viewy = y
        self.vieww = w
        self.viewh = h

    def moveView(self,x,y):
        self.viewx += x
        self.viewy += y

    def zoomView(self,w,h):
        self.vieww += w
        self.viewh += h

    def setRenderCulling(self,isCulled):
        self.renderCulling = isCulled

    def event_mouseDown(self,button,position):
        for obj in self.lUpdate:
            obj.event_mouseDown(button,position)

    def event_mouseUp(self,button,position):
        for obj in self.lUpdate:
            obj.event_mouseUp(button,position)

    def event_keyPressed(self,key):
        for obj in self.lUpdate:
            obj.event_keyPressed(key)

    def event_keyReleased(self,key):
        for obj in self.lUpdate:
            obj.event_keyReleased(key)

    def collideAll(self):
        colcount = 0
        indexi = 0
        indexj = 1
        for obji in self.lCollision:
            if not obji._destroyed:
                self.lCollision[indexi] = obji
                indexi += 1
                for j in range(indexj,len(self.lCollision)):
                    colcount += 1
                    if Tools.isCollision(obji,self.lCollision[j]):
                        obji.event_collision(self.lCollision[j])
                        self.lCollision[j].event_collision(obji)
            indexj += 1
        del self.lCollision[indexi:]

    def collideTree(self):
        colcount = 0
        self.coltree.clear()
        index = 0
        for obj in self.lCollision:
            if not obj._destroyed:
                if obj.isSolid():
                    self.coltree.insert(obj)
                    self.lCollision[index] = obj
                    index += 1
        del self.lCollision[index:]
        for obj in self.lCollision:
            lNearby = self.coltree.allNearby(obj)
            for other in lNearby:
                colcount += 1
                if Tools.isCollision(obj,other):
                    obj.event_collision(other)
                    other.event_collision(obj)
            self.coltree.remove(obj)

    def update(self):
        index = 0
        for obj in self.lUpdate:
            if not obj._destroyed:
                if obj._solidchange:
                    obj._solidchange = False
                    if obj.isSolid():
                        self.lCollision.append(obj)
                if obj._visiblechange:
                    obj._visiblechange = False
                    if obj.isVisible():
                        self._renderInsert(obj)
                self.lUpdate[index] = obj
                index += 1
                obj.update()
        del self.lUpdate[index:]
        self.collideTree()

    def _renderInsert(self,obj):
        i = 0
        while i < len(self.lRender):
            if self.lRender[i].depth < obj.depth:
                self.lRender.insert(i, obj)
                return
            i += 1
        self.lRender.append(obj)

    def render(self):
        sort = False
        index = 0
        for obj in self.lRender:
            if not obj._destroyed:
                if obj.isVisible():
                    self.lRender[index] = obj
                    if obj._depthchange:
                        sort = True
                        obj._depthchange = False
                    index += 1
                    if self.renderCulling == False:
                        obj.render(self.viewx,self.viewy,self.vieww,self.viewh)
                    elif ((obj.x+obj.sprite.x+obj.sprite.w) - self.viewx > 0 and (obj.y+obj.sprite.y+obj.sprite.h) - self.viewy > 0
                          and (obj.x+obj.sprite.x) - self.viewx < self.w and (obj.y+obj.sprite.y) - self.viewy < self.h):
                        obj.render(self.viewx,self.viewy,self.vieww,self.viewh)
        del self.lRender[index:]
        if sort:
            self.lRender = self._mergesort(self.lRender)

    def _mergesort(self,unsorted):
        if len(unsorted) <= 1:
            return unsorted
        mid = int(len(unsorted)/2)
        left = self._mergesort(unsorted[:mid])
        right = self._mergesort(unsorted[mid:])
        return self._merge(left,right)

    def _merge(self,left,right):
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i].depth >= right[j].depth:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result


class SoundManager(object):
    '''
    The SoundManager takes a directory pathname and loads all sounds in that directory and its subdirectories.
    It stores sounds in a dictionary, allowing them to be accessed by their filename (without the extension).
    '''

    def __init__(self):
        self.sounds = {}

    def loadMusic(self,musicPath):
        if os.path.isfile(musicPath):
            pygame.mixer.music.load(musicPath)
        else:
            raise Exception("(PyGMi Error) loadMusic must take a filepath string of a sound as its parameter.")

    def playMusic(self,loop):
        pygame.mixer.music.play(loop,0.0)

    def stopMusic(self):
        pygame.mixer.music.stop()

    def loadSounds(self,soundPath):
        if os.path.isfile(soundPath):
            self.sounds[os.path.basename(soundPath)] = pygame.image.load(soundPath)
        elif os.path.isdir(soundPath):
            for f in os.listdir(soundPath):
                self.loadSounds(soundPath+"/"+f)
        else:
            raise Exception("(PyGMi Error) loadSounds must take a filepath string of a sound or a directory as its parameter.")

    def playSound(self,name):
        self.sounds[name].play()

    def stopSound(self,name):
        self.sounds[name].stop()

class Sprite(object):
    '''
    The Sprite tracks an image and its bounding box.
    It's relatively straight forward.
    '''

    def __init__(self,pathOrSurfaces,x,y,w,h):
        self.image = None
        self.images = []
        self.alphas = []
        self.x = x;
        self.y = y;
        self.w = w;
        self.h = h;
        self.frameTime = 1
        self.index = 0
        self.flipx = False
        self.flipy = False
        self.loadImages(pathOrSurfaces)

    def loadImages(self,pathOrSurfaces):
        if isinstance(pathOrSurfaces,str) == False:
            if hasattr(pathOrSurfaces,"__iter__"):
                for item in pathOrSurfaces:
                    self.loadImages(item)
            elif type(pathOrSurfaces) == pygame.Surface:
                self.image = pathOrSurfaces
                self.images.append(pathOrSurfaces)
        else:
            if os.path.isfile(pathOrSurfaces):
                self.image = pygame.image.load(pathOrSurfaces)
                self.images.append(self.image)
            elif os.path.isdir(pathOrSurfaces):
                for f in os.listdir(pathOrSurfaces):
                    self.images.append(pygame.image.load(pathOrSurfaces+"/"+f))
                self.index = 0
                self.image = self.images[0]
            else:
                raise Exception("(PyGMi Error) loadImage's parameter wasn't a filepath, directory, Pygame Surface, or sequence thereof.")
        if len(self.images) < 2:
            self.frameTime = 0

    def loadAlphaMasks(self,pathOrSurfaces):
        if isinstance(pathOrSurfaces,str) == False:
            if hasattr(pathOrSurfaces,"__iter__"):
                for item in pathOrSurfaces:
                    self.loadAlphaMasks(item)
            elif type(pathOrSurfaces) == pygame.Surface:
                self.alphas.append(pathOrSurfaces)
        else:
            if os.path.isfile(pathOrSurfaces):
                self.images.append(pygame.image.load(pathOrSurfaces))
            elif os.path.isdir(pathOrSurfaces):
                for f in os.listdir(pathOrSurfaces):
                    self.alphas.append(pygame.image.load(pathOrSurfaces+"/"+f))
            else:
                raise Exception("(PyGMi Error) loadAlphaMasks' parameter wasn't a filepath, directory, Pygame Surface, or sequence thereof.")
        for i,alpha in enumerate(self.alphas):
            for j in range(0,alpha.get_width()):
                for k in range(0,alpha.get_height()):
                    c = alpha.get_at(j,k)
                    value = math.floor((c.r + c.g + c.b)/3)
                    c = self.images[i].get_at((j,k))
                    c.a = value
                    self.images[i].set_at((j,k),c)

    def setAlphaKey(self,color):
        for image in self.images:
            image.set_colorkey(color)

    def setAlpha(self,value):
        for image in self.images:
            image.set_alpha(value)

    def setFlipped(self,flipped_x,flipped_y):
        if self.flipx != flipped_x:
            self.x = -(self.x + self.w)
        if self.flipy != flipped_y:
            self.y = -(self.y + self.h)
        self.flipx = flipped_x
        self.flipy = flipped_y

    def setFrameTime(self,frameTime):
        self.frameTime = frameTime

    def render(self):
        if self.frameTime:
            self.image = self.images[math.floor(self.index/self.frameTime)]
            if self.index < (len(self.images) * self.frameTime) - 1:
                self.index += 1
            else:
                self.index = 0
        else:
            self.image = self.images[self.index]



class Object(object):
    '''
    Object should not be used directly, but should be inherited by any class which controls
    an in-game object. By overriding the event_ functions, you can create your own functions
    which will be automatically called when an event occurs.
    NOTE: If you want to add new events to pygmi, you must do the following:
    1) Have Pygmi check for the event's occurrence, then call the event function in the active room.
    2) Design the active room's event function to call the event function (by the same name) for all
       objects in that room. (If the event has frequent calls for a specific subset of objects, it
       may be advantageous to create a list just for those objects)
    3) Add the event function to the Object class, but leave it empty since it will be overridden.
    '''

    def __init__(self,sprite,x,y):
        self.x = x;
        self.y = y;
        self.sprite = sprite
        if sprite:
            self.bbox = Bbox(sprite.x,sprite.y,sprite.w,sprite.h)
        else:
            self.bbox = Bbox(0,0,0,0)
        self.solid = False
        self.visible = True
        self.depth = 0;
        self._destroyed = False
        self._depthchange = False
        self._solidchange = False
        self._visiblechange = False

    def setSprite(self,sprite):
        self.sprite = sprite

    def setX(self,x):
        self.x = x;

    def setY(self,y):
        self.y = y;

    def setPosition(self,x,y):
        self.x = x;
        self.y = y;

    def setBbox(self,x,y,w,h):
        self.bbox = Bbox(x,y,w,h)

    def setSolid(self,solid):
        self.solid = solid
        self._solidchange = True

    def setVisible(self,visible):
        self.visible = visible
        self._visiblechange = True

    def setDepth(self,depth):
        self.depth = depth
        self._depthchange = True

    def setFlipped(self,flipped_x,flipped_y):
        if self.sprite:
            self.sprite.setFlipped(flipped_x,flipped_y)
        if self.bbox:
            self.bbox.setFlipped(flipped_x, flipped_y)

    def isSolid(self):
        return self.solid

    def isVisible(self):
        return self.visible

    def destroy(self):
        self.event_destroy()
        self._destroyed = True

    def event_mouseDown(self,button,position):
        pass

    def event_mouseUp(self,button,position):
        pass

    def event_keyPressed(self,key):
        pass

    def event_keyReleased(self,key):
        pass

    def event_create(self):
        pass

    def event_destroy(self):
        pass

    def event_collision(self,other):
        pass

    def update(self):
        pass

    def render(self,viewx,viewy,vieww,viewh):
        if self.visible and self.sprite:
            self.sprite.render()
            img = pygame.transform.flip(self.sprite.image,self.sprite.flipx,self.sprite.flipy)
            #pygame.transform.scale(img, (width, height))
            pygame.display.get_surface().blit(img,(self.x + self.sprite.x-viewx,self.y + self.sprite.y-viewy))

class Bbox(object):

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.flipx = False
        self.flipy = False

    def top(self):
        return self.y

    def bottom(self):
        return self.y+self.h

    def left(self):
        return self.x

    def right(self):
        return self.x+self.w

    def setFlipped(self,flipped_x,flipped_y):
        if self.flipx != flipped_x:
            self.x = -(self.x + self.w)
        if self.flipy != flipped_y:
            self.y = -(self.y + self.h)
        self.flipx = flipped_x
        self.flipy = flipped_y


class CollisionTree(object):
    MAX_OBJECTS = 10
    MAX_LEVELS = 5

    def __init__(self,level,bounds):
        self.level = level
        self.bounds = bounds
        self.objects = []
        self.nodes = [None,None,None,None]

    def clear(self):
        self.objects = []
        for node in self.nodes:
            if node:
                node.clear()
                node = None

    def split(self):
        sw = self.bounds.w/2
        sh = self.bounds.h/2
        x = self.bounds.x
        y = self.bounds.y
        self.nodes[0] = CollisionTree(self.level+1,Bbox(x+sw,y,sw,sh))
        self.nodes[1] = CollisionTree(self.level+1,Bbox(x,y,sw,sh))
        self.nodes[2] = CollisionTree(self.level+1,Bbox(x,y+sh,sw,sh))
        self.nodes[3] = CollisionTree(self.level+1,Bbox(x+sw,y+sh,sw,sh))

    def join(self):
        pass

    def getQuadrant(self,obj):
        b = obj.bbox
        quadrant = -1
        vMid = self.bounds.x + self.bounds.w/2
        hMid = self.bounds.y + self.bounds.h/2
        tQuad = (obj.y + b.y < hMid and obj.y + b.y + b.h < hMid)
        bQuad = (obj.y + b.y > hMid)
        lQuad = (obj.x + b.x < vMid and obj.x + b.x + b.w < vMid)
        rQuad = (obj.x + b.x > vMid)
        if lQuad:
            if tQuad:
                quadrant = 1
            elif bQuad:
                quadrant = 2
        elif rQuad:
            if tQuad:
                quadrant = 0
            elif bQuad:
                quadrant = 3

        return quadrant

    def insert(self,obj):
        if self.nodes[0]:
            quad = self.getQuadrant(obj)
            if quad != -1:
                self.nodes[quad].insert(obj)
                return

        self.objects.append(obj)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if not self.nodes[0]:
                self.split()
            index = 0
            for obj in self.objects:
                quad = self.getQuadrant(obj)
                if quad != -1:
                    self.nodes[quad].insert(obj)
                else:
                    self.objects[index] = obj
                    index += 1
            del self.objects[index:]

    def allNearby(self,obj):
        lNearby = []
        quad = self.getQuadrant(obj)
        if quad != -1 and self.nodes[0]:
            lNearby.extend(self.nodes[quad].allNearby(obj))
        lNearby.extend(self.objects)
        return lNearby

    def remove(self,obj):
        if self.nodes[0]:
            quad = self.getQuadrant(obj)
            if quad != -1:
                self.nodes[quad].remove(obj)
                return
        self.objects.remove(obj)

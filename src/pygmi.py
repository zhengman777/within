'''
Created: 2013-05-09
Updated: 2013-06-27
@author: Catt
@version: 2.111
'''

from collections import OrderedDict
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
        self._emptyRoom = Room("empty",1,1)
        self.activeRoom = self._emptyRoom
        self.fpsmax = 60
        self.window = pygame.display.set_mode(dimensions,flags)
        self.assets = AssetManager()
        self.fpsClock = pygame.time.Clock()
        self.keys = {}
        for i in range(0,133):
            self.keys[i] = False
    
    def getAssetManager(self):
        return self.assets
    
    def addRoom(self,room):
        self.rooms[room.name] = room
        room.game = self
        room.assets = self.assets
        room.window = self.window
        for obj in room.lUpdate:
            obj.game = self
        
    def gotoRoom(self, roomName):
        self.activeRoom = self.rooms[roomName]
        self.activeRoom._event_create()
    
    def createInstance(self, obj):
        self.activeRoom._addToRoom(obj)
        obj.game = self
        obj.room = self.activeRoom
        obj.assets = self.assets
        obj.window = self.window
        obj.event_create()
        return obj
    
    def quit(self):
        pygame.quit()
        sys.exit()
        
    def update(self):
        if self.activeRoom:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == MOUSEBUTTONDOWN:
                    self.activeRoom._event_mousePressed(event.button,event.pos)
                if event.type == MOUSEBUTTONUP:
                    self.activeRoom._event_mouseReleased(event.button,event.pos)
                if event.type == KEYDOWN:
                    self.keys[event.key] = True
                    self.activeRoom._event_keyPressed(event.key)
                if event.type == KEYUP:
                    self.keys[event.key] = False
                    self.activeRoom._event_keyReleased(event.key)
                    if event.key == K_ESCAPE:
                        self.quit()
            self.activeRoom._update()
        self.fpsClock.tick(self.fpsmax)
    
    def render(self):
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
        self.game = None
        self.assets = None
        self.window = None
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
        self._updaterects = []
        self.background = None
        
    def _addToRoom(self,obj):
        self.lUpdate.append(obj)
        if obj.isVisible():
            self.lRender.append(obj)
            obj._visiblechange = False
        if obj.isSolid():
            self.lCollision.append(obj)
            obj._solidchange = False
    
    def setBackground(self,surface):
        self.background = surface
    
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
    
    def _event_mousePressed(self,button,position):
        self.event_mousePressed(button,(position[0]+self.viewx,position[1]+self.viewy))
        for obj in self.lUpdate:
            obj.event_mousePressed(button,(position[0]+self.viewx,position[1]+self.viewy))
    
    def _event_mouseReleased(self,button,position):
        self.event_mouseReleased(button,(position[0]+self.viewx,position[1]+self.viewy))
        for obj in self.lUpdate:
            obj.event_mouseReleased(button,(position[0]+self.viewx,position[1]+self.viewy))
    
    def _event_keyPressed(self,key):
        self.event_keyPressed(key)
        for obj in self.lUpdate:
            obj.event_keyPressed(key)
    
    def _event_keyReleased(self,key):
        self.event_keyReleased(key)
        for obj in self.lUpdate:
            obj.event_keyReleased(key)
   
    def _event_create(self):
        self.event_create()
        for obj in self.lUpdate:
            obj.event_create()
    
    def event_mousePressed(self,button,position):
        pass
    
    def event_mouseReleased(self,button,position):
        pass
            
    def event_keyPressed(self,key):
        pass
    
    def event_keyReleased(self,key):
        pass
    
    def event_create(self):
        pass
    
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
        pass
    
    def _update(self):
        self.update()
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
        if self.background:
            self.window.blit(self.background,(0,0))
        else:
            self.window.fill(Pygmi.clrBlack)
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
                    elif ((obj.x+obj._s_x+obj.sprite.w) - self.viewx > 0 and (obj.y+obj._s_y+obj.sprite.h) - self.viewy > 0 
                          and (obj.x+obj._s_x) - self.viewx < self.w and (obj.y+obj._s_y) - self.viewy < self.h):
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

    
class AssetManager(object):
    '''
    The SoundManager takes a directory pathname and loads all sounds in that directory and its subdirectories.
    It stores sounds in a dictionary, allowing them to be accessed by their filename (without the extension).
    '''
    
    def __init__(self):
        self.sounds = OrderedDict()
        self.images = OrderedDict()
        self.images = self.loadImages("img")
        self.loadSounds("snd")
        
    def loadImages(self,imagePath,dct = OrderedDict()):
        if os.path.isfile(imagePath):
            img = pygame.image.load(imagePath)
            dct[os.path.basename(imagePath)] = img.convert_alpha()
            return dct
        elif os.path.isdir(imagePath):
            if imagePath != "img":
                dct[os.path.basename(imagePath)] = OrderedDict()
                for f in os.listdir(imagePath):
                    self.loadImages(imagePath+"/"+f,dct[os.path.basename(imagePath)])
            else:
                for f in os.listdir(imagePath):
                    self.loadImages(imagePath+"/"+f,dct)
            return dct
        else:
            raise Exception("(PyGMi Error) AssetManager.loadImages says ",imagePath," is not a file or directory.")
    
    def loadMusic(self,musicPath):
        if os.path.isfile(musicPath):
            pygame.mixer.music.load(musicPath)
        else:
            raise Exception("(PyGMi Error) AssetManager.loadMusic must take a filepath string of a sound as its parameter.")
    
    def playMusic(self,loop):
        pygame.mixer.music.play(loop,0.0)
    
    def stopMusic(self):
        pygame.mixer.music.stop()
    
    def loadSounds(self,soundPath):
        if os.path.isfile(soundPath):
            self.sounds[os.path.basename(soundPath)] = pygame.mixer.Sound(soundPath)
        elif os.path.isdir(soundPath):
            for f in os.listdir(soundPath):
                self.loadSounds(soundPath+"/"+f)
        else:
            raise Exception("(PyGMi Error) AssetManager.loadSounds says ",soundPath,"is not a file or directory.")
        
    def playSound(self,name,loops):
        self.sounds[name].play(loops)
    
    def stopSound(self,name):
        self.sounds[name].stop()
        
class Sprite(object): 
    '''
    The Sprite tracks an image.
    It's relatively straight forward.
    ''' 
    
    def __init__(self,pathOrSurfaces,w,h,x=None,y=None):
        self.image = None
        self.images = []
        self.alphas = []
        self.x = x;
        self.y = y;
        self.w = w;
        self.h = h;
        self.index = 0
        self.flipx = False
        self.flipy = False
        self.angle = 0
        self.loadImages(pathOrSurfaces)
        if len(self.images) < 2:
            self.frameTime = 0
        else:
            self.frameTime = 1

    def loadImages(self,pathOrSurfaces):
        if isinstance(pathOrSurfaces,str) == False:
            if hasattr(pathOrSurfaces,"__iter__"):
                if isinstance(pathOrSurfaces,dict):
                    for key in pathOrSurfaces:
                        self.loadImages(pathOrSurfaces[key])
                else:
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
                raise Exception("(PyGMi Error) loadImage says ",pathOrSurfaces," is not a file, directory, Surface or iterable container.")
        #Convert images for optimal display time.
        if self.image:
            self.image = self.image.convert_alpha()
            #Autoset the sprite's w and h, if necessary.
            if self.w == None:
                self.w = self.image.get_width()
            if self.h == None:
                self.h = self.image.get_height()
        for i in range(0,len(self.images)):
            self.images[i] = self.images[i].convert_alpha()
    
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
        if self.image:
            self.image.set_colorkey(color)
        for image in self.images:
            image.set_colorkey(color)
    
    def setAlpha(self,value):
        if self.image:
            self.image.set_alpha(value)
        for image in self.images:
            image.set_alpha(value)
    
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
    
    def __init__(self,x,y):
        self.game = None
        self.room = None
        self.window = None
        self.assets = None
        self.x = x
        self.y = y
        self.sprite = None
        self.bbox = Bbox(0,0,0,0)
        self.solid = False
        self.visible = True
        self.active = True
        self.depth = 0;
        self._destroyed = False
        self._poschange = False
        self._flipped_x = False
        self._flipped_y = False
        self._angle = 0
        self._s_x = 0 #Sprite X position
        self._s_y = 0 #Sprite Y position
        self._x = x #Previous X position
        self._y = y #Previous Y position
        self._drawchange = False
        self._depthchange = False
        self._solidchange = False
        self._visiblechange = False
        self._activechange = False

    def setSprite(self,sprite,x=None,y=None,autobbox=True):
        #Unflip old sprite
        tempFlip_x = self._flipped_x
        tempFlip_y = self._flipped_y
        self.setFlipped(False,False)
        self.sprite = sprite
        if x != None:
            self._s_x = x
            sprite.x = x
        else:
            if sprite.x != None:
                self._s_x = sprite.x
        if y != None:
            self._s_y = y
            sprite.y = y
        else:
            if sprite.y != None:
                self._s_y = sprite.y
        if sprite and autobbox:
            self._b_x = x
            self._b_y = y
            self.setBbox(x,y,sprite.w,sprite.h)
        self.setFlipped(tempFlip_x, tempFlip_y)
        self._drawchange = True
    
    def setX(self,x):
        self._x = self.x
        self.x = x
        self._poschange = True
        self._drawchange = True
    
    def setY(self,y):
        self._y = self.y
        self.y = y
        self._poschange = True
        self._drawchange = True
    
    def setPosition(self,x,y):
        self._x = self.x
        self._y = self.y
        self.x = x
        self.y = y
        self._poschange = True
        self._drawchange = True
    
    def move(self,x,y):
        self._x = self.x
        self._y = self.y
        self.x += x
        self.y += y
        self._poschange = True
        self._drawchange = True
    
    def setBbox(self,x=None,y=None,w=None,h=None):
        if not x:
            x = self.bbox.x
        if not y:
            y = self.bbox.y
        if not w:
            w = self.bbox.w
        if not h:
            h = self.bbox.h
        self.bbox = Bbox(x,y,w,h)
        
    def setSolid(self,solid):
        self.solid = solid
        self._solidchange = True
        
    def setVisible(self,visible):
        self.visible = visible
        self._visiblechange = True
        self._drawchange = True
        
    def setActive(self,active):
        self.active = active
        self._activechange = True
    
    def setDepth(self,depth):
        self.depth = depth
        self._depthchange = True
        self._drawchange = True
        
    def setFlipped(self,flipped_x,flipped_y, autobbox=True):
        bbox_x = None
        bbox_y = None
        if self._flipped_x != flipped_x:
            self._s_x = -(self._s_x + self.sprite.w)
            bbox_x = -(self.bbox.x + self.bbox.w)
        if self._flipped_y != flipped_y:
            self._s_y = -(self._s_y + self.sprite.h)
            bbox_y = -(self.bbox.y + self.bbox.h)
        self._flipped_x = flipped_x
        self._flipped_y = flipped_y
        if autobbox:
            self.setBbox(bbox_x,bbox_y)
            
    def rotate(self,angle):
        self._angle = angle
    
    def isSolid(self):
        return self.solid
    
    def isVisible(self):
        return self.visible
    
    def isActive(self):
        return self.active
    
    def destroy(self):
        self.event_destroy()
        self._destroyed = True
        self._drawchange = True
    
    def event_mousePressed(self,button,position):
        pass
    
    def event_mouseReleased(self,button,position):
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
        self.event_update()
    
    def event_update(self):
        pass
    
    def render(self,viewx,viewy,vieww,viewh):
        self.event_render()
        if self.visible and self.sprite:
            self.sprite.render()
            img = pygame.transform.flip(self.sprite.image,self._flipped_x,self._flipped_y)
            img = pygame.transform.rotate(img,self._angle)
            self.window.blit(img,(self.x + self._s_x - viewx, self.y + self._s_y - viewy))
    
    def event_render(self):
        pass

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
        
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.Audio3DManager import Audio3DManager
import sys
import datetime

class FPS(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        """ create a FPS type game """
        self.initCollision()
        self.loadLevel()
        self.initPlayer()
        self.iniAudio3d()
        self.initObstacles()
        self.accept( "escape" , sys.exit)
        self.disableMouse()
        
        
    def initCollision(self):
        """ create the collision system """
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addInPattern('into-%in')
        #self.collHandEvent.addOutPattern('outof-%in')
        
    def loadLevel(self):
        """ load the self.level 
            must have
            <Group> *something* { 
              <Collide> { Polyset keep descend } 
            in the egg file
        """
        self.level = loader.loadModel('./models/ground.egg')
        self.level.reparentTo(render)
        self.level.setTwoSided(True)

    def iniAudio3d(self):
        self.audio = Audio3DManager(self.sfxManagerList[0], self.camera)
        self.enable_all_audio()

    def initObstacles(self):
        self.keyObjects = []
        self.keyObjects.append(wayPoint('./models/planet_sphere','./models/earth_1k_tex.jpg','./models/camera-focus-1_mono.wav', 0, 0, 1))
        
    def initPlayer(self):
        """ loads the player and creates all the controls for him"""
        Player()
        self.playerPosMsg = OnscreenText(style=1, fg=(1,1,1,1), pos=(-1.3, 0.95), align=TextNode.ALeft, scale = .05, mayChange=True)
        taskMgr.add(self.displayPos, 'displayPos-task', extraArgs = [render.find('player'), self.playerPosMsg], appendTask = True)
        taskMgr.add(self.logPos, 'logPos-task', extraArgs = [render.find('player'), open("./player_pos_.csv", "a")], appendTask = True)
    
    def displayPos(self, nodeObject, onScrennTextObject, task):
        x,y,z = nodeObject.getPos()
        h,p,r = nodeObject.getHpr()
        onScrennTextObject.setText('{:6.2f}, {:6.2f}, {:6.2f}\n {:6.2f}, {:6.2f}, {:6.2f}'.format(x,y,z,r,p,h))
        return task.cont

    def logPos(self, nodeObject, file, task):
        x,y,z = nodeObject.getPos()
        h,p,r = nodeObject.getHpr()
        file.write('{}, {}, {}, {}, {}, {}, {}\n'.format(datetime.datetime.now(),x,y,z,r,p,h))
        return task.cont
        
class Player(object):
    """
        Player is the main actor in the fps game
    """
    speed = 50
    FORWARD = Vec3(0,2,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-1,0,0)
    RIGHT = Vec3(1,0,0)
    LEFT_TURN = Vec3(60,0,0)
    RIGHT_TURN = Vec3(-60,0,0)
    NEUTRAL = Vec3(0,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    heading = NEUTRAL
    readyToJump = False
    jump = 0
    
    def __init__(self):
        """ inits the player """
        self.loadModel()
        self.setUpCamera()
        self.createCollisions()
        self.attachControls()
        # init mouse update task
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        taskMgr.add(self.jumpUpdate, 'jump-task')
        
    def loadModel(self):
        """ make the nodepath for player """
        self.node = NodePath('player')
        self.node.reparentTo(render)
        self.node.setPos(1,1,1)
        self.node.setScale(.05)

    def setUpCamera(self):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.node)
        base.camera.setHpr(Vec3(0,0,0))
        
    def createCollisions(self):
        """ create a collision solid and ray for the player """
        cn = CollisionNode('player')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.node, base.drive.node())
        # init players floor collisions
        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('playerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
        
    def attachControls(self):
        """ attach key events """
        base.accept( "space" , self.__setattr__,["readyToJump",True])
        base.accept( "space-up" , self.__setattr__,["readyToJump",False])
        base.accept( "w" , self.__setattr__,["walk",self.FORWARD])
        base.accept( "s" , self.__setattr__,["walk",self.BACK] )
        base.accept( "s-up" , self.__setattr__,["walk",self.STOP] )
        base.accept( "w-up" , self.__setattr__,["walk",self.STOP] )
        base.accept( "a" , self.__setattr__,["strafe",self.LEFT])
        base.accept( "d" , self.__setattr__,["strafe",self.RIGHT] )
        base.accept( "a-up" , self.__setattr__,["strafe",self.STOP] )
        base.accept( "d-up" , self.__setattr__,["strafe",self.STOP] )
        base.accept( "arrow_left" , self.__setattr__,["heading",self.LEFT_TURN])
        base.accept( "arrow_right" , self.__setattr__,["heading",self.RIGHT_TURN])
        base.accept( "arrow_left-up" , self.__setattr__,["heading",self.NEUTRAL])
        base.accept( "arrow_right-up" , self.__setattr__,["heading",self.NEUTRAL])
        
        
    def mouseUpdate(self,task):
        """ this task updates the mouse """
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, round(base.win.getXSize()/2), round(base.win.getYSize()/2)):
            self.node.setH(self.node.getH() -  (x - base.win.getXSize()/2)*0.1)
            #base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
        return task.cont

    def headingUpdate(self,task):
        return task.cont
    
    def moveUpdate(self,task): 
        """ this task makes the player move """
        # move where the keys set it
        self.node.setPos(self.node,self.walk*globalClock.getDt()*self.speed)
        self.node.setPos(self.node,self.strafe*globalClock.getDt()*self.speed)
        self.node.setHpr(self.node,self.heading*globalClock.getDt())
        return task.cont
        
    def jumpUpdate(self,task):
        # this task simulates gravity and makes the player jump
        # get the highest Z from the down casting ray
        highestZ = -100
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Cube":
                highestZ = z
        # gravity effects and jumps
        self.node.setZ(self.node.getZ()+self.jump*globalClock.getDt())
        self.jump -= 1*globalClock.getDt()
        if highestZ > self.node.getZ()-.3:
            self.jump = 0
            self.node.setZ(highestZ+.3)
            if self.readyToJump:
                self.jump = 1
        return task.cont

    
class keyObject(object):
    def __init__(self, modelDir, texDir, soundDir, posX = 0, posY = 0, posZ = 0):
        self.model = loader.loadModel(modelDir)
        #self.model.setScale(0.25, 0.25, 0.25)
        self.model.reparentTo(render)
        self.tex = loader.loadTexture(texDir)
        self.model.setTexture(self.tex,1)
        self.model.setPos(posX, posY, posZ)
        self.sound = base.audio.loadSfx(soundDir)
        base.audio.attachSoundToObject(self.sound, self.model)
        self.sound.setVolume(1)
        self.sound.setLoopCount(0)

class wayPoint(keyObject):
    path = []
    def __init__(self, modelDir, texDir, soundDir, posX = 0, posY = 0, posZ = 0):
        keyObject.__init__(self, modelDir, texDir, soundDir, posX, posY, posZ)
        self.sound.play()
        self.initCollision(posX, posY, posZ)
        self.loadPath()

    def loadPath(self):
        pathFile = open("./path.csv", "r")
        for line in pathFile:
            x, y, z = line.split(',')
            self.path.append( (float(x), float(y), float(z)) )
        pathFile.close()
        self.moveNext()

    def initCollision(self, posX, posY, posZ):
        cn = self.model.attachNewNode(CollisionNode('colNode'))
        cn.node().addSolid(CollisionSphere(0, 0, 0, 1))
        base.accept('into-' + cn.name, self.collition )
    
    def moveNext(self):
        self.model.setPos(self.path[0])
        self.path.remove(self.path[0])

    def collition(self, fromObj):
        # If collide with player
        if len(self.path) > 0:
            self.moveNext()
            feedBack = base.audio.loadSfx("./models/accending.mp3")
            feedBack.setVolume(0.5)
            feedBack.play()
        else:
            self.sound.stop()
    

game = FPS()
game.run()  
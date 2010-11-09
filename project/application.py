from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec3, Vec4, Point3, VBase4
from panda3d.core import CollisionTraverser
from panda3d.core import Light, Spotlight, PointLight, AmbientLight, PerspectiveLens

from menu import MainMenu
from lightcycle import LightCycle

MAX_STEPS = 0
ENABLE_STEPWISE = False

CAMERA_SPEED = 3

class PolyhedralTron(ShowBase):

    world = None

    def __init__(self):
        ShowBase.__init__(self)
        self.world = loader.loadModel('models/icosahedron')
        #TODO: Collisions can be sensitive to setScale, so change scale in Blender,
        #      and re-export. Using scale 10 for now.
        #self.world.setScale(10.0)
        self.world.setHpr(0,0,90)
        self.world.setColor(1, 1, 1)
        self.worldTex = loader.loadTexture('models/greenTriTex.png')
        self.world.setTexture(self.worldTex)
        self.world.reparentTo(render)
        self.collTrav = CollisionTraverser('GroundTrav')
        self.playerCycle = LightCycle(render, Vec3(1,1,-1), self.collTrav)
        self.setupLights()
        self.setupCamera()
        self.taskMgr.add(self.groundColTask, "GroundCollisionHandlingTask")
        self.registerKeys()
        self.steps = 0

        self.menu = MainMenu(self)

    def startGame(self):
        self.menu.hide()
        print "Uh... start the game, 'kay?"

    def quit(self):
        exit()

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(1, -4, 2)
        self.camera.lookAt(self.playerCycle.cycle)
        self.taskMgr.add(self.cameraMoveTask, 'cameraMoveTask')

    def setupLights(self):
        #Setup lights
        self.light = PointLight('pointLight')
        self.light.setColor(Vec4(1, 1, 1, 1))
        self.light.setLens(PerspectiveLens())
        self.lPath = render.attachNewNode(self.light)
        self.lPath.setPos(Point3(0, 0, 0))
        render.setLight(self.lPath)
        
        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        self.alnp = render.attachNewNode(self.alight)
        render.setLight(self.alnp)
        
        self.light2 = Spotlight('slight')
        self.light2.setColor(Vec4(1, 1, 1, 1))
        self.light2.setLens(PerspectiveLens())
        self.l2p = render.attachNewNode(self.light2)
        self.l2p.setPos(Point3(-1, 1, -1))
        self.l2p.lookAt(Point3(2, 2, -2))
        render.setLight(self.l2p)

    def registerKeys(self):
        self.accept('arrow_left', self.playerCycle.rotateStep, [-1])
        self.accept('arrow_right', self.playerCycle.rotateStep, [1])
        self.accept('escape', exit)
        self.accept('q', exit)
        
    ###    TASKS    ###
    def doStep(self, task):
        #self.taskMgr.add(self.groundColTask, 'GroundCollisionHandlingTask')
        #if ENABLE_STEPWISE:
        #    self.accept('space', self.doStep)
        self.groundColTask(task)
        self.cameraMoveTask(task)
        if ENABLE_STEPWISE:
            if MAX_STEPS != 0:
                self.steps += 1
            if MAX_STEPS == 0 or self.steps < MAX_STEPS:
                return Task.cont
    
    def groundColTask(self, task):
        #print "Testing collisions..."
        self.playerCycle.moveForwardBy(0.25)
        self.collTrav.traverse(render)
        self.playerCycle.adjustToTerrain()
        if self.steps < MAX_STEPS or MAX_STEPS == 0:
            self.steps += 1
            if not ENABLE_STEPWISE:
                return Task.cont

    def cameraMoveTask(self, task):
        cycPos = self.playerCycle.cycle.getPos()
        cycQuat = self.playerCycle.cycle.getQuat()
        camPos = self.camera.getPos()
        z = cycQuat.getUp()
        y = cycQuat.getForward()
        offset = z*3-y*8
        newCamPos = cycPos + offset
        if (newCamPos - camPos).length() > CAMERA_SPEED:
            direction = newCamPos - camPos
            direction.normalize()
            direction = direction * CAMERA_SPEED
            self.camera.setPos(camera.getPos() + direction)
        else:
            self.camera.setPos(newCamPos)
        self.camera.lookAt(cycPos + z*2, z)
        return Task.cont

        

if __name__ == '__main__':
    app = PolyhedralTron()
    app.run()

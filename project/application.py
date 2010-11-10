from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec3, Vec4, Point3, VBase4
from panda3d.core import CollisionTraverser
from panda3d.core import Light, Spotlight, PointLight, AmbientLight, PerspectiveLens

from menu import MainMenu
from lightcycle import LightCycle
from cameracontroller import CameraController

MAX_STEPS = 0
ENABLE_STEPWISE = False

CAMERA_SPEED = 3

class PolyhedralTron(ShowBase):

    world = None

    def __init__(self):
        ShowBase.__init__(self)
        base.win.setClearColor(VBase4(0, 0, 0, 0))
        self.world = loader.loadModel('models/icosahedron')
        self.menu = MainMenu(self)
        self.world.setHpr(0,0,90)
        self.world.setColor(1, 1, 1)
        self.worldTex = loader.loadTexture('models/greenTriTex.png')
        self.world.setTexture(self.worldTex)

    def startGame(self):
        self.menu.hide()
        #TODO: Collisions can be sensitive to setScale, so change scale in Blender,
        #      and re-export. Using scale 10 for now.
        #self.world.setScale(10.0)
        self.world.reparentTo(render)
        self.collTrav = CollisionTraverser('GroundTrav')
        self.playerCycle = LightCycle(render, Vec3(1,1,-1), self.collTrav)
        self.setupCamera()
        self.setupLights()
        self.registerKeys()
        self.taskMgr.add(self.groundColTask, "GroundCollisionHandlingTask")
        self.steps = 0

    def quit(self):
        exit()

    def setupCamera(self):
        self.cameraTracker = CameraController(self, self.camera, self.playerCycle.cycle, self.collTrav)
        self.camera.setPos(1, -4, 2)
        self.camera.lookAt(self.playerCycle.cycle)
        #self.taskMgr.add(self.cameraMoveTask, 'cameraMoveTask')

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
        self.accept('arrow_left', self.keyLeft)
        self.accept('arrow_right', self.keyRight)
        self.accept('escape', exit)
        self.accept('q', exit)

    def keyLeft(self):
        if self.playerCycle is not None:
            self.playerCycle.rotateStep(-1)

    def keyRight(self):
        if self.playerCycle is not None:
            self.playerCycle.rotateStep(1)
        
    ###    TASKS    ###
    def groundColTask(self, task):
        #print "Testing collisions..."
        self.playerCycle.moveForwardBy(0.25)
        self.cameraTracker.move(task)
        self.collTrav.traverse(render)
        self.playerCycle.adjustToTerrain()
        #self.cameraTracker.adjustToTerrain()
        if self.steps < MAX_STEPS or MAX_STEPS == 0:
            self.steps += 1
            if not ENABLE_STEPWISE:
                return Task.cont

        

if __name__ == '__main__':
    app = PolyhedralTron()
    app.run()

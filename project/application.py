from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Vec4, Point3, VBase4
from panda3d.core import CollisionTraverser
from panda3d.core import Light, Spotlight, PointLight, AmbientLight, PerspectiveLens
from lightcycle import LightCycle

class PolyhedralTron(ShowBase):

    world = None

    def __init__(self):
        ShowBase.__init__(self)
        self.world = loader.loadModel('models/icosahedron')
        #TODO: Change this to 20.0 or 50.0; 10.0 for the sake of debugging.
        self.world.setScale(10.0)
        self.world.reparentTo(render)
        self.collTrav = CollisionTraverser('GroundTrav')
        self.playerCycle = LightCycle(render, Vec3(0,0,0), self.collTrav)
        self.setupLights()
        self.taskMgr.add(self.groundColTask, "GroundCollisionHandlingTask")
        
    def groundColTask(self, task):
        print "Testing collisions..."
        self.collTrav.traverse(render)
        self.playerCycle.adjustToTerrain()

    def setupLights(self):
        #Setup lights
        self.light = PointLight('pointLight')
        self.light.setColor(Vec4(1, 1, 1, 1))
        self.light.setLens(PerspectiveLens())
        self.lPath = render.attachNewNode(self.light)
        self.lPath.setPos(Point3(15, 0, 0))
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
        

if __name__ == '__main__':
    app = PolyhedralTron()
    app.run()

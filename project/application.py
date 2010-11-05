from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from lightcycle import LightCycle

class PolyhedralTron(ShowBase):

    world = None

    def __init__(self):
        ShowBase.__init__(self)
        self.world = loader.loadModel('models/icosahedron')
        self.world.reparentTo(render)
        self.collTrav = CollisionTraverser('GroundTrav')
        self.playerCycle = LightCycle(render, Vec3(0,0,0), self.collTrav)
        

if __name__ == '__main__':
    app = PolyhedralTron()
    app.run()

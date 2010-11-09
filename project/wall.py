from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3, Vec4, Quat, BitMask32, Point3
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode, CollisionHandlerFloor
import math

class Wall(DirectObject):
    """This is a wall that protrudes from the lightcycles."""
    
    wall = None
    distMoved = 0

    def __init__(self, parentNode, startingPoint, quat):
        self.wall = loader.loadModel('models/wall')
        self.wall.reparentTo(parentNode)
        self.wall.setPos(startingPoint)
        self.wall.setQuat(quat)

    def moveForwardBy(self, position, dist):
        self.distMoved += dist
        self.wall.setPos(position)

    def getDistMoved(self):
        return self.distMoved

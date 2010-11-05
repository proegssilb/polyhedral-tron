from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3, Vec4, Quat, BitMask32
from panda3d.core import CollisionRay, CollisionHandlerFloor, CollisionNode


class LightCycle(DirectObject):
    """A class to represent a lightcycle in Tron
    Provides lightcycle-specific convenience functions, helps group per-cycle
    variables.
    """

    cycle = None

    def __init__(self, parentNode, startingPoint, collisionTraverser):
        self.cycle = loader.loadModel('models/lightcycle')
        self.cycle.reparentTo(parentNode)
        self.cycle.setPos(startingPoint)

        #Collision related stuff...
        self.groundRay = CollisionRay()
        self.groundRay.setOrigin(0,0, -100)
        self.groundRay.setDirection(0,0,1)
        
        self.colNode = CollisionNode('cycleRay-%s' % id(self))
        self.colNode.addSolid(self.groundRay)
        self.colNode.setFromCollideMask(BitMask32.bit(0))
        self.colNode.setIntoCollideMask(BitMask32.allOff())
        
        self.colNodePath = self.cycle.attachNewNode(self.colNode)
        self.colHandler = CollisionHandlerQueue()
        collisionTraverser.addCollider(self.colNodePath, self.colHandler)
        
    def setUp(upVect):
        rightVect = self.cycle.getQuat().getRight()
        forVect = upVect.cross(rightVect)
        self.cycle.lookAt(self.cycle.getPos() + forVect, upVect)

    def moveForwardBy(dist):
        forVect = self.cycle.getQuat().getForward()
        positionIncrement = forVect * dist
        newPos = self.cycle.getPos() + positionIncrement
        self.cycle.setPos(newPos)

    def rotateStep(numSteps):
        angle = 90*numSteps
        q = Quat()
        q.setFromAxisAngle(angle, self.cycle.getQuat().getUp())
        self.cycle.setQuat(self.cycle.getQuat()*q)

    #TODO: Add functions for ground-collision handling...
    def adjustToTerrain():
        """During collision handling, adjust height/orientation to match
           terrain. Assumes that the collision traverser has had .traverse()
           called."""
        entries = self.colHandler.getEntries()
        #entries.sort
        #z =
        #newNorm =
        self.cycle.setZ(z)
        r = self.cycle.getQuat().getRight()
        f = newNorm.cross(r)
        self.cycle.lookAt(self.cycle.getPos() + v, newNorm)

    
        
        

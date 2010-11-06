from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3, Vec4, Quat, BitMask32
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode, CollisionHandlerFloor
import math

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
        #pdir(self.groundRay)
        self.groundRay.setOrigin(0,0, 2)
        self.groundRay.setDirection(0,0,-1)
        
        self.colNode = CollisionNode('cycleRay-%s' % id(self))
        self.colNode.addSolid(self.groundRay)
        self.colNode.setFromCollideMask(BitMask32.bit(0))
        self.colNode.setIntoCollideMask(BitMask32.allOff())
        
        self.colNodePath = self.cycle.attachNewNode(self.colNode)
        self.colHandler = CollisionHandlerQueue()
        collisionTraverser.addCollider(self.colNodePath, self.colHandler)
        
    def setUp(self, upVect):
        rightVect = self.cycle.getQuat().getRight()
        forVect = upVect.cross(rightVect)
        self.cycle.lookAt(self.cycle.getPos() + forVect, upVect)

    def moveForwardBy(self, dist):
        forVect = self.cycle.getQuat().getForward()
        positionIncrement = forVect * dist
        newPos = self.cycle.getPos() + positionIncrement
        self.cycle.setPos(newPos)

    def rotateStep(self, numSteps):
        angle = 90*numSteps
        q = Quat()
        q.setFromAxisAngle(angle, self.cycle.getQuat().getUp())
        self.cycle.setQuat(self.cycle.getQuat()*q)

    #TODO: Add functions for ground-collision handling...
    def adjustToTerrain(self):
        """During collision handling, adjust height/orientation to match
           terrain. Assumes that the collision traverser has had .traverse()
           called."""
        entries = self.colHandler.getEntries()
        x, y, z, norm, count = 0, 0, 0, Vec3(), 0
        print 'Entries:', len(entries)
        for ent in entries[:]:
            p1 = ent.getSurfacePoint(self.cycle)
            p2 = self.cycle.getPos()
            #pdir(p1)
            dot = p1.dot(p2)
            mag1 = p1.length()
            mag2 = p2.length()
            print "Collision:", dot, mag1, mag2, p1
            if not (dot > 0 and mag1 >= mag2 - 0.005):
                entries.remove(ent)
            else:
                print 'Before:', self.cycle.getPos()
                self.cycle.setPos(p1)
                print 'After translate:', self.cycle.getPos()
                newNorm = ent.getSurfaceNormal(self.cycle)
                self.setUp(newNorm)
                print 'After orient:', self.cycle.getPos()
        #newNorm =


    
        
        

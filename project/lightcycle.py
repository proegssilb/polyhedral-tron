from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3, Vec4, Quat, BitMask32, Point3
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
        self.groundRay.setOrigin(0,0, 60)
        self.groundRay.setDirection(0,0,-1)
        
        self.colNode = CollisionNode('cycleRay-%s' % id(self))
        self.colNode.addSolid(self.groundRay)
        self.colNode.setFromCollideMask(BitMask32.bit(0))
        self.colNode.setIntoCollideMask(BitMask32.allOff())
        
        self.colNodePath = self.cycle.attachNewNode(self.colNode)
        self.colNodePath.show()
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
        newP, norm, count = Point3(),  Vec3(), 0
        print 'Entries:', len(entries)
        for ent in entries[:]:
            p1 = ent.getSurfacePoint(render)
            p2 = self.cycle.getPos()
            #pdir(p1)
            dot = p1.dot(p2)
            mag1 = p1.length()
            mag2 = p2.length()
            print "Collision:"
            print '    surfPos:', p1
            print '    cycPos:', p2
            print '    Dot product:', dot
            print '    abs(surfPos):', mag1
            print '    abs(cycPos):', mag2
            if not (dot > 0 and mag1 >= mag2 - 0.5):
            #if False:
                entries.remove(ent)
            else:
                newP += p1
                norm += ent.getSurfaceNormal(render)
                count += 1
        if count == 0:
            return
        norm.normalize()
        print 'Results from %s items:' % count
        print '    New Position:', newP, newP / count
        print '    New normal:', norm
        newP = newP / count
        norm.normalize()
        self.cycle.setPos(newP)
        self.setUp(norm)
        #newNorm =


    
        
        

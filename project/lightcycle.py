from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.task import Task
from panda3d.core import Vec3, Vec4, Quat, BitMask32, Point3, VBase3
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode, CollisionHandlerFloor
from panda3d.core import CollisionHandlerEvent, CollisionTube, CollisionSegment, CollisionSphere
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
import math, sys
from panda3d.core import Filename

from wall import Wall

class LightCycle(DirectObject):
    """A class to represent a lightcycle in Tron
    Provides lightcycle-specific convenience functions, helps group per-cycle
    variables.
    """

    cycle = None
    wallList = []
    currentWall = None
    wallOffset = -0.75
    enable = True
    

    def __init__(self, app, parentNode, startingPoint, collisionTraverser):
        self.app = app
        self.cycle = loader.loadModel('models/lightcycle')
        self.cycle.reparentTo(parentNode)
        self.cycle.setFluidPos(startingPoint)
        self.wallNode = parentNode.attachNewNode('walls')
        self.enable = True

        #Collision related stuff...
        self.groundRay = CollisionRay()
        self.groundRay.setOrigin(0,0, 1)
        self.groundRay.setDirection(0,0,-1)
        self.colNode = CollisionNode('cycleRay-%s' % id(self))
        self.colNode.addSolid(self.groundRay)
        self.colNode.setFromCollideMask(BitMask32.bit(0))
        self.colNode.setIntoCollideMask(BitMask32.allOff())        
        self.colNodePath = self.cycle.attachNewNode(self.colNode)
        self.colHandler = CollisionHandlerQueue()
        collisionTraverser.addCollider(self.colNodePath, self.colHandler)
        
        #Wall colliding stuff...
        self.colEventHandler = CollisionHandlerEvent()
        self.colEventHandler.addInPattern('%fn-into%(wall)ih')
        #These numbers are loosely based on the cycle model.
        self.colCapsule = CollisionSegment(0, 1.0, 0.5, 0, -0.2, 0.5)
        #self.colCapsule2 = CollisionSphere(0, 0, 0.5, .5)
        #self.colCapsule3 = CollisionSphere(0, -.7, 0.5, .5)
        name = 'cycle-%s' % id(self)
        self.colCycNode = CollisionNode(name)
        self.colCycNode.addSolid(self.colCapsule)
        #self.colCycNode.addSolid(self.colCapsule2)
        #self.colCycNode.addSolid(self.colCapsule3)
        self.colCycNode.setCollideMask(BitMask32.bit(1))
        self.colCycNP = self.cycle.attachNewNode(self.colCycNode)
        self.accept('%s-into' % name, self.explode)
        collisionTraverser.addCollider(self.colCycNP, self.colEventHandler)
        

        self.currentWall = Wall(self.wallNode, self.cycle.getPos() + self.cycle.getQuat().getForward() * self.wallOffset, self.cycle.getQuat())
        self.currentWall.wall.setCollideMask(BitMask32(0x00))

        base.enableParticles()
        self.p = ParticleEffect()
        
    def setUp(self, upVect):
        rightVect = self.cycle.getQuat().getRight()
        forVect = upVect.cross(rightVect)
        self.cycle.lookAt(self.cycle.getPos() + forVect, upVect)

    def moveForwardBy(self, dist):
        if not self.enable:
            return
        forVect = self.cycle.getQuat().getForward()
        positionIncrement = forVect * dist
        newPos = self.cycle.getPos() + positionIncrement
        self.cycle.setFluidPos(newPos)
        if (self.currentWall.getDistMoved() >= .75):
            self.newWall()
        else:
            self.currentWall.moveForwardBy(self.cycle.getPos() + self.cycle.getQuat().getForward() * self.wallOffset,dist)

    def rotateStep(self, numSteps):
        """Rotate a given number of steps.
        Rotates in 90-degree steps around this cycle's current up axis.
        Left is negative, right is positive.
        """
        if not self.enable:
            return
        print 'Rotating...', numSteps
        angle = -90*numSteps
        q = Quat()
        q.setFromAxisAngle(angle, self.cycle.getQuat().getUp())
        qi = self.cycle.quatInterval(.075, self.cycle.getQuat()*q)
        qi.start()
        self.newWall()

    def adjustToTerrain(self):
        """During collision handling, adjust height/orientation to match
           terrain. Assumes that the collision traverser has had .traverse()
           called."""
        if not self.enable: return
        entries = self.colHandler.getEntries()
        newP, norm, count = Point3(),  Vec3(), 0
        #print 'Entries:', len(entries)
        for ent in entries[:]:
            if ent.getIntoNodePath().hasNetTag('wall'):
                #The tag 'wall' is only given to walls.
                self.explode()
                return
            p1 = ent.getSurfacePoint(render)
            p2 = self.cycle.getPos()
            dot = p1.dot(p2)
            mag1 = p1.length()
            mag2 = p2.length()
            #print "Collision:"
            #print '    surfPos:', p1
            #print '    cycPos:', p2
            #print '    Dot product:', dot
            #print '    abs(surfPos):', mag1
            #print '    abs(cycPos):', mag2
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
        #print 'Results from %s items:' % count
        #print '    New Position:', newP, newP / count
        #print '    New normal:', norm
        newP = newP / count
        norm.normalize()
        up = self.cycle.getQuat().getUp()
        self.cycle.setFluidPos(newP)
        self.setUp(norm)
        if (up.angleDeg(norm) > 5):
            self.newWall()

    def newWall(self):
        if not self.enable:
            return
        self.wallList.append(self.currentWall)
        self.currentWall.wall.setCollideMask(BitMask32.bit(1))
        self.currentWall.wall.setTag('wall','1')
        self.currentWall = Wall(self.wallNode, self.cycle.getPos() + self.cycle.getQuat().getForward() * self.wallOffset, self.cycle.getQuat())
        #self.currentWall.wall.setCollideMask(BitMask32(0x00))
        self.currentWall.wall.setCollideMask(BitMask32.bit(1))
    
    def explode(self, *pargs):
        if not self.enable:
            return
        self.loadParticleConfig('splody3.ptf')
        self.cycle.detachNode()
        self.enable = False
        self.app.accept('escape', self.die)
        self.task = self.app.taskMgr.doMethodLater(7, self.die, 'resetTask')
        #li = self.cycle.hprInterval(0.5, VBase3(359, 0, 0), name='spin')
        #f = Func(self.die)
        #Sequence(li, li, li, li, name='SpinAndDie').loop()
        
        
    def die(self, *pargs):
        self.cycle.removeNode()
        self.wallNode.detachNode()
        self.wallNode.removeNode()
        #if self.p is not None:
        #    self.p.cleanup()
        #    self.p = None
        self.app.reset()
        self.app.taskMgr.remove(self.task)
        return Task.done

    def loadParticleConfig(self, file):
        #if self.p is not None:
        #    self.p.cleanup()
        #    self.p = None
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(file))
        dummy = render.attachNewNode('dummy')
        dummy.setPos(self.cycle.getPos())
        dummy.setQuat(self.cycle.getQuat())
        self.p.start(dummy)
        self.p.setFluidPos(0,0,0)
        self.app.taskMgr.doMethodLater(.2, lambda *pargs: self.p.cleanup(), 'endParticle')

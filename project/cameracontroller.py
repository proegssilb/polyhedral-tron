from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.interval.IntervalGlobal import *
from panda3d.core import Vec3, Vec4, Point3, Quat, BitMask32
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode

TIME_STEP = .02

class CameraController(DirectObject):
    """ A class to control the camera in a 3D-aware way.
    
    The standard camera procedures result in jerkiness and
    sometimes odd twitches or flips. This class controls
    the camera by following the floor, and using intervals
    to ensure smoothness. Or, that's the theory.
    """
    targetOffset = Vec3(0, -15, 5)
    maxDist = .55
    maxQuatAngle = 5
    
    def __init__(self, base, camera, npToTrack, collisionTraverser):
        base.disableMouse()
        self.camera = camera
        self.target = npToTrack
        
        #Collision stuff...
        self.ray = CollisionRay()
        self.ray.setOrigin(0, 0, 100)
        self.ray.setDirection(0,0,-1)
        self.colNode = CollisionNode('cameraRay')
        self.colNode.addSolid(self.ray)
        self.colNode.setFromCollideMask(BitMask32.bit(1))
        self.colNode.setIntoCollideMask(BitMask32(0))
        self.colNodePath = self.camera.attachNewNode(self.colNode)
        self.colHandler = CollisionHandlerQueue()
        collisionTraverser.addCollider(self.colNodePath, self.colHandler)
        
    def setUp(self, upVect):
        rightVect = self.camera.getQuat().getRight()
        self.camera.lookAt(self.target.getPos(), upVect)
    
    def move(self, task):
        #Do the calculations for position
        targPos = self.target.getPos()
        #offset = self.target.getQuat().xform(self.targetOffset)
        x = self.target.getQuat().getRight()
        y = self.target.getQuat().getForward()
        z = self.target.getQuat().getUp()
        dx = self.targetOffset.getX()
        dy = self.targetOffset.getY()
        dz = self.targetOffset.getZ()
        offset = x*dx + y*dy + z*dz
        targPos = targPos + offset
        toMove = targPos - self.camera.getPos()
        d = toMove.length()
        if (d > 15):
            toMove.normalize()
            toMove = toMove*15
        #Do calculations for quat
        #v = Vec3(targPos - self.camera.getPos())
        #f = self.camera.getQuat().getForward()
        #ang = f.angleDeg(v)
        #axis = f.cross(v)
        #axis.normalize()
        #q = Quat()
        #q.setFromAxisAngle(ang, axis)
        #q.normalize()
        #Update
        self.camera.setPos(targPos)
        laPos = self.target.getPos() + self.target.getQuat().getUp()*3
        self.camera.lookAt(laPos, self.target.getQuat().getUp())
        #
        return Task.again

    def adjustToTerrain(self):
        entries = self.colHandler.getEntries()
        newP, norm, count = Point3(),  Vec3(), 0
        for ent in entries[:]:
            p1 = ent.getSurfacePoint(render)
            p2 = self.camera.getPos()
            dot = p1.dot(p2)
            mag1 = p1.length()
            mag2 = p2.length()
            if not (dot > 0 and mag1 >= mag2 - 0.5):
                entries.remove(ent)
            else:
                newP += p1
                norm += ent.getSurfaceNormal(render)
                count += 1
        if count == 0:
            return
        norm.normalize()
        newP = newP / count
        norm.normalize()
        newP = newP + norm*3
        self.camera.setPos(newP)
        self.setUp(norm)
        

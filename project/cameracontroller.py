from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from panda3d.core import Vec3, Vec4, Point3, Quat
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode

TIME_STEP = .02

class CameraController(DirectObject):
    """ A class to control the camera in a 3D-aware way.
    
    The standard camera procedures result in jerkiness and
    sometimes odd twitches or flips. This class controls
    the camera by following the floor, and using intervals
    to ensure smoothness. Or, that's the theory.
    """
    
    def __init__(self, camera, npToTrack, collisionTraverser):
        self.camera = camera
        self.target = npToTrack
        
        #Collision stuff...

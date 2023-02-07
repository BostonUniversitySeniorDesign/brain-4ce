from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from panda3d.core import NodePath
from panda3d.core import PandaNode
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText
import math
import generate

class MyApp(ShowBase):

        
    xCoord = 0
    yCoord = 0
    angle  = 0
    textObject = None

    def __init__(self):
        ShowBase.__init__(self)
        # ShowBase.useDrive(self)
        # ShowBase.useTrackball(self)
        ShowBase.oobe(self)

        self.accept('d', self.ChangeCameraPositionRight)
        self.accept('a', self.ChangeCameraPositionLeft)
        self.accept('s', self.ChangeCameraPositionBackward)
        self.accept('w', self.ChangeCameraPositionForward)
        self.taskMgr.add(self.UpdateCameraPosition)

        blank_node = PandaNode("my_blank_node")
        self.nodepath1 = NodePath(blank_node)
        self.nodepath1.reparentTo(self.render)

        blank_node2 = PandaNode("my_blank_node2")
        self.nodepath2 = NodePath(blank_node2)
        self.nodepath2.reparentTo(self.render)

        blank_node3 = PandaNode("my_blank_node3")
        self.nodepath3 = NodePath(blank_node3)
        self.nodepath3.reparentTo(self.render)

        self.scene = generate.GenerateModel(self, (0,0,-0.5), (50,50,10), (0,0,0), self.nodepath3, "my-objects/plane.egg")
        self.sphObject = generate.GenerateModel(self, (0, 10, 0.1), (0.6, 0.6, 0.6), (0,0,0), self.nodepath2, "my-objects/sphere.egg")
        self.barrier1 = generate.GenerateModel(self,(0, 300, 1.63), (6.3, 31.3, 1), (90,0,0), self.nodepath1, "my-objects/barrier.egg")
        self.barrier2 = generate.GenerateModel(self, (300, 0, 1.63), (6.3, 31.3, 1), (180,0,0), self.nodepath1, "my-objects/barrier.egg")
        self.barrier3 = generate.GenerateModel(self, (-300, 0, 1.63), (6.3, 31.3, 1), (180,0,0), self.nodepath1, "my-objects/barrier.egg")
        self.barrier4 = generate.GenerateModel(self, (0, -300, 1.63), (6.3, 31.3, 1), (90,0,0), self.nodepath1, "my-objects/barrier.egg")


        self.textObject = OnscreenText(text='x:0 y:0', pos=(-0.5, 0.02), scale=0.07)

        generate.SetLight(self, "my dlight", 'd', 0, self.nodepath2)
        generate.SetLight(self, "my alight", 'a', (0.2,0.2,0.8,1), self.scene)
        generate.SetLight(self, "green light", 'a', ((0.2, 0.9, 0.2, 1)), self.nodepath1)


    def ChangeCameraPositionForward(self):
        self.yCoord += 5

    def ChangeCameraPositionBackward(self):
        self.yCoord -= 5     

    def ChangeCameraPositionRight(self):
        self.xCoord += 1



    def ChangeCameraPositionLeft(self):
        self.xCoord -= 1



    def UpdateCameraPosition(self, task):
        self.textObject.destroy()
        self.textObject = OnscreenText(text='x: ' + str(self.xCoord) + ' y:' + str(self.yCoord), pos=(-0.5, 0.02), scale=0.07)
        self.camera.setPos(self.xCoord, self.yCoord, 0)
#        self.camera.setHpr(self.angle, 0, 0)
        self.sphObject.setPos(self.xCoord, 10 + self.yCoord, 0.1)
        return task.cont




game = MyApp()
game.run()

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from panda3d.core import NodePath
from panda3d.core import PandaNode
from pandac.PandaModules import WindowProperties
from direct.showbase import DirectObject


class MyApp(ShowBase, DirectObject.DirectObject):

    xCoord = 0
    yCoord = 0

    def ChangeCameraPosition(self):
        self.xCoord = self.xCoord + 5
        self.yCoord = self.yCoord + 5
        self.camera.setPos(self.xCoord,self.yCoord,-0.5)
        print(self.xCoord)
        print(self.yCoord)

    # def __Mouseinit__(self):
    #    self.disableMouse()

    def __init__(self):
        ShowBase.__init__(self)
#        self.accept('mouse1', self.__Mouseinit__)
        self.accept('a', self.ChangeCameraPosition)

        blank_node = PandaNode("my_blank_node")
        nodepath1 = NodePath(blank_node)
        nodepath1.reparentTo(self.render)

        blank_node2 = PandaNode("my_blank_node2")
        nodepath2 = NodePath(blank_node2)
        nodepath2.reparentTo(self.render)        

        dlight = DirectionalLight('my dlight')

        self.scene = self.loader.loadModel("my-objects/plane.egg")
        self.scene.setPos(0,0,-0.5)
        self.scene.setScale(10, 10, 10)
        self.scene.reparentTo(nodepath2)

        sphObject = self.loader.loadModel("my-objects/sphere.egg")
        sphObject.setPos(0, 10, 0.1)
        sphObject.setScale(.6, .6, .6)
        sphObject.reparentTo(nodepath1)

        dlnp = nodepath1.attachNewNode(dlight)
        nodepath1.setLight(dlnp)





game = MyApp()

game.run()

print(game.x)
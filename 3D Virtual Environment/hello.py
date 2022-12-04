from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from panda3d.core import NodePath
from panda3d.core import PandaNode


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        blank_node = PandaNode("my_blank_node")
        blank_node_path = NodePath(blank_node)
        blank_node_path.reparentTo(self.render)

        dlight = DirectionalLight('my dlight')


        plane = self.loader.loadModel("my-objects/plane.egg")
        #plane.setPos(1,10,1)
        plane.setScale(10, 10, 10)
        plane.reparentTo(self.render)

        sphObject = self.loader.loadModel("my-objects/sphere.egg")
        sphObject.setPos(0, 10, 1)
        sphObject.setScale(1, 1, 1)
        sphObject.reparentTo(blank_node_path)

        dlnp = blank_node_path.attachNewNode(dlight)
        blank_node_path.setLight(dlnp)





game = MyApp()

game.run()
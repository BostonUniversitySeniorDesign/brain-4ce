from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from panda3d.core import NodePath
from panda3d.core import PandaNode, LightAttrib 
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText
import math

def GenerateModel(self, position, scale, hpr, parent, path):
    model = self.loader.loadModel(path)
    model.setPos(*position)
    model.setScale(*scale)
    model.setHpr(*hpr)
    model.reparentTo(parent)


    return model 

def SetLight(self, name, type, color, node):

    if (type == 'd'):
        self.light = DirectionalLight(name)
    elif (type == 'a'):
        self.light = AmbientLight(name)
    
    if (color):
        self.light.setColor(color)



    lp = node.attachNewNode(self.light)




    node.setLight(lp)
    
    return lp
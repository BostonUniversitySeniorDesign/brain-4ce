from panda3d.core import AmbientLight, DirectionalLight
import os

#config_dir = os.environ['models']

def GenerateModel(self, position, scale, hpr, parent, path):
    
    # full_path = os.path.join(config_dir, path)
    
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
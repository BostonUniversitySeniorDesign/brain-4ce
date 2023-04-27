from panda3d.core import AmbientLight, DirectionalLight

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
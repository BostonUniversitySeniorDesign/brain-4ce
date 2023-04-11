from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import AmbientLight, DirectionalLight, PointLight
from panda3d.core import NodePath
from panda3d.core import PandaNode, load_prc_file
from panda3d.core import Vec3, Spotlight, TextureStage
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText
import math
import socket
import generate
import random
import time
import simplepbr


load_prc_file('myConfig.prc')

class MyApp(ShowBase):

    xCoord = 0
    yCoord = 0
    angle  = 180
    textObject = None
    camera_pos = 0
    dir_list = ['left', 'right', 'backward', 'forward']
    prev_sec = 0

    def __init__(self):
        ShowBase.__init__(self)
        simplepbr.init()
        # ShowBase.useDrive(self)
        # ShowBase.useTrackball(self)
        ShowBase.oobe(self)


        
        self.accept('d', self.ChangeSpherePositionRight)
        self.accept('a', self.ChangeSpherePositionLeft)
        self.accept('s', self.ChangeSpherePositionBackward)
        self.accept('w', self.ChangeSpherePositionForward)
        self.taskMgr.add(self.UpdateSpherePosition)
        self.taskMgr.add(self.ChooseDirection)

        blank_node = PandaNode("my_blank_node")
        self.nodepath1 = NodePath(blank_node)
        self.nodepath1.reparentTo(self.render)

        blank_node2 = PandaNode("my_blank_node2")
        self.nodepath2 = NodePath(blank_node2)
        self.nodepath2.reparentTo(self.render)

        blank_node3 = PandaNode("my_blank_node3")
        self.nodepath3 = NodePath(blank_node3)
        self.nodepath3.reparentTo(self.render)



        self.scene = generate.GenerateModel(self, (0,0,-0.5), (50,50,10), (0,0,0), self.nodepath3, "models/plane.bam")
        #self.scene =  loader.loadModel("models/plane.bam")
        self.sphObject = generate.GenerateModel(self, (0, 10, 0.1), (0.6, 0.6, 0.6), (0,0,0), self.nodepath2, "models/sphere.egg")
        self.barrier1 = generate.GenerateModel(self,(0, 300, 1.63), (6.3, 31.3, 1), (90,0,0), self.nodepath1, "models/barrier.egg")
        self.barrier2 = generate.GenerateModel(self, (300, 0, 1.63), (6.3, 31.3, 1), (180,0,0), self.nodepath1, "models/barrier.egg")
        self.barrier3 = generate.GenerateModel(self, (-300, 0, 1.63), (6.3, 31.3, 1), (180,0,0), self.nodepath1, "models/barrier.egg")
        self.barrier4 = generate.GenerateModel(self, (0, -300, 1.63), (6.3, 31.3, 1), (90,0,0), self.nodepath1, "models/barrier.egg")




        self.textObject = OnscreenText(text='x:0 y:0', pos=(-0.5, 0.02), scale=0.07)

        #self.dlnp = generate.SetLight(self, "my dlight", 'd', 0, self.nodepath2)
      #  self.bluenp = generate.SetLight(self, "blue light", 'a', (0.2,0.2,0.8,1),  self.scene)
       # self.bluenp = generate.SetLight(self, "my dlight2", 'd', 0, self.scene)
       # self.greennp = generate.SetLight(self, "green light", 'a', ((0.2, 0.9, 0.2, 1)), self.nodepath1)


        # host = socket.gethostname()
        # port = 55002 #random unprivileged port

        # """ Starting a TCP socket. """
        # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # """ Bind the IP and PORT to the server. """
        # server_socket.bind((host, port))
        
        # """ Start Server Listening"""
        # server_socket.listen()

        # """ Server accepts connection from client"""
        # self.conn, self.address = server_socket.accept()



    def ChangeSpherePositionBackward(self):
        self.sphObject.setPos(self.sphObject.getPos() + Vec3(math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle)), 0) * 10)

    def ChangeSpherePositionForward(self):
        self.sphObject.setPos(self.sphObject.getPos() + Vec3(math.sin(math.radians(self.angle+180)), math.cos(math.radians(self.angle+180)), 0) * 10)

    def ChangeSpherePositionRight(self):
        self.angle += 10
    
    def ChangeSpherePositionLeft(self):
        self.angle -= 10
        

    def UpdateSpherePosition(self, task):
        self.sphObject.setH(self.angle)
        return task.cont

    def ChooseDirection(self, task):
        

        # data = self.conn.recv(1024).decode()
        # data = int(data)


        # dir = self.dir_list[data]
        # if dir == 'forward':
        #     self.sphObject.setPos(self.sphObject.getPos() + Vec3(math.sin(math.radians(self.angle+180)), math.cos(math.radians(self.angle+180)), 0) * 10)
        # elif dir == 'backward':
        #     self.sphObject.setPos(self.sphObject.getPos() + Vec3(math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle)), 0) * 10)
        # elif dir == 'right':
        #     self.angle += 10
        # elif dir == 'left':
        #     self.angle -= 10
        #self.prev_sec = curr_sec


        self.textObject.destroy()
        self.textObject = OnscreenText(text='x: ' + str(round(self.sphObject.getPos()[0],2)) + ' y:' + str(round(self.sphObject.getPos()[1],2)), pos=(-0.5, 0.02), scale=0.07)
        sph_hpr = self.sphObject.getHpr()
        sph_heading = sph_hpr[0]


        self.camera_pos = self.sphObject.getPos() + Vec3(math.sin(math.radians(sph_heading)), math.cos(math.radians(sph_heading)), 0) * 10
        self.xCoord = self.camera_pos[0] 
        self.yCoord = self.camera_pos[1] 

        self.camera.setPos(self.camera_pos)
        self.camera.lookAt(self.sphObject)

        
        #self.dlnp.setHpr(self.camera.getHpr())        

        return task.cont


game = MyApp()

game.run()


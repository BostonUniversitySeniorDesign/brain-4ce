from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import NodePath
from panda3d.core import PandaNode, load_prc_file, TextNode, Vec3
from direct.gui.DirectGui import *
import math
import generate
import simplepbr


load_prc_file('myConfig.prc')

class MyApp(ShowBase):

    xCoord = 0
    yCoord = 0
    angle  = 180
    textObject = None
    textNode = TextNode('myTextNode')
    scoreNode = TextNode('myScore')
    isMovingForward = False
    isMovingRight = False
    isMovingBackward = False
    isMovingLeft = False
    fakeHeading = 180
    obj_coords = []
    index = 0
    score = 0
    star_angle = 0
    last_message_time = 0

    camera_pos = 0
    dir_list = ['left', 'right', 'backward', 'forward']
    prev_sec = 0

    def __init__(self):
        ShowBase.__init__(self)

        self.setBackgroundColor(0.95, 2.45, 2.45)

        simplepbr.init()


        self.accept('d', self.ChangeSpherePositionRightStart)
        self.accept('d-up', self.ChangeSpherePositionRightEnd)
        self.accept('a', self.ChangeSpherePositionLeftStart)
        self.accept('a-up', self.ChangeSpherePositionLeftEnd)
        self.accept('s', self.ChangeSpherePositionBackwardStart)
        self.accept('s-up', self.ChangeSpherePositionBackwardEnd)
        self.accept('w', self.ChangeSpherePositionForwardStart)
        self.accept('w-up', self.ChangeSpherePositionForwardEnd)
        self.taskMgr.add(self.ChooseDirection)
        self.taskMgr.add(self.MoveFoward)
        self.taskMgr.add(self.MoveBackward)
        self.taskMgr.add(self.MoveLeft)
        self.taskMgr.add(self.MoveRight)
        self.taskMgr.add(self.rotateStar)

        blank_node = PandaNode("my_blank_node")
        self.nodepath1 = NodePath(blank_node)
        self.nodepath1.reparentTo(self.render)

        blank_node2 = PandaNode("my_blank_node2")
        self.nodepath2 = NodePath(blank_node2)
        self.nodepath2.reparentTo(self.render)

        blank_node3 = PandaNode("my_blank_node3")
        self.nodepath3 = NodePath(blank_node3)
        self.nodepath3.reparentTo(self.render)
        

        self.scene = generate.GenerateModel(self, (0,0,-0.5), (200,200,1), (0,0,0), self.nodepath3, "models/plane.bam")
        self.sphObject = generate.GenerateModel(self, (0, 10, 0.1), (0.2, 0.2, 0.2), (0,0,0), self.nodepath2, "models/brain.bam")

        star = None
        total = 0

        addy = 0
        for i in range(10):
            star = generate.GenerateModel(self, (0,25+addy,0.6), (1,1,1), (90,0,0), self.render, "models/star.bam")
            self.obj_coords.append((star, (0,25+addy,0.6)))
            addy+= 10
            total += 1            

        star = None
        addx  = 0
        for i in range(10):
            
            if i == 0:
                star = generate.GenerateModel(self, (0+addx,25+addy,0.6), (1,1,1), (90,0,0), self.render, "models/star.bam")
                self.obj_coords.append((star, (0+addx,25+addy,0.6)))
            else:
                star = generate.GenerateModel(self, (0+addx,25+addy,0.6), (1,1,1), (0,0,0), self.render, "models/star.bam") 
                self.obj_coords.append((star, (0+addx,25+addy,0.6)))

            total += 1
            
            addx += 10

            


        star = None
        for i in range(10):
            if i == 0:
                star = generate.GenerateModel(self, (0+addx,25+addy,0.6), (1,1,1), (0,0,0), self.render, "models/star.bam")
            else:
                star = generate.GenerateModel(self, (0+addx,25+addy,0.6), (1,1,1), (90,0,0), self.render, "models/star.bam") 
                
            self.obj_coords.append((star, (0+addx,25+addy,0.6)))
            
            total += 1

            addy -= 10


        self.sphObject.setH(self.angle)

        self.dlnp = generate.SetLight(self, "my dlight", 'd', 0, self.nodepath2)

    def cameraSet(self, sph_heading):


        self.camera_pos = self.sphObject.getPos() + Vec3(math.sin(math.radians(sph_heading)), math.cos(math.radians(sph_heading)), 0.1) * 10
        self.xCoord = self.camera_pos[0] 
        self.yCoord = self.camera_pos[1] 

        self.camera.setPos(self.camera_pos)
        self.camera.lookAt(self.sphObject)


    def ChangeSpherePositionBackwardStart(self):
        self.isMovingBackward = True

    def ChangeSpherePositionBackwardEnd(self):
        self.isMovingBackward = False

    def MoveBackward(self, task):
        if self.isMovingBackward == True:
            self.sphObject.setPos(self.sphObject.getPos() + Vec3(math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle)), 0) * 0.5 )

            self.cameraSet(self.fakeHeading)

        if self.camera.getHpr()[0] > 0:

            self.sphObject.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))

        else:
            self.sphObject.setHpr(Vec3(-(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(-(self.fakeHeading-180), 0,0))
         

        return task.cont    

    def ChangeSpherePositionForwardStart(self):
        self.isMovingForward = True
            

    def ChangeSpherePositionForwardEnd(self):
        self.isMovingForward = False
            



    def MoveFoward(self, task):
        if self.isMovingForward == True:
            self.sphObject.setPos(self.sphObject.getPos() + Vec3(math.sin(math.radians(self.angle+180)), math.cos(math.radians(self.angle+180)), 0) * 0.5 )


            self.cameraSet(self.fakeHeading)

        if self.camera.getHpr()[0] > 0:

            self.sphObject.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))

        else:
            self.sphObject.setHpr(Vec3(-(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(-(self.fakeHeading-180), 0,0))


        return task.cont

    def ChangeSpherePositionRightStart(self):
        self.isMovingRight = True

    def ChangeSpherePositionRightEnd(self):
        self.isMovingRight = False

    def MoveRight(self, task):
        if self.isMovingRight == True:
            self.angle += 2.5
            
            self.fakeHeading += 2.5


            self.cameraSet(self.fakeHeading)

        if self.camera.getHpr()[0] > 0:

            self.sphObject.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))

        else:
            self.sphObject.setHpr(Vec3(-(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(-(self.fakeHeading-180), 0,0))


        return task.cont
    

    def ChangeSpherePositionLeftStart(self):
        self.isMovingLeft = True
    
    def ChangeSpherePositionLeftEnd(self):
        self.isMovingLeft = False

    def MoveLeft(self, task):
        if self.isMovingLeft == True:
            self.angle -= 2.5


            self.fakeHeading -= 2.5

            self.cameraSet(self.fakeHeading)

        if self.camera.getHpr()[0] > 0:

            self.sphObject.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))

        else:
            self.sphObject.setHpr(Vec3(-(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(-(self.fakeHeading-180), 0,0))



        return task.cont

    def rotateStar(self, task):
        if self.obj_coords:
            for i in self.obj_coords:
                if not i[0].isEmpty():
                    angleDegrees = task.time * 150.0 % 360.0
                    i[0].setHpr(angleDegrees % 360, 0, 0)
            return Task.cont
        else:
            return Task.done



    def ChooseDirection(self, task):

        self.textNode.clear()
        self.textNode.setText('x: ' + str(round(self.sphObject.getPos()[0],2)) + ' y:' + str(round(self.sphObject.getPos()[1],2)))
        self.textNode.setTextColor(0, 0, 0, 1)
        textNodePath = self.aspect2d.attachNewNode(self.textNode)
        x = -self.get_aspect_ratio() + 0.1
        y = 0.9
        textNodePath.setPos(x, 0, y)        
        textNodePath.setScale(0.1)

        self.scoreNode.clear()
        self.scoreNode.setText("Score: " + str(self.score))
        self.scoreNode.setTextColor(0, 0, 0, 1)
        scoreNodePath = self.aspect2d.attachNewNode(self.scoreNode)
        x = -self.get_aspect_ratio() + 0.1
        y = 0.8
        scoreNodePath.setPos(x, 0, y)        
        scoreNodePath.setScale(0.1)


        self.cameraSet(self.fakeHeading)

        if self.camera.getHpr()[0] > 0:

            self.sphObject.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(abs(self.fakeHeading-180), 0,0))

        else:
            self.sphObject.setHpr(Vec3(-(self.fakeHeading-180), 0,0))
            self.dlnp.setHpr(Vec3(-(self.fakeHeading-180), 0,0))



        if abs(self.fakeHeading) >= 360:
            self.fakeHeading = 0


        pos = tuple(self.sphObject.getPos())
        


        self.index = 0
        


        for i in self.obj_coords:

            pos_tuple = tuple(pos)
            diff_x = i[1][0] - pos_tuple[0]
            diff_y = i[1][1] - pos_tuple[1]
            diff_z = i[1][2] - pos_tuple[2]

            if abs(diff_x) <= 1 and abs(diff_y) <= 1 and abs(diff_z) <= 1:
                
                star_to_delete = i[0]
                star_to_delete.removeNode() 

                self.score = self.score + 1

                self.obj_coords[self.index][0].removeNode()

                del self.obj_coords[self.index]


                break

            self.index = self.index +1
        
        return task.cont


game = MyApp()

game.run()


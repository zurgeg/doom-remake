from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.ode import OdeWorld
from panda3d.ode import OdeBody, OdeMass
import keyboard
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp
height = 1.75
radius = 0.4

class App(ShowBase):
    def moveForward(self,catch):
        print('w key pressed')
        self.cy = 3.0
        print(self.current_pos)
    def moveBackward(self,catch):
        print('w key pressed')
        self.cy = -3.0
        print(self.current_pos)
    def moveLeft(self,catch):
        print('w key pressed')
        self.cx = 3.0
        print(self.current_pos)
    def moveRight(self,catch):
        print('w key pressed')
        self.cx = -3.0
        print(self.current_pos)
    def lookLeft(self,catch):
        self.current_omega = 120
    def lookRight(self,catch):
        self.current_omega = -120
    def lookUp(self,catch):
        self.current_hpr = (self.current_hpr[0],self.current_hpr[1] - 1,self.current_hpr[2])

    def moveUp(self,catch):
        self.current_pos = (self.current_pos[0],self.current_pos[1],self.current_pos[2] + 1)
    def lookUp(self,catch):
        self.current_hpr = (self.current_hpr[0],self.current_hpr[1] + 1,self.current_hpr[2])
    def lookDown(self,catch):
        self.current_hpr = (self.current_hpr[0],self.current_hpr[1] - 1,self.current_hpr[2])

    def fire(self,catch):
        print("Fire!")
        if self.pandaPos[0] == self.current_pos[0] and self.pandaPos[2] + 0.5 == self.current_pos[2] and not self.pandaPos[1] == self.current_pos[1] and not self.pandaPos[1] - 1 == self.current_pos[1] and not self.current_pos[1] - 1 == self.pandaPos[1] and not self.current_pos[1] > self.pandaPos[1]:
            print('Oof')

    def jump(self,catch):
        self.player.setMaxJumpHeight(5.0)
        self.player.setJumpSpeed(8.0)
        self.player.doJump()
    def __init__(self):
        ShowBase.__init__(self)
        #self.word = BulletWorld()
        self.cx = 0.0
        self.cy = 0.0
        self.current_omega = 0
        s = self.loader.loadSfx('Doom Soundtrack - Level 1 (Extended).mp3')
        s.play()
        self.current_pos = (10, 5, 1)
        self.current_hpr = (0,0,0)
        #self.fxboy = self.loader.loadModel("cubearm.egg")
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -12.0))
        #self.physicsMgr.attachPhysicalNode(self.camera)
        keyboard.on_press_key('w', self.moveForward)
        keyboard.on_press_key('s', self.moveBackward)
        keyboard.on_press_key('j',self.lookLeft)
        keyboard.on_press_key('y',self.lookUp)
        keyboard.on_press_key('h',self.lookDown)
        keyboard.on_press_key('g',self.lookRight)
        keyboard.on_press_key('d', self.moveLeft)
        #self.fxboy.reparentTo(self.render)
        #self.camera.reparentTo(self.render)
        #self.camera.reparentTo(self.fxboy)
        keyboard.on_press_key('a', self.moveRight)
        keyboard.on_press_key('space', self.fire)
        keyboard.on_press_key('2',self.jump)
        #keyboard.on_press_key('y',self.lookUp)
        keyboard.on_press_key('1',self.moveUp)
        
        self.cam = BulletCapsuleShape(radius, height - 2*radius, ZUp)
        self.player = BulletCharacterControllerNode(self.cam,0.4,'Player')
        self.playernp = self.render.attachNewNode(self.player)
        self.world.attachCharacter(self.playernp.node())
        self.camera.reparentTo(self.playernp)
        self.playernp.setPos(self.current_pos)
        self.playernp.setHpr(self.current_hpr)
        self.playernp.setH(45)
        #self.player.setMass(10.0)
        # self.playernp.setCollideMask(BitMask32.allOn())
        self.disableMouse()

        self.scenes = BulletBoxShape(Vec3(0.25,0.25,0.25))
        self.scenenode = BulletRigidBodyNode('Scene')
        self.scenenode.setMass(12.0)
        self.scenenode.addShape(self.scenes)
        self.scenenp = render.attachNewNode(self.scenenode)
        self.scenenp.setPos(-8,40,0)
        self.world.attachRigidBody(self.scenenode)
        self.scene = self.loader.loadModel("models/environment.egg.pz")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25,0.25,0.25)
        self.scene.setPos(-8,40,0)
        self.scene.reparentTo(self.scenenp)
        
        #self.taskMgr.add(self.spinCameraTask,"SpinCameraTask")
        self.taskMgr.add(self.moveChar,"MoveChar")
        self.taskMgr.add(self.moveCBod,"MoveCBod")
        self.pandaActor = Actor("cubearm.egg",{"walk":"cubearm4-ArmatureAction.egg"})
        self.pandaActor.setScale(0.12,0.12,0.12)
        self.pandaActor.setPos((10,10,0.5))
        self.pandaPos = (10,10,0.5)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop('walk')
        '''
        posInterval1 = self.pandaActor.posInterval(13,Point3(0,-10,0),startPos=Point3(0,10,0))
        posInterval2 = self.pandaActor.posInterval(13,Point3(0,10,0),startPos=Point3(0,-10,0))
        hprInterval1 = self.pandaActor.hprInterval(3,Point3(180,0,0),startHpr=Point3(0,0,0))
        hprInterval2 = self.pandaActor.hprInterval(3,Point3(0,0,0),startHpr=Point3(180,0,0))
        self.pandaPace = Sequence(posInterval1,hprInterval1,posInterval2,hprInterval2,name="pandaPace")
        self.pandaPace.loop()
        '''
    
    def spinCameraTask(self,task):
        print(task.time * 6.0)
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians),3)
        self.camera.setHpr(angleDegrees,0,0)
        return Task.cont
    def moveChar(self,task):
        speed = Vec3(0,0,0)
        omega = self.current_omega
        speed.setX(self.cx)
        speed.setY(self.cy)
        #self.scenenp.setPos(-8,40,0)
        print('[Scene]: ' + str(self.scenenp.getPos()))
        print('[Cam]: ' + str(self.playernp.getPos()))
        self.player.setAngularMovement(omega)
        #self.player.setLinearMovement(speed,True)
        #self.playernp.setPos(self.current_pos)
        self.playernp.setHpr(self.current_hpr)
    
        return task.cont
    def moveCBod(self,task):
        self.world.doPhysics(globalClock.getDt())
        return task.cont
    
app = App()
app.run()

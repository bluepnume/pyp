from __future__ import division

import pyglet

from . import AdventureBase
from .scene import Scene

from .framework.children import AddChild, AddChildren, ParentProxy
from .framework.save import Save
from .framework.event import Event
from .framework.utils import cacheprop

from operator import sub
from math import hypot, acos, pi, sqrt, copysign

class Entity(AdventureBase):
  
  coordinates = Save((0, 0))
  
  image = None
  staticimage = None
  route = None
  animation = None
  
  speed = 2
  
  actions = AddChildren()
  
  moveright   = AddChild()
  moveleft    = AddChild()
  moveup      = AddChild()
  movedown    = AddChild()
  
  onMove = Event('onMove')
  onArrive = Event('onArrive')
  
  drawgroup = AdventureBase.fg
  
  @Scene.onActivate.callback
  def activate(self):
    self.moveleft.activate(static=True)
    self.sprite = self.animation.sprite
    self.sprite.x, self.sprite.y = self.coordinates
    
  def deactivate(self):
    self.animation.deactivate()
    
  @property
  def x(self):
    return self.coord[0]
    
  @property
  def y(self):
    return self.coord[1]
    
  @property
  def coord(self):
    return tuple(map(int, self.coordinates))
    
  @coord.setter
  def coord(self, value):
    self.coordinates = value
    
  @property
  def invx(self):
    return self.adventure.width + self.adventure.xoffset - self.x
    
  @property
  def invy(self):
    return self.adventure.height + self.adventure.yoffset - self.y
    
  def anchor(self, frame):
    frame.anchor_x = frame.width / 2
    frame.anchor_y = frame.height / 2
    return frame
    
  @property
  def scene(self):
    return self.adventure.activescene
    
  def enter(self, scene):
    self.coord = scene.paths[0][0]
    
  def activateanimation(self, anim):
    self.animation = anim
    
  def move(self, coord):
    self.onArrive.flush()
    if self.onMove.trigger():
      self.route = self.scene.getroute(self, coord)
      self.getdestination(self.coord)
      self.animation.start()
    
  def update(self):
    if self.route:
      self.animation.update()
      if self.steps:
        self.steps -= 1
        x, y = self.coordinates
        self.sprite.x, self.sprite.y = self.coordinates = (x + self.xvel, y + self.yvel)
      else:
        start = self.route.pop(0)
        if self.route:
          self.getdestination(start)
        else:
          self.animation.stop()
          self.onArrive.trigger()
    
  def getdestination(self, start):
    
    self.startpoint, self.destination = start, self.route[0]
    xdist, ydist = map(sub, self.destination, self.startpoint)
    
    x2, y2 = xdist**2, ydist**2
    x2plusy2 = x2 + y2
    
    self.steps = 0
    if x2plusy2:
      self.xvel = self.speed * copysign(sqrt(x2/x2plusy2), xdist)
      self.yvel = self.speed * copysign(sqrt(y2/x2plusy2), ydist)
      if xdist and self.xvel:
        self.steps = int(xdist / self.xvel)
      elif ydist and self.yvel:
        self.steps = int(ydist / self.yvel)
    else:
      self.xvel = 0
      self.yvel = 0
    
    if 0:#abs(ydist) > abs(xdist):
      if self.yvel > 0:
        self.moveup.activate()
      else:
        self.movedown.activate()
    else:
      if self.xvel > 0:
        self.moveright.activate()
      elif self.xvel < 0:
        self.moveleft.activate()

#!/usr/bin/python

from __future__ import division

import os, pyglet, pickle

from .window import Window

from .framework.children import AddChild, AddChildren
from .framework.save import Save
from .framework.utils import cacheprop

import random

class Adventure(Window):
  
  # Children 
  scenes     = AddChildren()
  mainscene  = AddChild(scenes)
  characters = AddChildren()
  mainchar   = AddChild()
  
  # Misc
  xpanspeed = 2
  ypanspeed = 2
  xpandivisor = 3
  ypandivisor = 2
  
  # Persistent
  activescene = Save(instance=True)
  
  # Defaults
  xpan = 0
  ypan = 0
  activeconvo = None
  
  def new(self):
    self.activescene = self.mainscene
  
  def activate(self):
    
    if os.path.exists('test.save'):
      self.load()
      self.activatescene()
    else:
      self.activatescene(self.mainscene)
      self.mainchar.enter(self.activescene)
      
    self.focuscamera()
    
  '''def load(self):
    super(Adventure, self).load()
    self.activescene.activate()'''
    
  def on_close(self):
    self.save()
    
  @cacheprop
  def cursor(self):
    hotspot = self.cursorhotspot
    image = pyglet.image.load(self.cursorimage)
    if hotspot is None:
      hotspot = (int(image.width / 2), int(image.height / 2))
    return pyglet.window.ImageMouseCursor(image, *hotspot)
    
  @cacheprop
  def activecursor(self):
    hotspot =  self.cursorhotspot if self.activecursorhotspot is None else self.activecursorhotspot
    image = pyglet.image.load(self.cursorimage if self.activecursorimage is None else self.activecursorimage)
    if hotspot is None:
      hotspot = (int(image.width / 2), int(image.height / 2))
    return pyglet.window.ImageMouseCursor(image, *hotspot)
    
  def activatecursor(self):
    self.window.set_mouse_cursor(self.cursor)
    
  def activateactivecursor(self, name=None):
    self.window.set_mouse_cursor(self.activecursor)
    
  def update(self, dt):
    if self.xpan > 0:
      remaining = (self.activescene.maxwidth - self.width - self.xoffset)
      if remaining < self.xpanspeed:
        self.xpan = 0
        self.xoffset = self.activescene.maxwidth - self.width
      else:
        self.xpan -= self.xpanspeed
        self.xoffset += self.xpanspeed
      #self.onMouseMove(self.mousex, self.mousey, dx=0, dy=0)
    if self.xpan < 0:
      if self.xpanspeed > self.xoffset:
        self.xpan = 0
        self.xoffset = 0
      else:
        self.xpan += self.xpanspeed
        self.xoffset -= self.xpanspeed
      #self.onMouseMove(self.mousex, self.mousey, dx=0, dy=0)
        
    self.activescene.update()
    self.mainchar.update()
    
  def enterscene(self):
    self.mainchar.enter(self.activescene)
    self.focuscamera()
    
  def activatescene(self, scene=None):
    if not scene is None:
      self.activescene = scene
    self.window.set_size(self.windowwidth or self.activescene.maxwidth, self.windowheight or self.activescene.maxheight)
    self.activescene.activate()
    self.adjustcamera()
    self.focuscamera()
    self.activatecursor()
    
    
  '''grid = pyglet.image.ImageGrid(pyglet.image.load('anims/guybrush/walk.png'), 1, 6)
  an = grid.get_animation(.1)
  sp = pyglet.sprite.Sprite(an, x=0, y=0)'''

#!/usr/bin/python

from __future__ import division

import pyglet

from operator import add, sub
from math import hypot
from itertools import chain

from . import AdventureBase

from .framework.children import AddChild, AddChildren, ParentProxy
from .framework.save import Save
from .framework.event import Event
from .framework.utils import cacheprop

from .adv import Adventure
from .nav import Nav

class Scene(Nav):
  
  backgroundimage = None
  route = None
  
  drawroute = False
  
  music = None
  
  hotspots = AddChildren()
  characters = AddChildren(hotspots)
  portals = AddChildren(hotspots)
  items = AddChildren()
  
  onClick = Adventure.onClick.proxy
  onMouseMove = Adventure.onMouseMove.proxy
  
  onEnter = Event('onEnter')
  onLeave = Event('onLeave')
  
  onActivate = Event('onActivate')
  
  @property
  def active(self):
    return self.adventure.activescene is self
    
  @property
  def maxwidth(self):
    return self.background.width

  @property
  def maxheight(self):
    return self.background.height
    
  @cacheprop
  def aspectratio(self):
    return self.maxwidth / self.maxheight
    

    
  @cacheprop
  def background(self):
    return pyglet.image.load(self.backgroundimage)
    
  def update(self):
    pass
    
  '''@cacheprop
  def audio(self):
    return pyglet.resource.media(self.music).play()'''
  audio = None
  
  def enter(self):
    self.adventure.enterscene()
    
  def activate(self):
    if self.onActivate.trigger():
      self.bgsprite = pyglet.sprite.Sprite(self.background, batch=self.screen, group=self.bg)
      if self.music:
        if not self.audio:
          self.audio = pyglet.media.Player()
          self.audio.queue(pyglet.resource.media(self.music))
          self.audio.eos_action = self.audio.EOS_LOOP
        self.audio.play()
     
  @onLeave.callback
  def deactivate(self):
    self.bgsprite.delete()
    if self.audio:
      self.audio.pause()
    
  def getroute(self, sprite, endcoord):
    
    startpoint, startpair = self.nearestpoint(sprite.coord)
    endpoint,   endpair   = self.nearestpoint(endcoord)
    
    if startpair == endpair:
      route = []
    else:
      for point in startpair:
        if point in endpair:
          route = [point]
          break
      else:
        route = self.findpath(startpair[0], endpair[0])
        if not startpair[1] in route:
          route.insert(0, startpair[0])
        if not endpair[1] in route:
          route.append(endpair[0])
      
    route.append(endpoint)
      
    return route
      
      
  def nearestpoint(self, coord):
    distance, point, pair = min(self.nearestpoints(coord))
    return point, tuple(pair)
           
  def nearestpoints(self, coord):
    for pair in self.pairs:
      point = pair.nearestpoint(coord)
      diff = map(sub, coord, point)
      distance = hypot(*diff)
      yield distance, point, pair

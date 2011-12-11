from __future__ import division

from operator import add, sub

from . import AdventureBase
from .window import Window

from .framework.children import AddChild, AddChildren, ParentProxy
from .framework.save import Save
from .framework.event import Event
from .framework.utils import cacheprop

from .sprite import Entity

class MainCharacter(Entity):
  
  onArrive = Entity.onArrive.proxy
  
  drawgroup = AdventureBase.mg
  
  @Window.onClick.callback
  def movechar(self, x, y, button, modifiers):
    self.move((x, y))
  
  def update(self):
    Entity.update(self)
    if self.x - self.adventure.xoffset < self.adventure.xpandistance:
      self.adventure.panleft()
    elif self.invx < self.adventure.xpandistance:
      self.adventure.panright()


from .hotspot import HotSpot

class Object(Entity, HotSpot):

  @cacheprop
  def region(self):
    halfdimensions = (self.sprite.width / 2, self.sprite.height / 2)
    return (map(int, map(sub, self.coord, halfdimensions)), map(int, map(add, self.coord, halfdimensions)))
    
  def draw(self):
    Entity.draw(self)
    HotSpot.draw(self)

    
    
class Item(Object):
  
  movexoffset = 20
  moveyoffset = 20
  
  pickedup = False
  
  @Object.onEngage.callback
  def pickup(self):
    self.pickedup = True
    
  def draw(self):
    super(Item, self).draw()
    if not self.pickedup:
      Object.draw(self)
  

class Character(Object):
  
  movexoffset = 40
  moveyoffset = 20
  
  conversations = AddChildren()

  @Object.onEngage.callback
  def arrive(self):
    convo = self.conversations[0]
    convo.activate()


# if obj is an instance of event's class --> callback should only be fired for specific object, not all children

# specific object == self.obj

# (self.obj == obj) == isinstance(obj, self.originalowner)

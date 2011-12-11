import pyglet

from .scene import Scene
from .char import MainCharacter

from . import AdventureBase

from .framework.children import ParentProxy
from .framework.event import Event
from .framework.utils import cacheprop

class HotSpot(AdventureBase):
  
  region = None
  scene = ParentProxy()
  move = True
  movexoffset = 0
  moveyoffset = 0
  engaged = False
  
  labelsize = 30
  
  mouseover = False
  
  onMouseOver = Event('onMouseOver')
  onMouseLeave = Event('onMouseLeave')
  onClick = Event('onClick')
  onEngage = Event('onEngage')
  
  def inregion(self, x, y):
    start, end = self.region
    if start[0] <= x <= end[0] and start[1] <= y <= end[1]: #TODO: this better?
      return True
    return False
    
  '''@cacheprop  
  def label(self):
    start, end = self.region
    return pyglet.text.Label(self.name, font_name=self.adventure.defaultfont, font_size=self.labelsize, x=end[0], y=end[1])'''
  
  @Scene.onClick.callback
  def click(self, x, y, button, modifiers):
    if self.inregion(x, y):
      return self.onClick.trigger()
    self.engaged = False
      
  @Scene.onMouseMove.callback
  def mouse(self, x, y, dx, dy):
    if self.inregion(x, y):
      #print len(self.static.image_data.get_data('A', self.static.width))
      ''''for row in self.static.image_data.get_data('A', self.static.width).split('\n'):
        print len(row)
        for char in row:
          if char == '\x00':
            sys.stdout.write(' ')
          else:
            sys.stdout.write('#')
        sys.stdout.write('\n')'''
      if not self.mouseover:
        self.mouseover = True
        if self.onMouseOver.trigger():
          start, end = self.region
          #self.label = pyglet.text.Label(self.name, font_name=self.adventure.defaultfont, font_size=self.labelsize, x=x, y=y, batch=self.overlay)
    else:
      if self.mouseover:
        self.mouseover = False
        if self.onMouseLeave.trigger():
          pass
          #self.label.delete()
        
  @onMouseOver.callback
  def activecursor(self):
    self.adventure.activateactivecursor()
    
  @onMouseLeave.callback
  def passivecursor(self):
    self.adventure.activatecursor()
    
  @onMouseOver.callback
  def namelabel(self):
    self.label = pyglet.text.Label(self.name, font_name=self.adventure.defaultfont, font_size=self.labelsize, x=50, y=50, batch=self.overlay)
    self.onMouseLeave.once(self.label.delete)
      
  @cacheprop
  def midpoint(self):
    return tuple(i//2 for i in map(sum, zip(*self.region)))
    
  @onClick.callback
  def moveto(self):
    if self.move and not self.engaged:
      point = self.midpoint
      movexoffset = self.movexoffset
      xdist = self.adventure.mainchar.x - point[0]
      if xdist > 0:
        movexoffset = -movexoffset
      point = (point[0] - movexoffset, point[1])
      self.adventure.mainchar.move(point)
      self.engaged = True
      MainCharacter.onArrive.once(self.onEngage)
    return False
      
  @onEngage.callback
  def flip(self):
    mainchar = self.adventure.mainchar
    (mainchar.moveright if mainchar.x < self.x else mainchar.moveleft).activate(static=True)
  
class Portal(HotSpot):
    
  @HotSpot.onEngage.callback
  def arrive(self):
    self.adventure.activatescene(self.paired.scene, position=self.paired.midpoint)

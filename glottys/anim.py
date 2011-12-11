import pyglet

from itertools import cycle

from . import AdventureBase
from .sprite import Entity

from .framework.children import ParentProxy
from .framework.utils import cacheprop

class Animation(AdventureBase):
  
  staticframe = None
  frames = None
  timestep = 5
  
  flip_x = False
  flip_y = False
  
  anchorpoint = None
  
  sprite = ParentProxy()
    
  @cacheprop
  def loadedframes(self):
    return cycle(map(self.anchor, (pyglet.resource.image(frame, flip_x=self.flip_x, flip_y=self.flip_y) for frame in self.frames)))
    
  @cacheprop
  def loadedstaticframe(self):
    loadedstaticframe = pyglet.resource.image(self.staticframe, flip_x=self.flip_x, flip_y=self.flip_y)
    self.anchor(loadedstaticframe)
    return loadedstaticframe
    
  def anchor(self, frame):
    if self.anchorpoint:
      frame.anchor_x, frame.anchor_y = self.anchorpoint
    else:
      frame.anchor_x, frame.anchor_y = frame.width / 2, frame.height / 2
    return frame
    
  def update(self):
    if not self.static:
      if self.step:
        self.step -= 1
      else:
        self.step = self.timestep
        self.sprite.image = self.loadedframes.next()
    
  def activate(self, static=False):
    self.sprite.activateanimation(self)
    self.step = 0
    self.static = static
    if static:
      self.stop()
    self.update()
      
  def stop(self):
    self.sprite.image = self.loadedstaticframe

class Anim2(Animation):
  
  framenumber = 0
  
  @cacheprop
  def loadedframes(self):
    grid = pyglet.image.ImageGrid(pyglet.image.load(self.frames), 1, self.framenumber)
    map(self.anchor, grid)
    return cycle(grid)
    return cycle(map(self.anchor, (pyglet.resource.image(frame, flip_x=self.flip_x, flip_y=self.flip_y) for frame in self.frames)))
    
    
class Anim(AdventureBase):
  
  timestep = 5
  
  anchorpoint = None
  
  flip_x = False
  flip_y = False
  
  spritesheet = None
  staticimage = None
  frames = 1
  
  stopped = True
  
  entity = ParentProxy()
  sprite = None
  
  active = False
  
  @property
  def x(self):
    return self.entity.x
    
  @property
  def y(self):
    return self.entity.y
    
  @cacheprop
  def animation(self):
    if not self.spritesheet:
      return self.static
    image = pyglet.image.load(self.spritesheet)
    imagegrid = pyglet.image.ImageGrid(image, 1, self.frames)
    for frame in imagegrid:
      self.anchor(frame)
    animation = imagegrid.get_animation(float(self.timestep) / self.adventure.fps).get_transform(flip_x=self.flip_x, flip_y=self.flip_y)
    return animation
    
  @cacheprop
  def static(self):
    staticimage = pyglet.resource.image(self.staticimage, flip_x=self.flip_x, flip_y=self.flip_y)
    self.anchor(staticimage)
    return staticimage
    
  def deletesprite(self):
    if self.sprite:
      self.sprite.delete()
      self.sprite = None
  
  def start(self):
    self.deletesprite()
    self.sprite = pyglet.sprite.Sprite(self.animation, batch=self.screen, group=self.mg)
    self.stopped = False
    self.parent.sprite = self.sprite
    self.setposition()
    
  def stop(self):
    self.deletesprite()
    self.sprite = pyglet.sprite.Sprite(self.static, batch=self.screen, group=self.mg)
    self.stopped = True
    self.parent.sprite = self.sprite
    self.setposition()
    
  def setposition(self):
    self.sprite.x, self.sprite.y = self.entity.coord
    
  def anchor(self, frame):
    if self.anchorpoint:
      frame.anchor_x, frame.anchor_y = self.anchorpoint
    else:
      frame.anchor_x, frame.anchor_y = frame.width / 2, frame.height / 2
    
  def update(self):
    pass
    
  def activate(self, static=False):
    if self.parent.animation:
      self.parent.animation.deactivate()
    self.active = True
    self.parent.animation = self
    if static:
      self.stop()
    else:
      self.start()
    
  def deactivate(self):
    self.active = False
    self.deletesprite()


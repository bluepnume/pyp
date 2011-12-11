import os, pyglet

from itertools import chain

from .framework.event import Event

from . import AdventureBase

#pyglet.options['debug_gl'] = False
from pyglet.gl import *

from pyglet.gl import glTranslatef, glLoadIdentity
from pyglet.window import key

class Window(AdventureBase):
  
  # Window
  title = None
  icon  = None
  fps   = 60
  width = None
  height = None
  minwidth = 480
  minheight = 340
  scalefilter = False
  
  # Cursor
  cursorimage = None
  cursorhotspot = None
  activecursorimage = None
  activecursorhotspot = None
  
  # Events
  onClick            = Event('onClick')
  onOverlayClick     = Event('onOverlayClick')
  onMouseMove        = Event('onMouseMove')
  onClickHotspot     = Event('onClickHotspot')
  onMouseoverHotspot = Event('onMouseoverHotspot')
  onWindowResize     = Event('onWindowResize')
  
  # Misc
  fontfiles = None
  defaultfont = ('Arial',)
  
  # Defaults
  xoffset = 0
  yoffset = 0
  
  period = 1.0 / fps
  
  def run(self):
    
    self.window = pyglet.window.Window(caption=self.title or self.name, resizable=True)
    self.window.push_handlers(self)
    self.window.set_minimum_size(self.minwidth, self.minheight)
    
    #pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)                         
    #pyglet.gl.glEnable(pyglet.gl.GL_BLEND)  
    pyglet.clock.schedule_interval(self.update, self.period)
    
    if self.fontfiles:
      for fontfile in self.fontfiles:
        pyglet.font.add_file(fontfile)
        
    self.activatecursor()
    if self.icon:
      self.window.set_icon(pyglet.image.load(self.icon))
    
    self.activate()
    
    pyglet.app.run()


  def activate(self):
    pass

  @onWindowResize.callback
  def adjustcamera(self, width=None, height=None):
    
    width = self.windowwidth = width or self.windowwidth
    height = self.windowheight = height or self.windowheight

    aspectratio = width / height
    if aspectratio < self.activescene.aspectratio:
      self.height = self.activescene.maxheight
      self.scale = height / self.height
      self.width = int(width / self.scale)
    else:
      self.width = self.activescene.maxwidth
      self.scale = width / self.width
      self.height = int(height / self.scale)
    
    self.buffer_manager = pyglet.image.get_buffer_manager()
    self.scaletexture = pyglet.image.Texture.create(self.width, self.height, rectangle=True)
    if not self.scalefilter:
      pyglet.gl.glTexParameteri(self.scaletexture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
      pyglet.gl.glTexParameteri(self.scaletexture.target, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
    
    self.focuscamera()
    
  @onOverlayClick.wrap
  def on_mouse_press(self, x, y, button, modifiers):
    return x, y, button, modifiers
    
  @onClick.wrap
  @onOverlayClick.callback
  def on_mouse_press(self, x, y, button, modifiers):
    x = self.mousex = int(x/self.scale + self.xoffset)
    y = self.mousey = int(y/self.scale + self.yoffset)
    return x, y, button, modifiers
    
  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    return self.on_mouse_motion(x, y, dx, dy)
  
  #@onMouseMove.wrap
  def on_mouse_motion(self, x, y, dx, dy):
    x = self.mousex = int(x/self.scale  + self.xoffset)
    y = self.mousey = int(y/self.scale  + self.yoffset)
    return x, y, dx, dy

  def on_draw(self):

    # Start scaling and translating output
    
    glViewport(0, 0, self.width, self.height)
    self.set_projection(self.width, self.height)
    glTranslatef(-self.xoffset, -self.yoffset, 0)

    # Clear window and draw frame
    
    self.window.clear()
    self.screen.draw()
        
    # Finish scaling and translating output
    
    self.scaletexture.blit_into(self.buffer_manager.get_color_buffer(), 0, 0, 0)
    glViewport(0, 0, self.window.width, self.window.height)
    self.set_projection(self.window.width, self.window.height)
    glLoadIdentity()
    self.scaletexture.blit(0, 0, width=self.window.width, height=self.window.height)
    
    self.overlay.draw()
    
  def overlaycoord(self, x, y):
    return (x - self.xoffset) * self.scale, (y - self.yoffset) * self.scale
    
  def set_projection(self, width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    
  def on_resize(self, width=None, height=None):
    self.onWindowResize.trigger(width, height)
    
  def focuscamera(self):
    
    self.xoffset = int(self.mainchar.x - (self.width / 2))
    self.yoffset = int(self.mainchar.y - (self.height / 2))
    self.xpan = 0
    self.ypan = 0
    
    if self.right > self.activescene.maxwidth:
      self.xoffset = self.activescene.maxwidth - self.width
    elif self.xoffset < 0:
      self.xoffset = 0
    if self.top > self.activescene.maxheight:
      self.yoffset = self.activescene.maxheight - self.height
    elif self.yoffset < 0:
      self.yoffset = 0
      
  def panleft(self):
    self.xpan = -self.xpandistance
    
  def panright(self):
    self.xpan = self.xpandistance
  
  @property
  def right(self):
    return self.width + self.xoffset
    
  @property
  def top(self):
    return self.height + self.yoffset
    
  @property
  def xpandistance(self):
    return (self.width / self.xpandivisor) - self.xpanspeed
    
  @property
  def ypandistance(self):
    return (self.height / self.ypandivisor) - self.xpanspeed

  def on_key_press(self, symbol, modifiers):
    if symbol == key.ENTER and modifiers & key.MOD_ALT:
      self.window.set_fullscreen(not self.window.fullscreen)

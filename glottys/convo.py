import pyglet

from . import AdventureBase

from .framework.children import AddChildren, ParentProxy
from .framework.utils import cacheprop

from .adv import Adventure
from .char import MainCharacter



class Thread(AdventureBase):
  
  query = None
  response = None

  automatic = False
  persistent = False
  locked = False
  
  allowmove = True
  
  char = ParentProxy()
  
  threads = AddChildren()
  
  vertex = None
  
  active = False
  
  def activate(self):
    self.active = True
    self.adventure.activeconvo = self
    self.initiate()
    
  @MainCharacter.onMove.callback
  def deactivate(self):
    if not self.allowmove:
      return False
    self.active = False
    self.adventure.activeconvo = None
    self.vertex.delete()
    self.text.delete()
    
  @property
  def unlockedthreads(self):
    return [child for child in self.threads if not child.locked]
    
  @cacheprop
  def formattext(self):
    return '%s: %%s' % self.char.name
    
  @cacheprop
  def queryduration(self):
    return len(self.query.split()) / 2
    
  @cacheprop
  def responseduration(self):
    return len(self.query.split()) / 2
    
  def settext(self, text):
    self.text = pyglet.text.Label(text, font_name=self.adventure.defaultfont, font_size=int(self.adventure.window.height/30), x=60, y=30, width=self.adventure.window.width-60, multiline=True, batch=self.overlay)
    self.text.anchor_y = 'bottom'
    x1, y1, x2, y2 = 50, 20, self.adventure.window.width-50, self.text.content_height+40
    self.vertex = self.overlay.add(4, pyglet.gl.GL_QUADS, None, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)), ('c4f', [0, 0, 0, .8]*4))
    self.text.batch = self.overlay
    
    
  @Adventure.onWindowResize.callback
  def initiate(self, x=None, y=None):
    
    self.settext('%s: %s' % (self.adventure.mainchar.name, self.query))
    
    self.presentoptions()
    
  def presentoptions(self):
    
    threads = self.unlockedthreads
    
    if not threads:
      return self.endconversation()

    if len(threads) == 1 and threads[0].automatic:
      return self.select(threads[0])

    print
    for i, child in enumerate(threads, 1):
      print '%s: %s' % (i, child.query)
      
    '''while True:
      choice = raw_input('\nChoice: ')
      if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(self.threads):
          break
      print 'Please select a valid query'
      
    return self.select(self.threads[choice-1])'''
    
  def select(self, child):
    
    child.initiate()
    
    if not child.persistent:
      self.threads.remove(child)

    if self.persistent:  
      self.presentoptions()

  def endconversation(self):
    pass

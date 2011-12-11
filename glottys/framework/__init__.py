from functools import partial

from .utils import cacheprop, cachetuple, cacheset

from .event import Event
from .save import Save
    
from .children import AbstractChildrenAdder, AddChildren
    
class FrameWork(object):
  
  parent    = None
  paired    = None
  callbacks = None
  
  active   = True
  modified = False
  
  def __new__(cls, stdatts=dir(object)):
    
    self = object.__new__(cls)
    while self.callbacks:
      self.callbacks.pop()(self)
      
    self.name = cls.__name__
    
    self.children = set()

    Save.add(self)
    self.saveable = {}
    
    atts = dir(cls)
    map(atts.remove, stdatts)
    for name, attribute in ((name, getattr(cls, name)) for name in atts):
      if isinstance(attribute, Save):
        self.saveable[name] = attribute
      elif hasattr(attribute, 'events'):
        for event, instance in attribute.events:
          event.registercallback(attribute.__get__(self, cls), self, instance)
    
    return self
    
  def __call__(self):
    return self
    
  def __invert__(self):
    return self.__class__
    
  @cacheset
  def family(self):
    yield self
    for child in self.children:
      yield child
      for subchild in child.family:
        yield subchild
        
  @cacheprop
  def typefamily(self):
    return map(type, self.family)
    
  @cacheprop
  def itemid(self):
    return Save.getid(self)
   
  @property
  def state(self):
    for name, save in self.saveable.iteritems():
      if save.modified:
        value = save.get(self)
        if save.instance:
          yield name, value.itemid
        else:
          yield name, value
          
  def save(self, filename='test.save'):
    Save.save(filename)
      
  def load(self, filename='test.save'):
    Save.load(filename)
      
  def __ror__(self, other):
    
    def pair(this):
      this.paired, self.paired = self, this
    other.callbacks.append(pair)
    return other

  @cachetuple
  def parents(self):
    parent = self
    while parent:
      yield parent
      parent = parent.parent

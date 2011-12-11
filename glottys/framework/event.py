from functools import wraps
from .utils import cacheprop

def event(callback):
  return

class Event(object):
  
  obj = None
  
  def __init__(self, name):
    self.callbacks = []
    self.proxies = []
    self.oneoffs = []
    
    self.name = name
    
  def callback(self, method):
    if not hasattr(method, 'events'):
      method.events = [(self, self.obj)]
    elif self not in method.events:
      method.events.append((self, self.obj))
    return method
    
  def once(self, callback):
    self.oneoffs.insert(0, callback)
    
  def hook(self, method):
    
    @wraps(method)
    def wrapper(this, *args, **kwargs):
      self.__get__(this, this.__class__)
      if self(*args, **kwargs):
        method(this, *args, **kwargs)
    return wrapper
    
  def wrap(self, method):
    
    @wraps(method)
    def wrapper(this, *args, **kwargs):
      self.__get__(this, this.__class__)
      self.trigger(*method(this, *args, **kwargs), **kwargs)
    return wrapper
    
  def flush(self):
    del self.oneoffs[:]
    
  def registercallback(self, callback, container, instance):
    self.callbacks.append((callback, instance, container))

  @property
  def proxy(self):
    return self
    event = Event()
    self.proxies.append(event)
    return event
    
  def trigger(self, *args, **kwargs):
    
    for callback, instance, container in reversed(self.callbacks):
      if container.active:
        if (instance is None) or (instance is self.obj):
          if (container in self.obj.family or not type(container) in self.obj.typefamily):
            if callback(*args, **kwargs) is False:
              return False
    while self.oneoffs:
      oneoff = self.oneoffs.pop()
      if oneoff.trigger(*args, **kwargs) is False:
        return False
        
    return True
    
  def watch(self, method):
    @wraps(method)
    def triggerwatchevent(this, *args, **kwargs):
      self(*args, **kwargs)
      method(this, *args, **kwargs)
    return triggerwatchevent
    
  def __get__(self, obj, owner):
    self.obj = obj
    return self

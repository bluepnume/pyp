from .utils import cacheprop

class AbstractChildrenAdder(object):
  
  def __init__(self, *collections):
    self.collections = collections
    
  def __call__(self, item):
    item = item()
    self.add(item)
    return item
    
  def add(self, item):
    
    self.append(item)
    item.parent = self.obj
    item.parent.children.add(item)
    
    for collection in self.collections:
      collection.__get__(self.obj).add(item)
      
  def __get__(self, obj, owner):
    self.obj = obj

class AddChildren(object):
  
  class ChildrenList(list, AbstractChildrenAdder):
    
    def __init__(self, *collections):
      list.__init__(self)
      AbstractChildrenAdder.__init__(self, *collections)
  
  def __init__(self, *collections):
    self.objects = {}
    self.collections = collections
    
  def __get__(self, obj, owner=None):
    if obj in self.objects:
      return self.objects[obj]
    children = self.objects[obj] = self.ChildrenList(*self.collections)
    children.__get__(obj, owner)
    return children
    
class AddChild(AbstractChildrenAdder):
  
  item = None
  
  def __init__(self, *collections):
    self.objects = {}
    AbstractChildrenAdder.__init__(self, *collections)
    
  def append(self, item):
    self.objects[self.obj] = item
    
  def __iter__(self):
    return iter((self.objects[self.obj],))
    
  def __get__(self, obj, owner):
    AbstractChildrenAdder.__get__(self, obj, owner)
    return self.objects.get(obj, self)
    
  def __set__(self, obj, value):
    self.obj = obj
    self.objects[obj] = item
    
    
class ParentProxy(object):
    
  def __get__(self, obj, owner):
    if obj:
      return obj.parent
      
class RootProxy(object):
  
  def __init__(self):
    self.items = {}
    
  def __get__(self, obj, owner):
    
    if obj in self.items:
      return self.items[obj]
      
    parent = obj
    while parent:
      if not parent.parent:
        self.items[obj] = parent
        return parent
      parent = parent.parent
      
class InheritableMutable(object):
  
  cls = None
  
  def __init__(self):
    self.items = {}
  
  def __get__(self, obj, owner):
    if owner in self.items:
      return self.items[owner]
    else:
      newobj = self.items[owner] = self.cls()
      return newobj
      
class InheritableList(InheritableMutable):
  cls = list
  

      
def game(cls):
  
  return cls()

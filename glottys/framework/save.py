import json, gzip

class Save(object):
  
  objects = []
  
  @classmethod
  def save(cls, filename):
    with open(filename, mode='w') as savefile:
      data = dict((obj.itemid, dict(obj.state)) for obj in cls.objects if obj.modified)
      json.dump(data, savefile, indent=1)
    
  @classmethod
  def load(cls, filename):
    for itemid, state in json.load(open(filename)).iteritems():
      obj = cls.getitem(int(itemid))
      for name, value in state.iteritems():
        save = obj.saveable[name]
        if save.instance:
          value = cls.getitem(value)
        setattr(obj, name, value)
      
  @classmethod
  def add(cls, obj):
    cls.objects.append(obj)
    
  @classmethod  
  def getid(cls, item):
    return cls.objects.index(item)
  
  @classmethod 
  def getitem(cls, itemid):
    return cls.objects[itemid]
    
    
  modified = False
  instance = False
  
  def __init__(self, default=None, instance=False):
    self.items = {}
    self.default = default
    self.instance = instance
  
  def __get__(self, obj, owner):
    return self.get(obj) if obj else self
    
  def get(self, obj):
    return self.items.get(obj, self.default)
    
  def __set__(self, obj, value):
    self.items[obj] = value
    obj.modified = self.modified = True

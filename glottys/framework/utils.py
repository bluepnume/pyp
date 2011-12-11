from functools import wraps

def cacheprop(method):
  @wraps(method)
  def cachemethod(self):
    while True:
      try:
        return self.cache[method]
      except AttributeError:
        self.cache = {}
      except KeyError:
        self.cache[method] = method(self)
  return property(cachemethod)

def cachetuple(method):
  @wraps(method)
  def cachemethod(self):
    while True:
      try:
        return self.cache[method]
      except AttributeError:
        self.cache = {}
      except KeyError:
        self.cache[method] = tuple(method(self))
  return property(cachemethod)

def cacheset(method):
  @wraps(method)
  def cachemethod(self):
    while True:
      try:
        return self.cache[method]
      except AttributeError:
        self.cache = {}
      except KeyError:
        self.cache[method] = set(method(self))
  return property(cachemethod)

from __future__ import division
from math import hypot, acos, pi, sqrt, copysign
from operator import sub

from helpers import cacheprop
import draw

from pygraph.classes.graph import graph
from pygraph.algorithms.heuristics.euclidean import euclidean
from pygraph.algorithms.minmax import heuristic_search, shortest_path

from . import AdventureBase

class Nav(AdventureBase):
  
  @cacheprop
  def graph(self):
    g = graph()
    for path in self.paths:
      for index, node in enumerate(path):
        if not node in g.nodes():
          g.add_node(node)
          g.add_node_attribute(node, ('position', node))
        if index:
          g.add_edge((path[index-1], node)) 
    return g
  
  @cacheprop        
  def heuristic(self):
    heuristic = euclidean()
    heuristic.optimize(self.graph)
    return heuristic
    
  def findpath(self, nodeone, nodetwo):
    return heuristic_search(self.graph, nodeone, nodetwo, self.heuristic)[1:-1]
    
  @cacheprop
  def paths(self):
    return tuple(self.getpaths(self.route))
  
  def getpaths(self, route):
    path = []
    for node in route:
      while isinstance(node[0], tuple):
        for newpath in self.getpaths(node):
          yield newpath
        node = node[0]
      path.append(node)
    yield tuple(path)
  
  def shortestpath(self, node):
    return shortest_path(self.graph, node)
    
  @cacheprop
  def pairs(self):
    return tuple(Pair(*path[i:i+2]) for path in self.paths for i in xrange(len(path)-1))

class Pair(object):
  
  def __init__(self, start, end):
    self.start, self.end = sorted((start, end))
    
  def __repr__(self):
    return '%s(%s, %s)' % (self.__class__.__name__, self.start, self.end)
  
  def __iter__(self):
    return iter((self.start, self.end))
    
  @property
  def points(self):
    return self.start, self.end
    
  @cacheprop
  def vec(self):
    return map(sub, self.end, self.start)
   
  @cacheprop
  def length(self):
    return hypot(*self.vec)
    
  @cacheprop
  def gradient(self):
    x, y = self.vec
    if x:
      return (y / x)
    return 0
    
  @property
  def vertical(self):
    x, y = self.vec
    return not x
    
  @property
  def horizontal(self):
    x, y = self.vec
    return not y
    
  @cacheprop
  def inversegradient(self):
    if self.gradient:
      return (-1 / self.gradient)
    return 0
    
  @cacheprop
  def constant(self):
    x, y = self.start
    return y - self.gradient * x
    
  def inverseconstant(self, x, y):
    return y - self.inversegradient * x
    
  def draw(self):
    draw.line(self.start, self.end)

  def nearestpoint(self, coord):
    
    x, y = coord
    
    if self.vertical:
      x = self.start[0]
      
    elif self.horizontal:
      y = self.start[1]
    
    else:
      inverseconstant = self.inverseconstant(x, y)
      gradient, constant = self.gradient, self.constant
      gradientsquared = gradient ** 2
      x = gradient * (inverseconstant - constant)
      y = inverseconstant * gradientsquared + constant
      gradientsquared += 1
      x /= gradientsquared
      y /= gradientsquared
      
    result = x, y
    
    if result < self.start:
      result = self.start
    elif result > self.end:
      result = self.end
    
    return result

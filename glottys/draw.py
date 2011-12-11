#!/usr/bin/python

from pyglet.graphics import draw
from pyglet.gl       import GL_LINES
from pyglet.gl import *

glEnable(GL_LINE_SMOOTH);
glLineWidth(2)  

def line(start, end):
  glEnable(GL_LINE_SMOOTH);
  #glLineWidth(2)  
  draw(2, GL_LINES, ('v2i', map(int, start + end)))

def lines(*points, **kwargs):
  for i in xrange(int(not kwargs.get('join', True)), len(points)):
    line(points[i-1], points[i], antialias=kwargs.get('antialias', True))

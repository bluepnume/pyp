#!/usr/bin/python

from pyglet.graphics import Batch, OrderedGroup

from .framework import FrameWork
from .framework.children import RootProxy, game as adventure
from .framework.event import event

class AdventureBase(FrameWork):
  
  adventure = RootProxy()
  
  # Draw
  screen = Batch()
  overlay = Batch()
  bg = OrderedGroup(0)
  mg = OrderedGroup(1)
  fg = OrderedGroup(2)

from .adv   import *
from .scene import *

from .char  import *
from .convo import *
from .anim  import * 
from .nav   import *
from .hotspot import *

    
    

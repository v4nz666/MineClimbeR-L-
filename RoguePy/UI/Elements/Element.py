"""
Documentation, License etc.

@package RoguePy.UI
"""
from RoguePy.libtcod import libtcod
from RoguePy.UI import View

class Element(View):
  #TODO we should be calling View.__init__  :/
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.width = w
    self.height = h

    self.visible = True
    self.enabled = True

    self.console = libtcod.console_new(w, h)

    self.setDefaultColors()
    self.clearConsole()

    self._elements = []
    self._inputs = {}

    self.fgOpacity = 1
    self.bgOpacity = 1
    self.parent = None

    self.bgFlag = libtcod.BKGND_SET

  def setParent(self, parent):
    self.parent = parent
  
  def draw(self):
    pass
  
  def show(self):
    self.visible = True
    return self
  def hide(self):
    self.visible = False
    return self
  def toggleVisible(self):
    self.visible = not self.visible
    return self
  
  ###
  # Disabled elements will be rendered with a low-opacity black overlay
  ###
  def enable(self):
    self.enabled = True
  def disable(self):
    self.enabled = False
  def toggleEnabled(self):
    self.enabled = not self.enabled
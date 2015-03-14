'''
Documentation, License etc.

@package RoguePy.UI
'''
from RoguePy.libtcod import libtcod
from RoguePy.UI.Elements import Element

class Label(Element):
  
  def __init__(self, x, y, label=""):
    super(Label, self).__init__(x, y, len(label), 1)
    self._label = label
  
  def setLabel(self, label):
    self._label = label
    if self.width != len(self._label):
      self.width = len(self._label)
      # TODO This is not subject to constraint by the parent element, and can therefore spill outside its parent.
      # TODO investigate / fix segfault when calling libtcod.console_delete(self.console)
      self.console = libtcod.console_new(len(self._label), 1)
  def getLabel(self):
    return self._label
  
  def draw(self):
    libtcod.console_print(self.console, 0, 0, self._label)
      
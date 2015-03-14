'''
Documentation, License etc.

@package RoguePy.UI
'''
from RoguePy.libtcod import libtcod
from RoguePy.UI.Elements import Element


class Dict(Element):
  
  def setItems(self, items):
    self._items = items
    return self
  
  def addItem(self, item):
    self._items.update(item)
    return self
  
  def removeItem(self, itemKey):
    if itemKey in self._items:
      del self._items[itemKey]
    return self
  
  def draw(self):
    y = 0
    for key in self._items:
      val = self._items[key]
      libtcod.console_print(self.console, 0, y, key)
      val = str(val)
      libtcod.console_print(self.console, self.width - len(val), y, val)
      y = y + 1
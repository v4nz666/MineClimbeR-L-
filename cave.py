from Item.itemtypes import Anchor
from RoguePy.Map.Map import Map

class Cave(Map):
  def __init__(self, w, h):
    super(Cave, self).__init__(w, h)
    self.enemies = []

  def reset(self):
    self.enemies = []

  def hasAnchor(self, x, y):
    return Anchor in self.getCell(x, y).entities

  def addEnemy(self, enemy):
    self.enemies.append(enemy)
  def removeEnemy(self, enemy):
    if enemy in self.enemies:
      self.enemies.remove(enemy)
      self.getCell(enemy.x, enemy.y).removeEntity(enemy)
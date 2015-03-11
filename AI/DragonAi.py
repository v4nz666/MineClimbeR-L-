from random import random
from Item import Item
from AI.Ai import Ai
from RoguePy.libtcod import libtcod

class DragonAi(Ai):

  fireChance = 0.15

  def __init__(self, map, enemy):
    super(DragonAi, self).__init__(map, enemy)
    self.dragonFireDef = ['Dragon Fire', 'W', libtcod.flame, 0, 10, 100, 100]
    self.waitTimeout = 4
    self.waitLeft = 2
    
    self.fire = Item('Dragon Fire')
    self.fire.setChar('W')
    self.fire.setColor(libtcod.flame)

    self.firePath = []

  def clearFirePath(self):
    for (x, y) in self.firePath:
      cell = self.map.getCell(x,y)
      if self.fire in cell.entities:
        cell.removeEntity(self.fire)
    self.firePath = []

  def update(self):
    if len(self.firePath):
      self.clearFirePath()
    Ai.move(self)

  def doAttack(self):
    libtcod.line_init(self.enemy.x, self.enemy.y, self.player.x, self.player.y)
    (x, y) = libtcod.line_step()
    while not x is None:
      cell = self.map.getCell(x, y)

      # Only rock walls will stop the dragon fire. Transparent wood beams won't.
      if not(cell.passable() or cell.transparent()):
        return False

      for j in range(-1,2):
        for i in range(-1,2):
          if not j and not i:
            chance = 0.9
          else:
            chance = self.fireChance
          _x = x+i
          _y = y+j
          try:
            cell = self.map.getCell(_x, _y)
          except:
            continue
          rnd = random()
          # Critical miss on the main line of the fire. Fizzle out.
          if chance == 0.9 and rnd < 0.1:
            return
          elif rnd <= chance:
            if cell.terrain.burnTerrain:
              cell.setTerrain(cell.terrain.burnTerrain)
            if cell.passable() or cell.transparent():
              self.firePath.append((_x, _y))
              self.map.addEntity(self.fire, _x, _y)
      (x, y) = libtcod.line_step()

    self.enemy.attackActor(self.player)
    return True

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    if self.map.getCell(xTo, yTo).passable():
      return 1.0
    else:
      return 0



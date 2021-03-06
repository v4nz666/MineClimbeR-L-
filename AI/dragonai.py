from random import random
from Item.item import Item
from AI.ai import Ai
from RoguePy.libtcod import libtcod
from sounds import fireSound

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
    self.fire.collectible = False
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
    return Ai.move(self)


  def doAttack(self):
    self.attacking = False
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
    fireSound.play()
    return self.enemy.defAttack(self.player)

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    if self.map.getCell(xTo, yTo).passable():
      return 1.0
    else:
      return 0
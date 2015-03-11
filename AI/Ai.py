from random import randrange
from RoguePy.libtcod import libtcod

class Ai(object):
  def __init__(self, map, enemy):
    self.enemy = None
    self.map = map
    self.player = enemy.player
    self.enemy = enemy
    self.path = None

    self.waitTimeout = 0
    self.waitLeft = 0

  def doAttack(self):
    self.enemy.attackActor(self.player)
    return True

  def update(self):
    self.move()

  def move(self):
    if self.path:
      libtcod.path_delete(self.path)
    self.path = libtcod.path_new_using_function(self.map.width,self.map.height,self.computePath)
    oldX, oldY = self.enemy.x, self.enemy.y
    hasPath = libtcod.path_compute(self.path, oldX, oldY, self.player.x, self.player.y)
    pathSize = libtcod.path_size(self.path)
    if self.waitLeft > 0:
      self.waitLeft -= 1

    # In range, we can attack whether we have a path or not.
    if pathSize <= self.enemy.range:
      # Time to attack
      if self.waitLeft == 0:
        # If the attack succeeds, reset the wait timer
        if self.doAttack():
          self.waitLeft = self.waitTimeout
          return True
        # else, try repositioning
        else:
          return self.reposition()
      # Still waiting, jostle around a bit
      else:
        return self.reposition()

    if hasPath:
      if pathSize > 0:
        (newX, newY) = libtcod.path_get(self.path, 0)
        try:
          self.moveEnemy(newX, newY)
          return True
        except ValueError:
          pass

    return False
  def moveEnemy(self, newX, newY):
    oldX = self.enemy.x
    oldY = self.enemy.y
    self.map.getCell(oldX, oldY).removeEntity(self.enemy)
    self.map.addEntity(self.enemy, newX, newY)
    self.enemy.setCoords(newX, newY)

  def reposition(self):
    # Try 8 times to find a suitable spot around us, stay put if we fail
    for attempt in range(8):
      while True:
        x = randrange(-1,2)
        y = randrange(-1,2)
        if (x or y) and not (x < 0 or y < 0 or x >= self.map.width or y >= self.map.height):
          break
      x = self.enemy.x + x
      y = self.enemy.y + y
      cell = self.map.getCell(x, y)
      if cell.passable():
        self.moveEnemy(x, y)
        return

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    return 1.0

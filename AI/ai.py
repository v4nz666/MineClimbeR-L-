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

    self.attacking = False

  def doAttack(self):
    self.attacking = False
    return self.enemy.defAttack(self.player)


  def update(self):
    return self.move()

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
      # Our attack timer has elapsed
      if self.waitLeft == 0:
        # Reset the wait timer
        self.attacking = True
        self.waitLeft = self.waitTimeout
        return True
      # Not yet time to attack, returning False will trigger an idleUpdate()
      else:
        return False


    if hasPath:
      if pathSize > 0:
        (newX, newY) = libtcod.path_get(self.path, 0)
        try:
          self.moveEnemy(newX, newY)
          return True
        except ValueError:
          pass
    else:
      return False

    return False
  def moveEnemy(self, newX, newY):
    oldX = self.enemy.x
    oldY = self.enemy.y
    self.map.getCell(oldX, oldY).removeEntity(self.enemy)
    self.map.addEntity(self.enemy, newX, newY)
    self.enemy.setCoords(newX, newY)

  def reposition(self):

    newX = newY = -1

    # Try 8 times to find a suitable spot around us, stay put if we fail
    for attempt in range(8):
      while True:
        deltaX = randrange(-1,2)
        deltaY = randrange(-1,2)
        newX = self.enemy.x + deltaX
        newY = self.enemy.y + deltaY
        if (deltaX or deltaY) and not (newX < 0 or newY < 0 or newX >= self.map.width or newY >= self.map.height):
          break

      if self.computePath(self.enemy.x, self.enemy.y, newX, newY, 1):
        self.moveEnemy(newX, newY)
        return True
    return False

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    return 1.0

from RoguePy.libtcod import libtcod

class Ai(object):
  def __init__(self, map, enemy):
    self.enemy = None
    self.map = map
    self.player = enemy.player
    self.enemy = enemy
    self.path = None


  def move(self):
    if self.path:
      libtcod.path_delete(self.path)
    self.path = libtcod.path_new_using_function(self.map.width,self.map.height,self.computePath)
    oldX, oldY = self.enemy.x, self.enemy.y
    hasPath = libtcod.path_compute(self.path, oldX, oldY, self.player.x, self.player.y)
    pathSize = libtcod.path_size(self.path)
    if hasPath and pathSize > 0:
      (newX, newY) = libtcod.path_get(self.path, 0)
      if pathSize <= self.enemy.range:
        self.enemy.attackActor(self.player)
      else:
        try:
          self.map.getCell(oldX, oldY).removeEntity(self.enemy)
          self.map.addEntity(self.enemy, newX, newY)
          self.enemy.setCoords(newX, newY)
          return True
        except ValueError:
          pass
    else:
      # if not hasPath:
      #   print "No path", self.__class__, "HAS SIZE", pathSize
      #
      # else:
      #   print "No size", self.__class__
      pass

    return False

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    return 1.0

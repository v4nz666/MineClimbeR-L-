from math import sqrt
from RoguePy.Map.Entity import Entity

class Item(Entity):
  def __init__(self, name, material=None):
    super(Item, self).__init__(name)
    self.material = material

    # number of items to generate
    self.genCount = 0
    # Minimum depth to spawn at
    self.genMin = 0.0
    # Maximum depth to spawn at
    self.genMax = 1.0

    self.collectible = True
    self.maxInv = 2

    # The type of Enemy that we'll spawn, when first encountered
    # ...This should probably live in a Spawner derivative class.
    self.spawns = None

    self.collectCount = 1

  def distance(self, x, y):
    # return the linear distance to a point, from our point
    dx = x - self.x
    dy = y - self.y
    distance = sqrt(dx ** 2 + dy ** 2)
    return distance

  def collect(self, player):
    inInv = player.inventory.count(self)
    for i in range(self.collectCount):
      if inInv < self.maxInv:
        player.pickupItem(self)
      else:
        return False
    return True



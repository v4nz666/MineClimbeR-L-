from RoguePy.Map.Entity import Entity

class Item(Entity):
  def __init__(self, name):
    super(Item, self).__init__(name)

    # number of items to generate
    self.genCount = 0
    # Minimum depth to spawn at
    self.genMin = 0.0
    # Maximum depth to spawn at
    self.genMax = 1.0

    self.collectible = True
    self.maxInv = 2

    # The type of entity that we'll spawn, when first encountered
    # ...This should probably live in a Spawner derivative class.
    self.spawns = None

  def collect(self, player):
    inInv = player.inventory.count(self)
    if inInv < self.maxInv:
      player.pickupItem(self)
      return True
    return False


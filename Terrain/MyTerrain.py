from RoguePy.Map.Terrain import Terrain

class MyTerrain(Terrain):
  def __init__(self, see, walk, desc):
    Terrain.__init__(self, see, walk, desc)
    self.damage = 0
    self.hp = 2
    # The item we'll drop when destroyed
    self.itemDrop = None
    self.digTerrain = None

  def drops(self, item):
    self.itemDrop = item
    return self
  def digs(self, terrain):
    self.digTerrain = terrain
    return self
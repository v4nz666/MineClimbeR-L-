from RoguePy.Map.Terrain import Terrain

class MyTerrain(Terrain):
  def __init__(self, see, walk, desc):
    Terrain.__init__(self, see, walk, desc)
    self.damage = 0
    self.hp = 2
    # The item we'll drop when destroyed
    self.itemDrop = None
    self.digTerrain = None
    self.burnTerrain = None

  def burns(self, terrain):
    self.burnTerrain = terrain
    return self

  def drops(self, item):
    self.itemDrop = item
    return self
  def digs(self, terrain):
    self.digTerrain = terrain
    return self
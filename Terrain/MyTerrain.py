from RoguePy.Map.Terrain import Terrain

class MyTerrain(Terrain):
  def __init__(self, see, walk, desc):
    Terrain.__init__(self, see, walk, desc)
    self.damage = 0
    self.hp = 2
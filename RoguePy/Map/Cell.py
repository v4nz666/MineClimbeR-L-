import terrains


class Cell(object):
  def __init__(self, terrain = terrains.EMPTY):
    """
    Cell class. Represents one space on the Map

    :return: self
    """
    self.terrain = terrain
    self.entities = []


  def setTerrain(self, terrain):
    self.terrain = terrain

  def transparent(self):
    return self.terrain.see

  def passable(self):
    return self.terrain.walk

  def addEntity(self, entity, first=False):
    if first:
      self.entities.insert(0,entity)
    else:
      self.entities.append(entity)

  def removeEntity(self, entity):
    try:
      self.entities.remove(entity)
    except KeyError:
      pass
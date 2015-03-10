from Ai import Ai

class DragonAi(Ai):

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    if self.map.getCell(xTo, yTo).passable():
      return 1.0
    else:
      return 0



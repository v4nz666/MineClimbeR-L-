from ai import Ai

class SnakeAi(Ai):

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    if self.map.getCell(xTo, yTo).passable():
      try:
        if not self.map.getCell(xTo, yTo + 1).passable():
          return 1.0
      except:
        pass
    return 0



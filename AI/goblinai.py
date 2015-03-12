from ai import Ai

class GoblinAi(Ai):

  def computePath(self, xFrom, yFrom, xTo, yTo, data):
    cell = self.map.getCell(xTo, yTo)
    if cell.passable():
      try:
        if self.map.hasAnchor(xTo, yTo) or not self.map.getCell(xTo, yTo + 1).passable():
          return 1.0
      except:
        pass
    return 0

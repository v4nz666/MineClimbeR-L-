from Ai import Ai

class SpiderAi(Ai):

  def computePath(self, xFrom, yFrom, xTo, yTo, len):
    if self.map.getCell(xTo, yTo).passable():
      try:
        if  not self.map.getCell(xTo,     yTo - 1).passable() or\
            not self.map.getCell(xTo - 1, yTo).passable() or\
            not self.map.getCell(xTo + 1, yTo).passable() or\
            not self.map.getCell(xTo,     yTo + 1).passable():
          return 1.0
      except:
        pass
    return 0



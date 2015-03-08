from RoguePy.libtcod import libtcod
from Item import Item

class Actor(Item):
  def __init__(self, name):
    super(Actor,self).__init__(name)
    self.x = None
    self.y = None
    self.needFovUpdate = False


  def setCoords(self, x, y):
    self.x = x
    self.y = y

  def moveU(self):
    self.y -= 1
    self.needFovUpdate = True

  def moveD(self):
    self.y += 1
    self.needFovUpdate = True
  def moveL(self):
    self.x -= 1
    self.needFovUpdate = True
  def moveR(self):
    self.x += 1
    self.needFovUpdate = True
  def moveUL(self):
    self.x -= 1
    self.y -= 1
    self.needFovUpdate = True
  def moveUR(self):
    self.x += 1
    self.y -= 1
    self.needFovUpdate = True
  def moveDL(self):
    self.x -= 1
    self.y += 1
    self.needFovUpdate = True
  def moveDR(self):
    self.x += 1
    self.y += 1
    self.needFovUpdate = True

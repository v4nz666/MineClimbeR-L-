from Item import Item

class Actor(Item):
  def __init__(self, name):
    super(Actor,self).__init__(name)
    self.x = None
    self.y = None

  def setCoords(self, x, y):
    self.x = x
    self.y = y

  def moveU(self):
    self.y -= 1
  def moveD(self):
    self.y += 1
  def moveL(self):
    self.x -= 1
  def moveR(self):
    self.x += 1
  def moveUL(self):
    self.x -= 1
    self.y -= 1
  def moveUR(self):
    self.x += 1
    self.y -= 1
  def moveDL(self):
    self.x -= 1
    self.y += 1
  def moveDR(self):
    self.x += 1
    self.y += 1

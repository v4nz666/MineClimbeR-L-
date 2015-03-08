from Item import Item

class Ore(Item):
  def __init__(self, name):
    super(Ore, self).__init__(name)
    self.char = '*'

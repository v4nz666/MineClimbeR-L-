from Item.Actor import Actor
from Item.itemTypes import Anchor
from Item.itemTypes import Rope

class Player(Actor):


  def __init__(self, name="You"):
    super(Player, self).__init__(name, 100, 10, 10)

    self.startingAnchors = 50
    self.ropeCount = 8

    self.maxTorchStrength = 25
    self.torchStrength = self.maxTorchStrength

    self.needFovUpdate = True

    self.fell = 0
    self.falling = False
    self.fallDamage = 2
    self.maxFallHeight = 2

    self.attached = False

    self.inventory = [Anchor for i in range(self.startingAnchors)] + [Rope for i in range(self.ropeCount)]

  def anchorIn(self):
    hasAnchor = Anchor in self.map.getCell(self.x, self.y).entities
    if Anchor in self.inventory or hasAnchor:
      self.attached = True
      if not hasAnchor:
        self.inventory.remove(Anchor)
      self.falling = False
      self.fell = 0
      return True
    else:
      return False

  def detach(self):
    self.inventory += [Rope for i in range(self.ropeCount - self.inventory.count(Rope))]
    self.attached = False

  def land(self):
    if self.fell > self.maxFallHeight:
      delta = pow(self.fallDamage, self.fell - self.maxFallHeight)
      self.health -= delta
    self.falling = False
    self.fell = 0
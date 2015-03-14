from Item.actor import Actor
from Item.itemtypes import *

class Player(Actor):


  def __init__(self, name="You"):
    super(Player, self).__init__(name, 100, 10, 10)

    self.startingAnchors = 50
    self.ropeCount = 8

    self.maxTorchStrength = 25
    self.torchStrength = self.maxTorchStrength

    self.pickStrength = 0
    self.maxPickStrength = 0
    self.basePickStrength = 100

    self.needFovUpdate = True

    self.fell = 0
    self.falling = False
    self.fallDamage = 2
    self.maxFallHeight = 2

    self.attached = False
    self.inventory = [Anchor for i in range(self.startingAnchors)] + [Rope for i in range(self.ropeCount)]

  def collectPick(self, pick):
    self.maxPickStrength = int(pick.material.multiplier * self.basePickStrength)
    self.meleeMultiplier = pick.material.multiplier
    self.pickStrength = self.maxPickStrength

  def collectArrows(self, arrow, num):
    self.rangeMultiplier = arrow.material.multiplier
    self.inventory += [Arrow for i in range(num)]

  def damagePick(self):
    self.pickStrength = max(0, self.pickStrength - 1)
    return self.pickStrength > 0

  def anchorIn(self):
    if self.falling:
      return False

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
    delta = 0
    if self.fell > self.maxFallHeight:
      delta = pow(self.fallDamage, self.fell - self.maxFallHeight)
      self.health -= delta
    self.falling = False
    self.fell = 0
    return delta
from Item.Actor import Actor
from Item.itemTypes import Anchor
from Item.itemTypes import Rope

class Player(Actor):


  def __init__(self, name="You"):
    super(Player, self).__init__(name)

    self.startingAnchors = 50
    self.ropeCount = 8

    self.maxTorchStrength = 10
    self.torchStrength = self.maxTorchStrength

    self.needFovUpdate = True

    self.falling = False
    self.attached = False

    self.inventory = [Anchor for i in range(self.startingAnchors)] + [Rope for i in range(self.ropeCount)]

  def anchorIn(self):
    if Anchor in self.inventory:
      self.attached = True
      self.inventory.remove(Anchor)

      return True
    else:
      return False

  def detach(self):
    self.inventory += [Rope for i in range(self.ropeCount - self.inventory.count(Rope))]
    self.attached = False


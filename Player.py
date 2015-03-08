from Item.Actor import Actor
from Item.itemTypes import Anchor

class Player(Actor):


  def __init__(self, name="You"):
    super(Player, self).__init__(name)

    self.startingAnchors = 50
    self.ropeCount = 8
    self.ropeAttached = 0

    self.maxTorchStrength = 10
    self.torchStrength = self.maxTorchStrength

    self.needFovUpdate = True

    self.falling = False
    self.attached = False


    self.inventory = [Anchor for i in range(self.startingAnchors)]

  def anchorIn(self):
    if Anchor in self.inventory:
      self.attached = True
      self.ropeAttached = 1
      self.inventory.remove(Anchor)
      return True
    else:
      return False

  def detach(self):
    self.ropeAttached = 0
    self.attached = False


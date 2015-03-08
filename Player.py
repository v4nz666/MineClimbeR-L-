from Item.Actor import Actor

class Player(Actor):
  def __init__(self, name="You"):
    super(Player, self).__init__(name)

    self.maxTorchStrength = 10
    self.torchStrength = self.maxTorchStrength

    self.needFovUpdate = True

    self.falling = False



from Item.Actor import Actor

class Player(Actor):
  def __init__(self, name="You"):
    super(Player, self).__init__(name)
    self.calculateFov = False



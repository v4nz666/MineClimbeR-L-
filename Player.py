from RoguePy.Map import Entity

class Player(Entity):
  def __init__(self, name="You"):
    super(Player, self).__init__(name)
    self.calculateFov = False


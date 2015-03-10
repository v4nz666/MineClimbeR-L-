from Item.Actor import Actor

class Enemy(Actor):
  def __init__(self, player, name, char, color, maxHealth, attack, defend, dex):
    super(Enemy, self).__init__(name, maxHealth, attack, defend, dex)

    self.player = player

    self.char = char
    self.color = color
    self._ai = None
    self.maxPath = 10

  def setAi(self, ai):
    self._ai = ai

  def aiMove(self):
    self._ai.move()
    pass
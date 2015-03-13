from Item.actor import Actor

class Enemy(Actor):
  def __init__(self, player, name, char, color, maxHealth, attack, defend, dex):
    super(Enemy, self).__init__(name, maxHealth, attack, defend, dex)

    self.player = player

    self.char = char
    self.color = color
    self._ai = None
    self.maxPath = 10
    self.range = 1

  def setAi(self, ai):
    self._ai = ai

  def aiUpdate(self):
    if self._ai:
      self._ai.update()
      return True
    return False

  def aiAttack(self):
    return self._ai.doAttack()

  def attacking(self):
    return self._ai.attacking
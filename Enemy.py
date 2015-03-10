from Item.Actor import Actor

class Enemy(Actor):
  def __init__(self, name, char, color, maxHealth, attack, defend, dex):
    super(Enemy, self).__init__(name, maxHealth, attack, defend, dex)
    self.char = char
    self.color = color

  def aiMove(self):
    print "Enemy moving"
    pass
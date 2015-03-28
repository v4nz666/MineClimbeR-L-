from random import randrange
from RoguePy.libtcod import libtcod
from item import Item




class Actor(Item):
  def __init__(self, name, maxHealth, attack=0 , defend=0, dex=0):
    super(Actor,self).__init__(name)

    self.maxHealth = maxHealth
    self.health = maxHealth
    self.attack = attack
    self.defend = defend
    self.dex = dex

    self.meleeMultiplier = 1.0
    self.rangeMultiplier = 1.0

    self.map = None
    self.x = None
    self.y = None
    self.collectible = False
    self.needFovUpdate = False

    self.inventory = []
    self.drops = None
    self.dropChance = 1.0

  def defAttack(self, target):
    if target.dead():
      return
    atk = int(self.attack * self.meleeMultiplier)
    damage = randrange(0, atk + 1)
    defend = randrange(0, target.defend + 1)

    delta = damage - defend
    if delta > 0:
      target.health -= delta
      return delta
    else:
      return 0
  # Pits our ranged attack against an enemy's dex stat
  def dexAttack(self, target):
    if target.dead():
      return
    atk = int(self.attack * self.rangeMultiplier)
    damage = randrange(0, atk + 1)
    defend = randrange(0, target.dex + 1)

    delta = damage - defend
    if delta > 0:
      target.health -= delta
      return delta
    else:
      return 0
  def pickupItem(self, item):
    self.inventory.append(item)
  def dropItem(self, item):
    if not item in self.inventory:
      return False
    else:
      self.inventory.remove(item)
      return True

  def dead(self):
    return self.health <= 0

  def setCoords(self, x, y):
    self.x = x
    self.y = y

  def setMap(self, map):
    self.map = map

  def moveU(self):
    self.y -= 1
    self.needFovUpdate = True
  def moveD(self):
    self.y += 1
    self.needFovUpdate = True
  def moveL(self):
    self.x -= 1
    self.needFovUpdate = True
  def moveR(self):
    self.x += 1
    self.needFovUpdate = True
  def moveUL(self):
    self.x -= 1
    self.y -= 1
    self.needFovUpdate = True
  def moveUR(self):
    self.x += 1
    self.y -= 1
    self.needFovUpdate = True
  def moveDL(self):
    self.x -= 1
    self.y += 1
    self.needFovUpdate = True
  def moveDR(self):
    self.x += 1
    self.y += 1
    self.needFovUpdate = True

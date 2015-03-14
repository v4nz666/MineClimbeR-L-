from ore import Ore
from Item.item import Item
from AI import *
#from enemies import *
from RoguePy.libtcod import libtcod
from pygame import mixer

waterSound = mixer.Sound('./sounds/water.wav')

Tin = Ore('Tin')
Tin.setColor(libtcod.Color(211, 212, 213))
Tin.genCount = 55
Tin.genMin = 0.025
Tin.genMax = 0.5
Tin.multiplier = 0.75

Copper = Ore('Copper')
Copper.setColor(libtcod.Color(184, 115, 51))
Copper.genCount = 50
Copper.genMin = 0.05
Copper.genMax = 0.5
Copper.multiplier = 1.0

Iron = Ore('Iron')
Iron.setColor(libtcod.Color(102, 102, 102))
Iron.genCount = 45
Iron.genMin = 0.4
Iron.genMax = 1.0
Iron.multiplier = 1.5

Coal = Ore('Coal')
Coal.setColor(libtcod.black)
Coal.genCount = 125
Coal.genMin = 0.05
Coal.genMax = 0.95

Diamond = Ore('Diamond')
Diamond.setColor(libtcod.lightest_cyan)
Diamond.setChar('+')
Diamond.genCount = 10
Diamond.genMin = 0.75
Diamond.genMax = 1.0
Diamond.multiplier = 10

# Alloys - no spawning
Bronze = Ore('Bronze')
Bronze.setColor(libtcod.Color(205, 127, 50))
Bronze.multiplier = 1.25

Steel = Ore('Steel')
Steel.setColor(libtcod.Color(192, 192, 192))
Steel.multiplier = 1.75

Anchor = Item('Anchor')
Anchor.setChar('"')
Anchor.setColor(libtcod.silver)
Anchor.collectible = False
Anchor.maxInv = 200
Anchor.collectCount = 50

Rope = Item('Rope')
Rope.setChar('%')
Rope.setColor(libtcod.crimson)
Rope.collectible = False
Rope.collectCount = 4
Rope.maxInv = 24

String = Item('String')
String.setChar('%')
String.setColor(libtcod.light_crimson)

Silk = Item('Silk')
Silk.setChar('%')
Silk.setColor(libtcod.lightest_crimson)

Arrow = Item('Arrow')
Arrow.setChar('.')
Arrow.setColor(libtcod.lightest_grey)
Arrow.collectible = False

Venom = Item('Venom')
Venom.setChar('!')
Venom.setColor(libtcod.light_green)
Venom.multiplier = 2

Wood = Item('Wood')
Wood.setChar('-')
Wood.setColor(libtcod.dark_orange)
Wood.maxInv = 4

Water = Item('Water')
Water.setChar('~')
Water.setColor(libtcod.darker_blue)
Water.genCount = 75
Water.genMin = 0.05
Water.genMax = 0.95

Bow = Item('Bow')

DragonScale = Item('Dragon Scale')
DragonScale.setChar(libtcod.CHAR_RADIO_SET)
DragonScale.setColor(libtcod.chartreuse)

Torch = Item('Torch')
Torch.maxInv = 1

########
# Tools
TinPick = Item('Pick', Tin)
CopperPick = Item('Pick', Copper)
BronzePick = Item('Pick', Bronze)
IronPick = Item('Pick', Iron)
SteelPick = Item('Pick', Steel)
TinArrow = Item('Arrow', Tin)
CopperArrow = Item('Arrow', Copper)
BronzeArrow = Item('Arrow', Bronze)
IronArrow = Item('Arrow', Iron)
SteelArrow = Item('Arrow', Steel)
DiamondArrow = Item('Arrow', Diamond)
PoisonArrow = Item('!Arrow!', Venom)
########

#########
# Enemies
BatDef = {
  'args': ['Bat', '^', libtcod.darkest_grey, 1, 3, 3, 10],
  'ai': BatAi,
  'maxPath': 15
}
SpiderDef = {
  'args': ['Spider', 'x', libtcod.darker_sepia, 3, 4, 3, 8],
  'ai': SpiderAi,
  'maxPath': 10,
  'drops': Silk,
  'dropChance': 0.5
}
SnakeDef = {
  'args': ['Snake', 's', libtcod.dark_amber, 5, 5, 3, 5],
  'ai': SnakeAi,
  'maxPath': 5,
  'drops': Venom,
  'dropChance': 0.5
}
GoblinDef = {
  'args': ['Goblin', 'g', libtcod.han, 10, 8, 6, 5],
  'ai': GoblinAi,
  'maxPath': 15,
  'drops': String,
  'dropChance': 0.25
}
TrollDef = {
  'args': ['Troll', 'T', libtcod.yellow, 15, 12, 12, 2],
  'ai': TrollAi,
  'maxPath': 20,
  'drops': Diamond,
  'dropChance': 0.05
}
DragonDef = {
  'args': ['Dragon', 'D', libtcod.darker_chartreuse, 75, 30, 25, 10],
  'ai': DragonAi,
  'maxPath': 50,
  'range': 4,
  'drops': DragonScale,
  'dropChance': 1.0
}

BatSpawner = Item('')
BatSpawner.genCount = 32
BatSpawner.genMin = 0.05
BatSpawner.genMax = 0.75
BatSpawner.collectible = False
BatSpawner.spawns = BatDef

SpiderSpawner = Item('')
SpiderSpawner.genCount = 64
SpiderSpawner.genMin = 0.0
SpiderSpawner.genMax = 0.60
SpiderSpawner.collectible = False
SpiderSpawner.spawns = SpiderDef

SnakeSpawner = Item('')
SnakeSpawner.genCount = 32
SnakeSpawner.genMin = 0.0
SnakeSpawner.genMax = 0.25
SnakeSpawner.collectible = False
SnakeSpawner.spawns = SnakeDef

GoblinSpawner = Item('')
GoblinSpawner.genCount = 24
GoblinSpawner.genMin = 0.5
GoblinSpawner.genMax = 0.8
GoblinSpawner.collectible = False
GoblinSpawner.spawns = GoblinDef

TrollSpawner = Item('')
TrollSpawner.genCount = 16
TrollSpawner.genMin = 0.65
TrollSpawner.genMax = 0.9
TrollSpawner.collectible = False
TrollSpawner.spawns = TrollDef

DragonSpawner = Item('')
DragonSpawner.genCount = 1
DragonSpawner.genMin = 0.95
DragonSpawner.genMax = 1.0
DragonSpawner.collectible = False
DragonSpawner.spawns = DragonDef

########
# overridden collect methods
def collectWater(player):
  player.health = min(player.maxHealth, player.health + 25)
  waterSound.play()
  return True
Water.collect = collectWater

def collectTorch(player):
  player.torchStrength = player.maxTorchStrength
  player.needFovUpdate = True
  return True
Torch.collect = collectTorch

def collectRope(player):
  Item.collect(Rope, player)
  player.ropeCount += Rope.collectCount
Rope.collect = collectRope

# Arrows
arrowCount = 20
def collectTinArrow(player):
  player.collectArrows(TinArrow, arrowCount)
  return True
TinArrow.collect = collectTinArrow
def collectCopperArrow(player):
  player.collectArrows(CopperArrow, arrowCount)
  return True
CopperArrow.collect = collectCopperArrow
def collectBronzeArrow(player):
  player.collectArrows(BronzeArrow, arrowCount)
  return True
BronzeArrow.collect = collectBronzeArrow
def collectIronArrow(player):
  player.collectArrows(IronArrow, arrowCount)
  return True
IronArrow.collect = collectIronArrow
def collectSteelArrow(player):
  player.collectArrows(SteelArrow, arrowCount)
  return True
SteelArrow.collect = collectSteelArrow
def collectPoisonArrow(player):
  player.collectArrows(PoisonArrow, 0)
  return True
PoisonArrow.collect = collectPoisonArrow
def collectDiamondArrow(player):
  player.collectArrows(DiamondArrow, arrowCount)
  return True
DiamondArrow.collect = collectDiamondArrow

# Picks
def collectTinPick(player):
  player.collectPick(TinPick)
  return True
TinPick.collect = collectTinPick
def collectCopperPick(player):
  player.collectPick(CopperPick)
  return True
CopperPick.collect = collectCopperPick
def collectBronzePick(player):
  player.collectPick(BronzePick)
  return True
BronzePick.collect = collectBronzePick
def collectIronPick(player):
  player.collectPick(IronPick)
  return True
IronPick.collect = collectIronPick
def collectSteelPick(player):
  player.collectPick(SteelPick)
  return True
SteelPick.collect = collectSteelPick

########
# Craftables/recipes
recipes = [
  { 'item': Torch,  'recipe': [Coal, Wood], 'fn': Torch.collect },

  { 'item': Anchor,  'recipe': [Tin], 'fn': Anchor.collect },
  { 'item': Anchor,  'recipe': [Copper], 'fn': Anchor.collect },
  { 'item': Anchor,  'recipe': [Bronze], 'fn': Anchor.collect },
  { 'item': Anchor,  'recipe': [Iron], 'fn': Anchor.collect },
  { 'item': Anchor,  'recipe': [Steel], 'fn': Anchor.collect },

  { 'item': Bronze, 'recipe': [Copper, Tin], 'fn': Bronze.collect },
  { 'item': Steel, 'recipe': [Iron, Coal], 'fn': Steel.collect },

  { 'item': TinPick, 'recipe': [Tin, Wood], 'fn': TinPick.collect },
  { 'item': CopperPick, 'recipe': [Copper, Wood], 'fn': CopperPick.collect },
  { 'item': BronzePick, 'recipe': [Bronze, Wood], 'fn': BronzePick.collect },
  { 'item': IronPick, 'recipe': [Iron, Wood], 'fn': IronPick.collect },
  { 'item': SteelPick, 'recipe': [Steel, Wood], 'fn': Steel.collect },

  { 'item': Rope, 'recipe': [String, String], 'fn': Rope.collect},
  { 'item': String, 'recipe': [Silk, Silk], 'fn': String.collect },
  { 'item': Bow, 'recipe': [String, Wood], 'fn': Bow.collect },

  { 'item': TinArrow, 'recipe': [Tin, Wood], 'fn': TinArrow.collect, 'dontDrop': [Arrow] },
  { 'item': CopperArrow, 'recipe': [Copper, Wood], 'fn': CopperArrow.collect, 'dontDrop': [Arrow] },
  { 'item': BronzeArrow, 'recipe': [Bronze, Wood], 'fn': BronzeArrow.collect, 'dontDrop': [Arrow] },
  { 'item': IronArrow, 'recipe': [Iron, Wood], 'fn': IronArrow.collect, 'dontDrop': [Arrow] },
  { 'item': SteelArrow, 'recipe': [Steel, Wood], 'fn': SteelArrow.collect, 'dontDrop': [Arrow] },
  { 'item': PoisonArrow, 'recipe': [Arrow, Venom], 'fn': PoisonArrow.collect, 'dontDrop': [Arrow] },
  { 'item': DiamondArrow, 'recipe': [Diamond, Wood], 'fn': DiamondArrow.collect, 'dontDrop': [Arrow] }
]



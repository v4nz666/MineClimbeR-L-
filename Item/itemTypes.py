from Ore import Ore
from Item import Item
from AI import *
#from enemies import *
from RoguePy.libtcod import libtcod

Tin = Ore('Tin')
Tin.setColor(libtcod.Color(211, 212, 213))
Tin.genCount = 15
Tin.genMin = 0.025
Tin.genMax = 0.3
Tin.multiplier = 0.75

Copper = Ore('Copper')
Copper.setColor(libtcod.Color(184, 115, 51))
Copper.genCount = 20
Copper.genMin = 0.2
Copper.genMax = 0.5
Copper.multiplier = 1.0

Iron = Ore('Iron')
Iron.setColor(libtcod.Color(102, 102, 102))
Iron.genCount = 25
Iron.genMin = 0.4
Iron.genMax = 1.0
Iron.multiplier = 1.75

Coal = Ore('Coal')
Coal.setColor(libtcod.darker_grey)
Coal.genCount = 50
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
Steel.multiplier = 2.5

Anchor = Item('Climbing anchor')
Anchor.setChar('"')
Anchor.setColor(libtcod.silver)
Anchor.collectible = False

Rope = Item('Rope')
Rope.setChar('%')
Rope.setColor(libtcod.crimson)
Rope.collectible = False

String = Item('String')
String.setChar('%')
String.setColor(libtcod.light_crimson)

Thread = Item('Thread')
Thread.setChar('%')
Thread.setColor(libtcod.lighter_crimson)

Silk = Item('Spider Silk')
Silk.setChar('%')
Silk.setColor(libtcod.lightest_crimson)

Water = Item('Water')
Water.setChar('~')
Water.setColor(libtcod.darker_blue)
Water.genCount = 50
Water.genMin = 0.05
Water.genMax = 0.95

def collectWater(player):
  player.health = min(player.maxHealth, player.health + 25)
  return True
Water.collect = collectWater

Arrow = Item('Arrow')
Arrow.setChar('/')
Arrow.setColor(libtcod.lightest_grey)

Venom = Item('Venom')
Venom.setChar('!')
Venom.setColor(libtcod.light_green)

Wood = Item('Wood')
Wood.setChar('-')
Wood.setColor(libtcod.dark_orange)
Wood.maxInv = 4

########
# Tools
TinPick = Item('Tin Pick')
TinPick.material = Tin

CopperPick = Item('Copper Pick')
CopperPick.material = Copper

BronzePick = Item('Bronze Pick')
BronzePick.material = Bronze

IronPick = Item('Iron Pick')
IronPick.material = Iron

SteelPick = Item('Steel Pick')
SteelPick.material = Steel

DiamondPick = Item('Diamond Pick')
DiamondPick.material = Diamond
########





#########
# Enemies
BatDef = {
  'args': ['Bat', '^', libtcod.darkest_grey, 1, 3, 3, 10],
  'ai': BatAi,
  'maxPath': 15,
}
SpiderDef = {
  'args': ['Spider', 'x', libtcod.darker_sepia, 3, 4, 3, 8],
  'ai': SpiderAi,
  'maxPath': 10,
}
SnakeDef = {
  'args': ['Snake', 's', libtcod.dark_amber, 5, 5, 3, 5],
  'ai': SnakeAi,
  'maxPath': 5,
}
GoblinDef = {
  'args': ['Goblin', 'g', libtcod.han, 10, 8, 6, 5],
  'ai': GoblinAi,
  'maxPath': 15,
}
TrollDef = {
  'args': ['Troll', 'T', libtcod.yellow, 15, 12, 12, 2],
  'ai': TrollAi,
  'maxPath': 20,
}
DragonDef = {
  'args': ['Dragon', 'D', libtcod.dark_crimson, 50, 20, 25, 10],
  'ai': DragonAi,
  'maxPath': 50,
  'range': 5
}

BatSpawner = Item('')
# BatSpawner.genCount = 30
# BatSpawner.genMin = 0.05
# BatSpawner.genMax = 0.75
BatSpawner.genCount = 30
BatSpawner.genMin = 0.05
BatSpawner.genMax = 0.75
BatSpawner.collectible = False
BatSpawner.spawns = BatDef

SpiderSpawner = Item('')
# SpiderSpawner.genCount = 15
# SpiderSpawner.genMin = 0.0
# SpiderSpawner.genMax = 0.20
SpiderSpawner.genCount = 15
SpiderSpawner.genMin = 0.0
SpiderSpawner.genMax = 0.60
SpiderSpawner.collectible = False
SpiderSpawner.spawns = SpiderDef

SnakeSpawner = Item('')
# SnakeSpawner.genCount = 5
# SnakeSpawner.genMin = 0.0
# SnakeSpawner.genMax = 0.2
SnakeSpawner.genCount = 5
SnakeSpawner.genMin = 0.0
SnakeSpawner.genMax = 0.25
SnakeSpawner.collectible = False
SnakeSpawner.spawns = SnakeDef

GoblinSpawner = Item('')
# GoblinSpawner.genCount = 15
# GoblinSpawner.genMin = 0
# GoblinSpawner.genMax = 0.2
GoblinSpawner.genCount = 15
GoblinSpawner.genMin = 0.5
GoblinSpawner.genMax = 0.8
GoblinSpawner.collectible = False
GoblinSpawner.spawns = GoblinDef

TrollSpawner = Item('')
# TrollSpawner.genCount = 10
# TrollSpawner.genMin = 0
# TrollSpawner.genMax = 0.2
TrollSpawner.genCount = 10
TrollSpawner.genMin = 0.65
TrollSpawner.genMax = 0.9
TrollSpawner.collectible = False
TrollSpawner.spawns = TrollDef

DragonSpawner = Item('')
DragonSpawner.genCount = 1
DragonSpawner.genMin = 0
DragonSpawner.genMax = 0.05
# DragonSpawner.genCount = 1
# DragonSpawner.genMin = 0.95
# DragonSpawner.genMax = 1.0
DragonSpawner.collectible = False
DragonSpawner.spawns = DragonDef

#TODO Remove
BatSpawner.setChar('^')
BatSpawner.setColor(libtcod.white)
SpiderSpawner.setChar('x')
SpiderSpawner.setColor(libtcod.white)
SnakeSpawner.setChar('s')
SnakeSpawner.setColor(libtcod.white)
GoblinSpawner.setChar('g')
GoblinSpawner.setColor(libtcod.white)
TrollSpawner.setChar('T')
TrollSpawner.setColor(libtcod.white)
DragonSpawner.setChar('D')
DragonSpawner.setColor(libtcod.white)
# End TODO
from ore import Ore
from Item.item import Item
from AI import *
#from enemies import *
from RoguePy.libtcod import libtcod

Tin = Ore('Tin')
Tin.setColor(libtcod.Color(211, 212, 213))
Tin.genCount = 55
Tin.genMin = 0.025
Tin.genMax = 0.5
Tin.multiplier = 0.75

Copper = Ore('Copper')
Copper.setColor(libtcod.Color(184, 115, 51))
Copper.genCount = 40
Copper.genMin = 0.2
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

Wood = Item('Wood')
Wood.setChar('-')
Wood.setColor(libtcod.dark_orange)
Wood.maxInv = 4

Water = Item('Water')
Water.setChar('~')
Water.setColor(libtcod.darker_blue)
Water.genCount = 50
Water.genMin = 0.05
Water.genMax = 0.95

Bow = Item('Bow')

DragonScale = Item('Dragon Scale')
DragonScale.setChar(libtcod.CHAR_RADIO_SET)
DragonScale.setColor(libtcod.chartreuse)


def collectWater(player):
  player.health = min(player.maxHealth, player.health + 25)
  return True
Water.collect = collectWater
########
# Tools
TinPick = Item('Pick', Tin)
CopperPick = Item('Pick', Copper)
BronzePick = Item('Pick', Bronze)
IronPick = Item('Pick', Iron)
SteelPick = Item('Pick', Steel)
TinArrow = Item('Arrows', Tin)
CopperArrow = Item('Arrows', Copper)
BronzeArrow = Item('Arrows', Bronze)
IronArrow = Item('Arrows', Iron)
SteelArrow = Item('Arrows', Steel)
DiamondArrow = Item('Arrows', Diamond)
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
  'drops': Arrow,
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
  'args': ['Dragon', 'D', libtcod.dark_chartreuse, 50, 20, 25, 10],
  'ai': DragonAi,
  'maxPath': 50,
  'range': 5,
  'drops': DragonScale,
  'dropChance': 1.0
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
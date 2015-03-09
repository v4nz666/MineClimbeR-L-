from Ore import Ore
from Item import Item
from RoguePy.libtcod import libtcod

Tin = Ore('Tin')
Tin.setColor(libtcod.Color(211, 212, 213))
Tin.genCount = 15
Tin.genMin = 0.025
Tin.genMax = 0.3

Copper = Ore('Copper')
Copper.setColor(libtcod.Color(184, 115, 51))
Copper.genCount = 20
Copper.genMin = 0.2
Copper.genMax = 0.5

Iron = Ore('Iron')
Iron.setColor(libtcod.Color(102, 102, 102))
Iron.genCount = 25
Iron.genMin = 0.4
Iron.genMax = 1.0

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

# Alloys - no spawning
Bronze = Ore('Bronze')
Bronze.setColor(libtcod.Color(205, 127, 50))

Steel = Ore('Steel')
Steel.setColor(libtcod.Color(192, 192, 192))

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

Arrow = Item('Arrow')
Arrow.setChar('/')
Arrow.setColor(libtcod.lightest_grey)

Venom = Item('Venom')
Venom.setChar('!')
Venom.setColor(libtcod.light_green)


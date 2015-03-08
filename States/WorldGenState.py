from random import randrange

from Terrain import terrains
from Item import itemTypes
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod
from RoguePy.Map.Map import Map
from RoguePy.State.GameState import GameState


class WorldGenState(GameState):
  def __init__(self, name, manager, ui):
    super(WorldGenState, self).__init__(name, manager, ui)
    self.map = None
    self.caveW = self.view.width * 4 / 5
    self.caveH = self.view.height * 10

    self.map = Map(self.caveW, self.caveH)

    self.caveStartY = 5
    self.firstFrame = True

    self.mapElement = self.view.addElement(Elements.Map(0, 0, self.caveW, self.view.height, self.map))
    self.view.addElement(Elements.Label(self.caveW + 1, 2, "Up/Dn - Scroll"))
    self.view.addElement(Elements.Label(self.caveW + 1, 3, "R - Regenerate Mine"))
    self.view.addElement(Elements.Label(self.caveW + 1, 4, "P - Play this Mine"))

    self.minOffset = self.mapElement.height / 2
    self.maxOffset = self.caveH - self.minOffset
    self.offset = self.minOffset

    self._setupInputs()


  def tick(self):
    self.mapElement.center(0, self.offset)


  def initCave(self):
    self.offset = self.minOffset

    self._blank()
    self._caGenerate()
    self._placeOres()

  def _blank(self):
    for y in range(self.caveH):
      for x in range(self.caveW):
        cell = self.map.getCell(x, y)

        if y < self.caveStartY:
          cell.setTerrain(terrains.openAir)
        elif y == self.caveStartY:
          if randrange(100) < 50:
            cell.setTerrain(terrains.openAir)
          else:
            cell.setTerrain(terrains.caveWall)
        else:
          cell.setTerrain(terrains.caveWall)

  def _caGenerate(self):
    caDigDensity = 0.4
    caNeighboursSpawn = 6
    caNeighboursStarve = 3
    caIterations = 5

    digCount = self.caveW * self.caveH * caDigDensity

    while digCount > 0:
      x = randrange(0, self.caveW - 1)
      y = randrange(0, self.caveH - 1)
      if y < self.caveStartY + 3:
        continue
      c = self.map.getCell(x,y)
      if not c.passable():
        digCount -= 1
        c.setTerrain(terrains.openMine)

    for i in range(caIterations):
      neighbours = [[None for _y in range(self.caveH)] for _x in range(self.caveW)]
      for y in range(self.caveH) :
        for x in range(self.caveW) :
          neighbours[x][y] = self.countWallNeighbours(x,y)

      for y in range(self.caveH) :
        for x in range(self.caveW) :
          if y <= self.caveStartY:
            continue
          c = self.map.getCell(x, y)

          n = neighbours[x][y]
          if c.passable() :
            if n >= caNeighboursSpawn:
              c.setTerrain(terrains.caveWall)
          else :
            if n <= caNeighboursStarve:
              c.setTerrain(terrains.openMine)

  def _placeOres(self):
    ores = [
      itemTypes.Coal,
      itemTypes.Tin,
      itemTypes.Copper,
      itemTypes.Iron,
      itemTypes.Diamond
    ]

    for ore in ores:
      placed = 0
      while placed < ore.genCount:
        genMin = int(self.caveH * ore.genMin)
        genMax = int(self.caveH * ore.genMax)
        x = randrange(self.caveW - 1)
        y = randrange(genMin, genMax)
        cell = self.map.getCell(x, y)
        if len(cell.entities) == 0 and not cell.passable():
          self.map.addEntity(ore, x, y)
          placed += 1

  def countWallNeighbours(self, x, y) :
    n = 0
    for _x in range ( -1, 2 ):
      for _y in range ( -1, 2 ):
        if not _x and not _y:
          continue
        try:
          c = self.map.getCell(x + _x, y + _y)
          if not c.passable() :
            n += 1
        except IndexError:
          pass
    return n


  def _setupInputs(self):
    self.inputsSet = True
    self.view.setInputs({
      'menuUp': {
        'key': libtcod.KEY_UP,
        'ch': None,
        'fn': self.scrollUp
      },
      'menuDn': {
        'key': libtcod.KEY_DOWN,
        'ch': None,
        'fn': self.scrollDown
      },
      'regenerate': {
        'key': None,
        'ch': 'R',
        'fn': self.initCave
      },
      'proceed': {
        'key': None,
        'ch': 'P',
        'fn': self.proceed
      },
      })

  def scrollUp(self):
    if self.offset > self.minOffset:
      self.offset -= 1
    pass
  def scrollDown(self):
    if self.offset < self.maxOffset:
      self.offset += 1

  def proceed(self):
    playState = self._manager.getState('Play')
    playState.setCave(self.map)
    self._manager.setNextState('Play')
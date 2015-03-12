from random import randrange

from Terrain import terrains
from Item import itemtypes
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod
from cave import Cave
from RoguePy.State.GameState import GameState


class WorldGenState(GameState):
  def __init__(self, name, manager, ui):
    super(WorldGenState, self).__init__(name, manager, ui)
    self.cave = None
    self.caveW = self.view.width# * 4 / 5
    self.caveH = self.view.height * 10

    self.cave = Cave(self.caveW, self.caveH)

    self.caveStartY = 5

    self.mapElement = self.view.addElement(Elements.Map(0, 0, self.caveW, self.view.height, self.cave))
    self.view.addElement(Elements.Label(self.caveW + 1, 2, "Up/Dn - Scroll"))
    self.view.addElement(Elements.Label(self.caveW + 1, 3, "R - Regenerate Mine"))
    self.view.addElement(Elements.Label(self.caveW + 1, 4, "P - Play this Mine"))
    self.view.addElement(Elements.Label(self.caveW + 1, 5, "ESC - Back to Menu"))


    self.minOffset = self.mapElement.height / 2
    self.maxOffset = self.caveH - self.minOffset
    self.offset = self.minOffset

    self._setupInputs()


  def tick(self):
    self.mapElement.center(0, self.offset)


  def initCave(self):

    # Preview mine from top
    self.offset = self.minOffset
    # Preview mine from bottom
    # self.offset = self.maxOffset

    self.cave.reset()
    self._blank()
    self._digDragonsDen()
    self._caGenerate()
    self._genLava()
    self._genWooden()
    self._genEntrance()
    self._genEntities()

  def _blank(self):
    for y in range(self.caveH):
      for x in range(self.caveW):
        cell = self.cave.getCell(x, y)
        cell.entities = []
        if y < self.caveStartY:
          cell.setTerrain(terrains.openAir)
        elif y == self.caveStartY:
          if randrange(100) < 75:
            cell.setTerrain(terrains.openAir)
          else:
            cell.setTerrain(terrains.caveWall)
        else:
          cell.setTerrain(terrains.caveWall)


  def _digDragonsDen(self):
    for y in range(self.caveH - 10, self.caveH - 20, -1):
      for x in range(5, self.caveW - 10):
        self.cave.getCell(x, y).setTerrain(terrains.openMine)

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
      c = self.cave.getCell(x,y)
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
          c = self.cave.getCell(x, y)

          n = neighbours[x][y]
          if c.passable() :
            if n >= caNeighboursSpawn:
              c.setTerrain(terrains.caveWall)
          else :
            if n <= caNeighboursStarve:
              c.setTerrain(terrains.openMine)

  def _genWooden(self):
    structureCount = 25
    while structureCount:
      x = randrange(1, self.caveW - 1)
      y = randrange(6, self.caveH - 25)

      if self._suitableSite(x, y):
        self._placeWood(x, y, terrains.caveWoodPost, terrains.caveWoodBeam)
        structureCount -= 1
  
  def _genEntrance(self):
    y = self.caveStartY
    while True:
      x = randrange(3, self.caveW - 3)
      if self._suitableSite(x, y):
        self._placeWood(x, y, terrains.openWoodPost, terrains.openWoodBeam)
        break
    y += 1
    while not self.cave.getCell(x, y).passable():
      self.cave.getCell(x, y).terrain = terrains.openMine
      y += 1

  def _suitableSite(self, x, y):
    if (self.cave.getCell(x-1, y+1).passable() or self.cave.getCell(x, y+1).passable() or self.cave.getCell(x+1, y+1).passable()) or\
      not (self.cave.getCell(x-1, y).passable() and self.cave.getCell(x, y).passable() and self.cave.getCell(x+1, y).passable()) or\
      not (self.cave.getCell(x-1, y-1).passable() and self.cave.getCell(x, y-1).passable() and self.cave.getCell(x+1, y-1).passable()) or\
      not (self.cave.getCell(x-1, y-2).passable() and self.cave.getCell(x, y-2).passable() and self.cave.getCell(x+1, y-2).passable()):
        return False
    else:
      return True


  def _placeWood(self, x, y, post, beam):
    self.cave.getCell(x-1,y).terrain = post
    self.cave.getCell(x+1,y).terrain = post
    self.cave.getCell(x-1,y-1).terrain = post
    self.cave.getCell(x+1,y-1).terrain = post
    self.cave.getCell(x-1,y-2).terrain = beam
    self.cave.getCell(x,y-2).terrain = beam
    self.cave.getCell(x+1,y-2).terrain = beam

  def _genEntities(self):
    entities = {
      itemtypes.Coal: True,
      itemtypes.Tin: True,
      itemtypes.Copper: True,
      itemtypes.Iron: True,
      itemtypes.Diamond: True,
      itemtypes.Water: False,
      itemtypes.BatSpawner: False,
      itemtypes.SpiderSpawner: False,
      itemtypes.SnakeSpawner: False,
      itemtypes.GoblinSpawner: False,
      itemtypes.TrollSpawner: False,
      itemtypes.DragonSpawner: False
    }

    for entity in entities:
      inWall = entities[entity]
      placed = 0
      while placed < entity.genCount:
        genMin = int(self.caveH * entity.genMin)
        genMax = int(self.caveH * entity.genMax)
        x = randrange(self.caveW - 1)
        y = randrange(genMin, genMax)
        cell = self.cave.getCell(x, y)

        # We've already got one
        if entity in cell.entities:
          continue
        # Not in a cave wall, when we should be, or vice versa
        if inWall == cell.passable() or inWall == cell.transparent():
          continue
        # Too close to the bottom
        if y >= self.caveH - 1:
          continue
        # Out in the open, and no floor below (forces non inWall items to be on the ground, no effect on inWall items)
        if cell.passable() and self.cave.getCell(x, y+1).passable():
          continue
        self.cave.addEntity(entity, x, y)
        placed += 1

  def _genLava(self):
    for y in range(1, 7):
      _y = self.caveH - y
      for x in range(self.caveW):
        cell = self.cave.getCell(x, _y)
        if cell.passable():
          cell.setTerrain(terrains.lava)
  def countWallNeighbours(self, x, y) :
    n = 0
    for _x in range ( -1, 2 ):
      for _y in range ( -1, 2 ):
        if not _x and not _y:
          continue
        try:
          c = self.cave.getCell(x + _x, y + _y)
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
      'back': {
        'key': libtcod.KEY_ESCAPE,
        'ch': None,
        'fn': self.backToMenu
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
    playState.setCave(self.cave)
    self._manager.setNextState('Play')
  def backToMenu(self):
    menuState = self._manager.getState('Menu')
    menuState.reset()
    self._manager.setNextState('Menu')
    self._manager.setNextState('Menu')
from Player import Player
from MyElements import MyMapElement
from Terrain import terrains
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class PlayState(GameState):

  def __init__(self, name, manager, ui):
    super(PlayState, self).__init__(name, manager, ui)
    self._setupInputs()

    self.player = Player()
    self.player.setChar('@')
    self.player.setColor(libtcod.white)

    self.dug = None


  def tick(self):
    self.mapElement.center(self.player.x, self.player.y)
    if self.player.falling:
      if self.cave.getCell(self.player.x, self.player.y + 1).passable():
        self.mvPlayer(0, 1, self.player.moveD)
      else:
        self.player.falling = False

    if self.player.needFovUpdate:
      self.player.needFovUpdate = False
      self.mapElement.calculateFovMap()



  def setCave(self, cave):
    self.cave = cave
    self._setupView()
    self.placePlayer()

  def _setupInputs(self):
    self.view.setInputs({
      'mvUp': {
          'key': libtcod.KEY_KP8,
          'ch': None,
          'fn': self.mvUp
        },
        'mvDn': {
          'key': libtcod.KEY_KP2,
          'ch': None,
          'fn': self.mvDn
        },
        'mvRgt': {
          'key': libtcod.KEY_KP6,
          'ch': None,
          'fn': self.mvRgt
        },
        'mvLft': {
          'key': libtcod.KEY_KP4,
          'ch': None,
          'fn': self.mvLft
        },
        'mvUpLft': {
          'key': libtcod.KEY_KP7,
          'ch': None,
          'fn': self.mvUpLft
        },
        'mvUpRgt': {
          'key': libtcod.KEY_KP9,
          'ch': None,
          'fn': self.mvUpRgt
        },
        'mvDnLft': {
          'key': libtcod.KEY_KP1,
          'ch': None,
          'fn': self.mvDnLft
        },
        'mvDnRgt': {
          'key': libtcod.KEY_KP3,
          'ch': None,
          'fn': self.mvDnRgt
        },
        
        # 'toggleRope': {
        #   'key': libtcod.KEY_SPACE,
        #   'ch': None,
        #   'fn': self.ropeToggle
        # },
        'proceed': {
          'key': libtcod.KEY_ESCAPE,
          'ch': None,
          'fn': self.proceed
        },
      })

  def placePlayer(self):
    playerX = 1
    playerY = 1
    placed = False
    while not placed:
      c = self.cave.getCell(playerX, playerY)
      if not c.passable():
        self.cave.addEntity(self.player, playerX, playerY - 1)
        self.player.setCoords(playerX, playerY - 1)
        self.mapElement.setPlayer(self.player)
        placed = True
      else:
        playerY += 1

  def _setupView(self):
    self.mapElement = self.view.addElement(MyMapElement(0, 0, self.cave.width, self.view.height, self.cave))
  
  ########
  # State transitions
  def proceed(self):
    menuState = self._manager.getState('Menu')
    menuState.reset()
    self._manager.setNextState('Menu')
  ########

  def mvPlayer(self, deltaX, deltaY, playerFunc):
    x = self.player.x + deltaX
    y = self.player.y + deltaY
    cell = self.cave.getCell(x, y)
    if x >= 0 and x < self.cave.width and y >= 0 and y < self.cave.height:
      if cell.passable() or self.dig(x, y):
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        playerFunc()
        self.cave.addEntity(self.player, self.player.x, self.player.y)
        self.player.falling = self.cave.getCell(self.player.x, self.player.y + 1).passable()

  ########
  # Input handlers
  def mvUp(self) :
    self.mvPlayer(0, -1, self.player.moveU)

  def mvDn(self) :
    self.mvPlayer(0, 1, self.player.moveD)

  def mvLft(self) :
    self.mvPlayer(-1, 0, self.player.moveL)

  def mvRgt(self) :
    self.mvPlayer(1, 0, self.player.moveR)

  def mvUpLft(self) :
    self.mvPlayer(-1, -1, self.player.moveUL)

  def mvUpRgt(self) :
    self.mvPlayer(1, -1, self.player.moveUR)

  def mvDnLft(self) :
    self.mvPlayer(-1, 1, self.player.moveDL)

  def mvDnRgt(self) :
    self.mvPlayer(1, 1, self.player.moveDR)

  def dig(self, x, y):

    cell = self.cave.getCell(x, y)
    if self.dug == (x, y):
      if y <= 5:
        t = terrains.openAir
      else:
        t = terrains.openMine

      cell.setTerrain(t)
      libtcod.map_set_properties(self.mapElement.fovMap, x, y, True, True)
      return True
    else:
      self.dug = (x, y)







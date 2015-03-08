from Player import Player
from MyElements import MyMapElement
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class PlayState(GameState):

  def __init__(self, name, manager, ui):
    super(PlayState, self).__init__(name, manager, ui)
    self._setupInputs()

    self.player = Player()
    self.player.setChar('@')
    self.player.setColor(libtcod.white)

    #TODO REMOVE
    self.offset = 0

  def tick(self):
    self.mapElement.center(0, self.offset)
    if self.player.calculateFov:
      self.player.calculateFov()
    pass

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


  #TODO REMOVE
  def scrollUp(self):
    if self.offset > 0:
      self.offset -= 1
    pass
  def scrollDown(self):
    if self.offset < self.cave.height - self.view.height:
      self.offset += 1
  # END TODO

  def placePlayer(self):
    playerX = 1
    playerY = 1
    placed = False
    while not placed:
      c = self.cave.getCell(playerX, playerY)
      if not c.passable():
        self.cave.addEntity(self.player, playerX, playerY - 1)
        self.player.setCoords(playerX, playerY - 1)
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
  
  ########
  # Input handlers
  def mvUp(self) :
    y = self.player.y - 1
    cell = self.cave.getCell(self.player.x, y)
    if y >= 0:
      if cell.passable():
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveU()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvDn(self) :
    y = self.player.y + 1
    cell = self.cave.getCell(self.player.x, y)
    if y < self.cave.height:
      if cell.passable():
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveD()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvLft(self) :
    x = self.player.x - 1
    cell = self.cave.getCell(x, self.player.y)
    if x >= 0:
      if cell.passable():
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveL()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvRgt(self) :
    x = self.player.x + 1
    cell = self.cave.getCell(x, self.player.y)
    if x < self.cave.width:
      if cell.passable():
        print "moving right"
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveR()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvUpLft(self) :
    y = self.player.y - 1
    x = self.player.x - 1
    cell = self.cave.getCell(x, y)
    if y >= 0 and x >= 0:
      if cell.passable():
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveUL()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvUpRgt(self) :
    y = self.player.y - 1
    x = self.player.x + 1
    cell = self.cave.getCell(x, y)
    if y >= 0 and x < self.cave.width:
      if cell.passable():
        print "moving up/right"
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveUR()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvDnLft(self) :
    y = self.player.y + 1
    x = self.player.x - 1
    cell = self.cave.getCell(x, y)
    if y < self.cave.height:
      if cell.passable():
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveDL()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

  def mvDnRgt(self) :
    y = self.player.y + 1
    x = self.player.x + 1
    cell = self.cave.getCell(x, y)
    if y < self.cave.height and x < self.cave.width:
      if cell.passable():
        oldCell = self.cave.getCell(self.player.x, self.player.y)
        oldCell.removeEntity(self.player)
        self.player.moveDR()
        self.cave.addEntity(self.player, self.player.x, self.player.y)

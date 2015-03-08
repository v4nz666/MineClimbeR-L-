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
      'mapUp': {
        'key': libtcod.KEY_UP,
        'ch': None,
        'fn': self.scrollUp
      },
      'mapDn': {
        'key': libtcod.KEY_DOWN,
        'ch': None,
        'fn': self.scrollDown
      },
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


  ########
  # State transitions
  def proceed(self):
    menuState = self._manager.getState('Menu')
    menuState.reset()
    self._manager.setNextState('Menu')


  def placePlayer(self):
    playerX = 1
    playerY = 1
    placed = False
    while not placed:
      c = self.cave.getCell(playerX, playerY)
      if not c.passable():
        self.cave.addEntity(self.player, playerX, playerY - 1)
        placed = True
      else:
        playerY += 1

  def _setupView(self):
    self.mapElement = self.view.addElement(MyMapElement(0, 0, self.cave.width, self.view.height, self.cave))

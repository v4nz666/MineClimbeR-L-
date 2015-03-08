from math import tanh
from Player import Player
from RoguePy.UI import Elements
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
    pass

  def setCave(self, cave):
    self.cave = cave
    self._setupView()
    self.placePlayer()

  def drawOverlay(self):
    offset = self.mapElement._offsetY * 1.0
    #TODO player.y / self.cave.height
    opacity = offset / self.cave.height

    for y in range(self.mapOverlay.height):
      for x in range(self.mapOverlay.width):
        c = self.cave.getCell(x, y)
        # If we've seen this cell before, darken as we go
        if not self.fog[x][y + int(offset)]:
          libtcod.console_put_char(self.mapOverlay.console, x, y, ' ', libtcod.BKGND_ALPHA(opacity) )
        # Otherwise render full opacity
        else:
          libtcod.console_put_char(self.mapOverlay.console, x, y, ' ', libtcod.BKGND_ALPHA(1.0) )

  def drawMap(self):
    Elements.Map.draw(self.mapElement)
    self.drawOverlay()
    libtcod.console_blit(self.mapOverlay.console, 0,0, self.mapOverlay.width, self.mapOverlay.height,
                         self.view.console, 0,0)



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
      playerY += 1

  def _setupView(self):
    self.mapElement = self.view.addElement(Elements.Map(0, 0, self.cave.width, self.view.height, self.cave))
    #Trickery. We'll draw the overlay ourselves
    self.mapOverlay = self.mapElement.addElement(Elements.Element(0, 0, self.cave.width, self.view.height)).hide()
    self.mapElement.draw = self.drawMap
    self.mapOverlay.bgOpacity = 0.0
    self._setupFog()

  def _setupFog(self):
    self.fog = [[True for _y in range(self.cave.height)] for _x in range(self.cave.width)]
    for y in range(8):
      for x in range(self.cave.width):
        c = self.cave.getCell(x, y)
        if c.passable():
          self.fog[x][y] = False


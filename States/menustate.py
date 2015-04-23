from time import sleep
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class MenuState(GameState):
  def __init__(self, name, manager, ui):
    super(MenuState, self).__init__(name, manager, ui)

    self.mapReady = False
    self.proceeding = 0

    self._setupView()
    self._setupInputs()

  def _setupView(self):

    # New Game
    # Help
    # About
    # Quit

    menuW = 8
    menuH = 4
    menuX = (self.view.width - menuW) / 2
    menuY = (self.view.height - menuH) / 2

    self.menu = self.view.addElement(
      Elements.Menu(menuX, menuY, menuW, menuH, [
        {'New Game' : self.menuSelected},
        {'Help' : self.menuSelected},
        {'About' : self.menuSelected},
        {'Exit' : self.menuSelected}
      ])
    )

    self.generatingCave = self.view.addElement(Elements.Label(1, 1, "Generating Mine")).setDefaultColors(libtcod.green)
    self.generatingCave.setDefaultColors(libtcod.green)\
      .hide()
    self.reticulating = self.view.addElement(Elements.Label(1, 2, "Reticulating Splines"))
    self.reticulating.setDefaultColors(libtcod.green)\
      .hide()

  def reset(self):
    self.view.clear()
    self._setupView()
    self._setupInputs()
    self.proceeding = 0
    self.mapReady = False
    self.setBlocking(True)
    self.menu.show()
    self.generatingCave.hide()
    self.reticulating.hide()


  def _setupInputs(self):
    self.view.setInputs({
      'menuUp': {
        'key': libtcod.KEY_UP,
        'ch': None,
        'fn': self.menu.selectUp
      },
      'menuDn': {
        'key': libtcod.KEY_DOWN,
        'ch': None,
        'fn': self.menu.selectDown
      },
      'menuSelect': {
        'key': libtcod.KEY_ENTER,
        'ch': None,
        'fn': self.menu.selectFn
      },
      'menuUpKP': {
        'key': libtcod.KEY_KP8,
        'ch': None,
        'fn': self.menu.selectUp
      },
      'menuDnKP': {
        'key': libtcod.KEY_KP2,
        'ch': None,
        'fn': self.menu.selectDown
      },
      'menuSelectKP': {
        'key': libtcod.KEY_KPENTER,
        'ch': None,
        'fn': self.menu.selectFn
      },

    })

  def tick(self):
    if self.proceeding == 1:
      self.proceeding += 1
      self.setBlocking(False)
      self.menu.hide()
      self.generatingCave.show()
    elif self.proceeding == 2:
      self.proceeding += 1
      worldGenState = self._manager.getState('WorldGen')
      worldGenState.initCave()
      self.mapReady = True
      self.reticulating.show()
    elif self.proceeding == 3:
      sleep(0.2)
      self._manager.setNextState('WorldGen')
    else:
      pass

  ########
  # State Transitions
  def menuSelected(self, selected):
    if not self.mapReady:
      if selected == 0:
        self.proceeding = 1
      elif selected == 1:
        self._manager.setNextState('Help')
      elif selected == 2:
        self._manager.setNextState('About')
      elif selected == 3:
        self._manager.setNextState('Quit')
  ########


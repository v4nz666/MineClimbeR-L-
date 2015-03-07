from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class MenuState(GameState):
  def __init__(self, name, manager, ui):
    super(MenuState, self).__init__(name, manager, ui)
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
        {'Quit' : self.menuSelected}
      ])
    )


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
    })
    pass


  ########
  # State Transitions
  def menuSelected(self, selected):
    if selected == 0:
      self._manager.setNextState('WorldGen')
    elif selected == 1:
      self._manager.setNextState('Help')
    elif selected == 2:
      self._manager.setNextState('About')
    elif selected == 3:
      self._manager.setNextState('Quit')
  ########


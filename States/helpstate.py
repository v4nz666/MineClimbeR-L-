from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState
from UiElements import HelpElement


class HelpState(GameState):

  def __init__(self, name, manager, ui):
    super(HelpState, self).__init__(name, manager, ui)
    self.helpElement = self.view.addElement(HelpElement(self.view))
    self._setupInputs()

  def _setupInputs(self):
    self.view.setInputs({
      'backToMenu': {
        'key': libtcod.KEY_ESCAPE,
        'ch': None,
        'fn': self.backToMenu
      },
      'nextTab': {
        'key': libtcod.KEY_TAB,
        'ch': None,
        'fn': self.helpElement.cycleTabs
      }
    })


  def backToMenu(self):
    self._manager.setNextState('Menu')

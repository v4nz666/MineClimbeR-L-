from RoguePy.State.GameState import GameState
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod

class TitleState(GameState):

  def __init__(self, name, manager, ui):
    super(TitleState, self).__init__(name, manager, ui)
    self._setupView()
    self._setupInputs()

  def _setupView(self):
    title = "MineClimbeR(L)"
    titleX = (self.view.width - len(title)) / 2
    titleY = self.view.height / 2 - 1
    _7drl = "a 7dRL"
    _7drlX = (self.view.width - len(_7drl)) / 2
    credits = "2015 - Jeff Ripley"
    creditsX = (self.view.width - len(credits)) / 2

    self.view.addElement(Elements.Label(titleX, titleY, title)).setDefaultColors(libtcod.gold)
    self.view.addElement(Elements.Label(_7drlX, titleY+1, _7drl)).setDefaultColors(libtcod.grey)
    self.view.addElement(Elements.Label(creditsX, titleY + 2, credits)).setDefaultColors(libtcod.silver)

  def _setupInputs(self):
    self.view.setInputs({
      'proceed': {
        'key': 'any',
        'ch': None,
        'fn': self.proceed
      }
    })
    pass

  def proceed(self):
    self._manager.setNextState('Story')

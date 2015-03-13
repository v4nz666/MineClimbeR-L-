from time import sleep
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class DeathState(GameState):


  def __init__(self, name, manager, ui):
    super(DeathState, self).__init__(name, manager, ui)
    self._setupView()
    self.shown = False
    self.slept = False

  def tick(self):
    if not self.shown:
      self.shown = True
    elif not self.slept:
      sleep(2)
      self._setupInputs()
      self.pressKey.show()

  def reset(self):
    self.shown = False
    self.slept = False
    self.pressKey.hide()

  def _setupView(self):
    title = "You have died"
    titleX = (self.view.width - len(title)) / 2
    titleY = self.view.height / 2
    self.view.addElement(Elements.Label(titleX, titleY, title)).setDefaultColors(libtcod.black, libtcod.dark_red)
    pressKey = "Press Any Key" 
    pressKeyX = (self.view.width - len(pressKey)) / 2
    pressKeyY = self.view.height / 2 + 1
    self.pressKey = self.view.addElement(Elements.Label(pressKeyX, pressKeyY, pressKey))\
      .setDefaultColors(libtcod.black, libtcod.dark_red)\
      .hide()

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
    menuState = self._manager.getState('Menu')
    menuState.reset()
    self._manager.setNextState('Menu')

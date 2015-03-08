from RoguePy.UI import Elements
from RoguePy.State.GameState import GameState

class PlayState(GameState):

  def __init__(self, name, manager, ui):
    super(PlayState, self).__init__(name, manager, ui)
    self._setupView()
    self._setupInputs()

  def tick(self):
    pass

  def setCave(self, cave):
    self.cave = cave
    self.mapElement = self.view.addElement(Elements.Map(0, 0, self.cave.width, self.view.height, self.cave))

  def _setupView(self):
    pass


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

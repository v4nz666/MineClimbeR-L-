from RoguePy.State.GameState import GameState

class AboutState(GameState):

  def tick(self):
    self._manager.setNextState('Menu')
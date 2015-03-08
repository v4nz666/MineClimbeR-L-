from RoguePy.State.GameState import GameState

class HelpState(GameState):


  def tick(self):
    self._manager.setNextState('Menu')
from RoguePy.State.GameState import GameState

class HelpState(GameState):


  def tick(self):
    print "Help"
    self._manager.setNextState('Menu')
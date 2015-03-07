from RoguePy.State.GameState import GameState

class AboutState(GameState):

  def tick(self):
    print "About"
    self._manager.setNextState('Menu')
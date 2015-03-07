from RoguePy.State.GameState import GameState

class MenuState(GameState):

  def tick(self):
    print "Menu"

    self._manager.setNextState('WorldGen')

  pass
from RoguePy.State.GameState import GameState

class TitleState(GameState):

  def tick(self):
    print "Title"

    self._manager.setNextState('Menu')

  pass
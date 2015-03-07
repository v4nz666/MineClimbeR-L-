from RoguePy.State.GameState import GameState

class PlayState(GameState):
  def tick(self):
    print "Playing"

    self._manager.setNextState('Quit')

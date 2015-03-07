from RoguePy.State.GameState import GameState

class WorldGenState(GameState):
  def tick(self):
    self._manager.setNextState('Play')

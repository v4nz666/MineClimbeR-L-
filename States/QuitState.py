from sys import exit
from RoguePy.State.GameState import GameState

class QuitState(GameState):
  def tick(self):
    exit()
  pass
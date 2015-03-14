"""
StateManager
"""


class StateManager():
  def __init__(self):
    self._states = {}
    self._currentState = None
    self._nextState = None
  
  def addState(self, gameState):
    self._states[gameState.getName()] = gameState
    return gameState
  def getState(self, stateName):
    if stateName in self._states:
      return self._states[stateName]
    else:
      return None
  
  def getCurrentState(self):
    return self._currentState
  def setCurrentState(self, stateName):
    newState = self._states[stateName]
    newState.beforeLoad()
    self._currentState = newState
    
  def getNextState(self):
    return self._nextState
  def setNextState(self, stateName):
    self._nextState = self._states[stateName]

  def doTick(self):
    state = self._currentState
    state.tick()
    state.ui.refresh(state)
    state.processInput()
    self.stateTransition()
  
  def stateTransition(self):
    if self._nextState and self._currentState != self._nextState:
      self._currentState.beforeUnload()
      self._currentState = self._nextState
      self._nextState = None

from InputHandler import InputHandler

class KeyboardHandler(InputHandler) :
  def __init__(self):
    self.keyInputs = {}
    self.key = None
  
  def _addKeyInputs(self, inputs):
    for i in inputs:
      self.keyInputs[i] = inputs[i]
  def setInputs(self, inputs):
    self.keyInputs = {}
    self._addKeyInputs(inputs)
  
  
  def handleKeyInput(self, key):
    for name in self.keyInputs:
      cmd = self.keyInputs[name]
      if ( cmd['key'] and ( cmd['key'] == key.vk or str(cmd['key']).lower() == "any") ) or (
        cmd['ch'] and ( ord(cmd['ch'].lower()) == key.c or ord(cmd['ch'].upper()) == key.c ) ):
          return cmd['fn']()
    return self

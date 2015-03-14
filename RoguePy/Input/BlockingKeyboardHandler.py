from RoguePy.Input.KeyboardHandler import KeyboardHandler
from RoguePy.libtcod import libtcod

class BlockingKeyboardHandler(KeyboardHandler):
  def handleInput(self):
    key = libtcod.console_wait_for_keypress(True)
    self.handleKeyInput(key)
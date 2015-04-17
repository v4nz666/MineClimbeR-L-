'''
Documentation, License etc.

@package RoguePy.UI
'''
from RoguePy.libtcod import libtcod

class View(object):

  def __init__(self, ui):
    self.x = 0
    self.y = 0
    self.width = ui.getWidth()
    self.height = ui.getHeight()
    
    self._elements = []
    self._inputs = {}
    
    self._storedEnabled = None
    
    self.console = libtcod.console_new(self.width, self.height)
    self.inputsEnabled = True
    self.fg = libtcod.white
    self.bg = libtcod.black

  def clear(self):
    for e in self._elements:
      e.clear()
    self._elements = []
    self._inputs = {}

  def getElements(self):
    return self._elements
  
  def getConsole(self):
    return self.console
  
  def addElement(self, el):
    if el.x + el.width >= self.width:
      el.width = self.width - el.x
    if el.y + el.height>= self.height:
      el.height = self.height - el.y
  
    self._elements.append(el)
    el.setParent(self)
    return el
  def removeElement(self, el):
    if el in self._elements:
      self._elements.remove(el)
  
  def setInputs(self, inputs):
    """
    Set the inputs to be bound to this View/Element

    :param inputs: Dictionary of input definitions. Takes the format:
      {
        'quit': {
          'key': libtcod.KEY_ESCAPE,
          'char': None,
          'fn': self.quitCallback
        },
        ...,
        'goNorth': {
          'key': libtcod.KEY_CHAR,
          'char': 'n',
          'fn': self.move
        },
        ...
      }
    """
    self._inputs = inputs
  def getInputs(self):
    return self._inputs
  
  def storeState(self):
    """
    Store the enabled status of all elements. This method must be called prior to calling restoreState. Use this method
      in conjunction with the disableAll method to put the view into "modal" mode, by calling them, then manually
      enabling an element.


    :return: None
    """
    self._storedEnabled = []
    index = 0
    for e in self._elements:
      if e.enabled:
        self._storedEnabled.append(index)
      index += 1
  def restoreState(self):
    """
    Restore the enabled state of all elements previously stored via storeState.

    :raise Exception: When called before a call to storeState.
    """
    if not self._storedEnabled:
      raise Exception("You must call storeState before calling restoreState.")
    for index in self._storedEnabled:
      self._elements[index].enable()
  
  def disableAll(self, disableSelf=True):
    """
    Disable all elements. Disabled elements are rendered with a low-opacity black overlay.

    :param disableSelf: Also disable the Inputs bound directly to the View? Defaults to True
    """
    for e in self._elements:
      e.disable()
    if disableSelf:
      self.disableInputs()
  
  def enableInputs(self):
    self.inputsEnabled = True
  def disableInputs(self):
    self.inputsEnabled = False
  
  def getActiveInputs(self, _inputs={}, el=None):
    """
    Recursive function to get the inputs of our self, and all active elements.

    :param _inputs: The inputs we've gathered so far
    :param el: The current element we're working on
    :return: The full list of all active Inputs
    """
    if el is None:
      el = self
      inputs = {}
    else:
      inputs = _inputs
    if ( el == self ) or ( el.visible and el.enabled ):
      if ( el == self and self.inputsEnabled ) or el != self:
        newInputs = el.getInputs()
        inputs.update(newInputs)
        
      for e in el.getElements():
        self.getActiveInputs(inputs, e)
    if el == self:
      return inputs
  
  def setDefaultForeground(self, fg, cascade=False):
    libtcod.console_set_default_foreground(self.console,fg)
    if cascade:
      for e in self._elements:
        e.setDefaultForeground(fg, True)
  def setDefaultBackground(self, bg, cascade=False):
    libtcod.console_set_default_background(self.console,bg)
    if cascade:
      for e in self._elements:
        e.setDefaultBackground(bg, True)
  #TODO Convert fg, bg to a tuple
  def setDefaultColors(self, fg = libtcod.white, bg = libtcod.black, cascade=False):
    self.setDefaultForeground(fg, cascade)
    self.setDefaultBackground(bg, cascade)
    return self
  
  def getDefaultColors(self):
    return self.fg, self.bg
  
  def clearConsole(self):
    libtcod.console_clear(self.console)
    return self
  
  def renderElements(self):
    for e in self._elements:
      e.clearConsole()
      if not e.visible:
        continue
      try:
        e.updateAnimationFrame()
      except AttributeError:
        pass
      e.draw()
      e.renderElements()
      if not e.enabled:
        self.renderOverlay(e)
      libtcod.console_blit(e.getConsole(), 0, 0, e.width, e.height, self.console, e.x, e.y, e.fgOpacity, e.bgOpacity)

  @staticmethod
  def renderOverlay(el):
    if not (el.width and el.height):
      return
    con = libtcod.console_new(el.width, el.height)
    libtcod.console_set_default_background(con, libtcod.black)
    libtcod.console_blit(con, 0, 0, el.width, el.height, el.console, 0, 0, 0.0, 0.4)
    libtcod.console_delete(con)
    

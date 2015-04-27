'''
Documentation, License etc.

@package RoguePy.UI
'''
from RoguePy.libtcod import libtcod
from RoguePy.UI.Elements import Element

class Slider(Element):
  
  def __init__(self, x, y, w, min, max, val=0, step=1):
    self._min = min
    self._max = max
    self._val = val
    self.setStep(step)
    
    super(Slider, self).__init__(x, y, w, 1)
    self.sliderWidth = self.width - 2
    self.valPerChar = 1 + (self._max - self._min) / self.sliderWidth
    self.setChars(['<','-','>','|'])
  
  def onChange(self):
    pass
  
  def setMin(self, min):
    self._min = min
  def getMin(self):
    return self._min
  
  def setMax(self, max):
    self._max = max
  def getMax(self):
    return self._max

  def setVal(self, val):
    if val > self._max:
      val = self._max
    elif val < self._min:
      val = self._min
    if val != self._val:
      self._val = val
      self.onChange()
    
  def getVal(self):
    return self._val
  
  def setStep(self, step):
    self._step = step
  def getStep(self):
    return self.step
  
  def setChars(self, chars):
    if not len(chars) == 4:
      raise IndexError("chars list must contain 4 elements")
    self._left = chars[0]
    self._center = chars[1]
    self._right = chars[2]
    self._bar = chars[3]
  
  def left(self):
    self.setVal(self._val - self._step)
  def right(self):
    self.setVal(self._val + self._step)
  
  def draw(self):
    libtcod.console_put_char(self.console, 0, 0,self._left)
    for x in range(self.sliderWidth):
      libtcod.console_put_char(self.console, x + 1, 0, self._center)
    libtcod.console_put_char(self.console, self.width - 1, 0, self._right)

    sliderPosition = min(self.sliderWidth, self._val / self.valPerChar)
    libtcod.console_put_char(self.console, sliderPosition, 0, self._bar)

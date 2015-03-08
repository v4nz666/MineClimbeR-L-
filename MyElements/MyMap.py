from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod

class MyMap(Elements.Map):
  def __init__(self, x, y, w, h, _map):
    super(MyMap, self).__init__(x, y, w, h, _map)
    self.overlay = libtcod.console_new(w, h)
    self._setupFog()

  def draw(self):
    for y in range(self.height):
      for x in range(self.width):
        # If we've explored this cell already ,render it
        if self.seen[x][y]:
          c = self._map.getCell(x + self._offsetX, y + self._offsetY)
          libtcod.console_put_char_ex(self.console, x, y, c.terrain.char, c.terrain.fg, c.terrain.bg)

          for i in range(len(c.entities)):
            e = c.entities[i]
            libtcod.console_put_char(self.console, x, y, e.char)
            libtcod.console_set_char_foreground(self.console, x, y, e.color)
        # Otherwise, render the fog of war
        else:
          libtcod.console_put_char_ex(self.console, x, y, ' ', libtcod.black, libtcod.black)
    self.drawOverlay()

  def drawOverlay(self):
    offset = self._offsetY * 1.0
    #TODO calculate this once, and store in a list keyed by offset
    opacity = offset / ( self._map.height - self.height )
    opacity = 0.5 + (opacity / 2)
    print "Opacity at: " + str(opacity)
    libtcod.console_blit(self.overlay, 0, 0, self.width, self.height, self.console, 0, 0, 0, opacity)

  def _setupFog(self):
    self.seen = [[False for _y in range(self._map.height)] for _x in range(self._map.width)]
    for y in range(8):
      for x in range(self._map.width):
        c = self._map.getCell(x, y)
        if c.passable():
          self.seen[x][y] = True
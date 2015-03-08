from math import sqrt
from math import pow
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod

class MyMapElement(Elements.Map):

  torchAlpha = 0.5
  torchColor = libtcod.desaturated_flame

  def __init__(self, x, y, w, h, _map):
    super(MyMapElement, self).__init__(x, y, w, h, _map)
    self.overlay = libtcod.console_new(w, h)
    self._setupFog()
    self._initFovMap()
    self.player = None

  def setPlayer(self, player):
    self.player = player

  def draw(self):
    libtcod.console_clear(self.overlay)

    fogOpacity = min(1, (1.0*self.player.y) / self._map.height)
    for y in range(self.height):
      for x in range(self.width):
        c = self._map.getCell(x, y+self._offsetY)
        libtcod.console_put_char_ex(self.console, x, y, c.terrain.char, c.terrain.fg, c.terrain.bg)

        visible = libtcod.map_is_in_fov(self._map._map, x, y + self._offsetY)
        if visible:
          # Render the top item, if there are any here
          if len(c.entities) > 0:
            item = c.entities[len(c.entities)-1]
            libtcod.console_put_char_ex(self.console, x, y, item.char, item.color, c.terrain.bg)
        else:
          self.renderFovOverlay(x, y, fogOpacity)


  def renderFovOverlay(self, x, y, opacity):
    """
    We'll only be called for coordinates outside the torch light, leaving a space where the torch reaches

    :param x: onscreen x coord
    :param y: onscreen y coord
    :param opacity: opacity to render the fog at
    :return: None
    """
    cell = self._map.getCell(x, y + self._offsetY)

    # Above ground, don't worry about it
    if y + self._offsetY <= 5:
      return
    # Below ground, outside torch light, we'll render the fog of war
    else:

      if not self.seen[x][y]:
        color = libtcod.black
        opacity = 1
      else:
        color = cell.terrain.bg
    libtcod.console_put_char(self.console, x, y, ' ', libtcod.BKGND_ALPHA(opacity))


  @staticmethod
  def calculateIntensity(player, x, y):
    intensity = 1

    deltaX = player.x - x
    deltaY = player.y - y

    distance = sqrt(pow(deltaX,2) + pow(deltaY, 2))

    if distance > 0:
      intensity = 1 - pow(distance / player.torchStrength, 2)
      intensity = 1.0 / 4.0 + (3*intensity) / 4
    return intensity

  def drawOverlay(self):
    offset = self._offsetY * 1.0
    #TODO calculate this once, and store in a list keyed by offset
    opacity = offset / ( self._map.height - self.height )
    opacity = min(1, 0.25 + (opacity * 3 / 4))
    libtcod.console_blit(self.overlay, 0, 0, self.width, self.height, self.console, 0, 0, 0, opacity)

  def _setupFog(self):
    self.seen = [[False for _y in range(self._map.height)] for _x in range(self._map.width)]
    for y in range(8):
      for x in range(self._map.width):
        c = self._map.getCell(x, y)
        if c.passable():
          self.seen[x][y] = True

  def _initFovMap(self):
    self.fovMap = self._map._map
    for x in range(self._map.width):
      for y in range(self._map.height):
        c = self._map.getCell(x,y)
        libtcod.map_set_properties(self.fovMap, x, y, c.passable(), c.transparent())

  def calculateFovMap(self):
    libtcod.map_compute_fov(
        self._map._map, self.player.x, self.player.y, self.player.torchStrength, True, libtcod.FOV_SHADOW)
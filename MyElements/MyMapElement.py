from math import sqrt
from math import pow
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod

class MyMapElement(Elements.Map):

  torchAlpha = 0.5
  torchColor = libtcod.darkest_flame * 0.5

  def __init__(self, x, y, w, h, _map):
    super(MyMapElement, self).__init__(x, y, w, h, _map)
    self._setupFog()
    self._initFovMap()
    self.player = None

  def setPlayer(self, player):
    self.player = player

  def draw(self):
    baseOpacity = (1.0*self.player.y) / self._map.height
    fogOpacity = min(1, 0.5 + (baseOpacity * 0.5))
    for onScreenY in range(self.height):
      mapY = onScreenY + self._offsetY
      for x in range(self.width):
        c = self._map.getCell(x, mapY)
        inTorch = libtcod.map_is_in_fov(self._map._map, x, mapY)

        libtcod.console_put_char_ex(self.console, x, onScreenY, c.terrain.char, c.terrain.fg, c.terrain.bg)
        self.renderFovOverlay(c, x, mapY, fogOpacity, inTorch)

        if inTorch:
          self.seen[x][mapY] = True
          # Render the top item, if there are any here
          if len(c.entities) > 0:
            if self.player in c.entities:
              item = self.player
            else:
              item = c.entities[len(c.entities)-1]
            libtcod.console_put_char_ex(self.console, x, onScreenY, item.char, item.color, c.terrain.bg)



  def renderFovOverlay(self, cell, x, y, opacity, inTorch):
    """
    We'll only be called for coordinates outside the torch light, leaving a space where the torch reaches

    :param x: on map x coord
    :param y: on map y coord
    :param opacity: opacity to render the fog at
    :return: None
    """
    if y <= 5:
      opacity = 0
      color = libtcod.black
    elif inTorch:
      color = self.torchColor
      opacity = self.calculateIntensity(x, y)
    # Below ground, outside torch light, we'll render the fog of war
    else:
      if not self.seen[x][y]:
        color = libtcod.black
        opacity = 1
      else:
        color = cell.terrain.bg

    libtcod.console_put_char(self.console, x, y - self._offsetY, cell.terrain.char, libtcod.BKGND_ALPHA(opacity))
    if inTorch:
      libtcod.console_set_char_background(self.console, x, y - self._offsetY, color, libtcod.BKGND_ADDALPHA(opacity))

  def calculateIntensity(self, x, y):
    intensity = 0

    deltaX = self.player.x - x
    deltaY = self.player.y - y

    distance = sqrt(pow(deltaX,2) + pow(deltaY, 2))

    if distance > 0:
      intensity = pow(distance / self.player.torchStrength, 2)
    return intensity / 2

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
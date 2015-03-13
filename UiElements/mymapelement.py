from math import sqrt
from math import pow
from enemy import Enemy
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
    self.baseOpacity = 0
    self.fogOpacity = 0

  def setPlayer(self, player):
    self.player = player

  def draw(self):
    self.baseOpacity = (1.0*self.player.y) / self._map.height
    self.fogOpacity = min(1, 0.5 + (self.baseOpacity * 0.5))
    for onScreenY in range(self.height):
      mapY = onScreenY + self._offsetY
      for x in range(self.width):
        c = self._map.getCell(x, mapY)
        inTorch = libtcod.map_is_in_fov(self._map._map, x, mapY)

        if self.seen[x][mapY]:
          libtcod.console_put_char_ex(self.console, x, onScreenY, c.terrain.char, c.terrain.fg, c.terrain.bg)
        self.renderFovOverlay(c, x, mapY, inTorch)

        if inTorch:
          self.seen[x][mapY] = True
          if len(c.entities) > 0:

            # Take care of any spawners, while we're looping on the entities.
            # This should definitely not live here, in the display layer :/
            for e in c.entities:
              if e.spawns:
                enemyDef = e.spawns
                enemy = Enemy(self.player, *enemyDef['args'])
                print "Spawning enemy: " + str(enemy.name) + " at " + str((x, mapY))

                enemy.setAi(enemyDef['ai'](self._map, enemy))
                enemy.setMap(self._map)
                enemy.maxPath = enemyDef['maxPath']
                if 'range' in enemyDef:
                  enemy.range = enemyDef['range']
                if 'drops' in enemyDef:
                  enemy.drops = enemyDef['drops']
                  enemy.dropChance = enemyDef['dropChance']

                self._map.addEntity(enemy, x, mapY)
                enemy.setCoords(x, mapY)
                self._map.addEnemy(enemy)


            # Now that we've spawned any enemies, just remove any spawners that were in the list
            c.entities = [e for e in c.entities if not e.spawns]

            # Render the top item, if there are any here. Player takes precedence,though
            if self.player in c.entities:
              item = self.player
            elif len(c.entities) > 0:
              item = c.entities[-1]
            libtcod.console_put_char_ex(self.console, x, onScreenY, item.char, item.color, c.terrain.bg)

  def renderFovOverlay(self, cell, x, y, inTorch):
    """
    Render the torch, and fog of war overlay for cell

    :param x: on map x coord
    :param y: on map y coord
    :param opacity: opacity to render the fog at
    :return: None
    """
    # No overlay above ground.
    if y <= 5:
      return

    # Inside our torch light, we'll have a halo with increasing opacity
    if inTorch:
      bgColor = self.torchColor
      opacity = self.calculateIntensity(x, y)
      ch = cell.terrain.char
    # Below ground, outside torch light, we'll render the fog of war for any tiles we've seen
    else:
      # Straight black for tiles we haven't seen, no need to draw anything
      if not self.seen[x][y]:
        return
      else:
        bgColor = cell.terrain.bg
        opacity = self.fogOpacity
        ch = ' '

    libtcod.console_put_char(self.console, x, y - self._offsetY, ch, libtcod.BKGND_ALPHA(opacity))
    libtcod.console_set_char_foreground(self.console, x, y - self._offsetY, cell.terrain.fg)
    if inTorch:
      libtcod.console_set_char_background(self.console, x, y - self._offsetY, bgColor, libtcod.BKGND_ADDALPHA(opacity))

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
        if y <= 6 or c.passable():
          self.seen[x][y] = True

  def _initFovMap(self):
    self.fovMap = self._map._map
    for x in range(self._map.width):
      for y in range(self._map.height):
        c = self._map.getCell(x,y)
        libtcod.map_set_properties(self.fovMap, x, y, c.transparent(), c.passable())

  def calculateFovMap(self):
    libtcod.map_compute_fov(
        self._map._map, self.player.x, self.player.y, self.player.torchStrength, True, libtcod.FOV_SHADOW)

  def explored(self, x, y):
    return self.seen[x][y]
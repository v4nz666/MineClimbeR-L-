from Player import Player
from RoguePy.UI import Elements
from MyElements import MyMapElement
from Terrain import terrains
from Item.itemTypes import Anchor
from Item.itemTypes import Rope
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class PlayState(GameState):

  def __init__(self, name, manager, ui):
    super(PlayState, self).__init__(name, manager, ui)

    self.cave = None

    self.player = Player()
    self.player.setChar('@')
    self.player.setColor(libtcod.white)

    self.ropePath = []
    self.dug = None


  def tick(self):
    if self.player.dead():
      self.doDeathState()

    ########
    # Non-turn-based updates
    self.mapElement.center(self.player.x, self.player.y)

    if self.player.falling:
      if self.cave.getCell(self.player.x, self.player.y + 1).passable():
        self.player.fell += 1
        self.mvPlayer(0, 1, self.player.moveD)
      else:
        self.player.land()
    elif (not self.player.attached) and self.cave.getCell(self.player.x, self.player.y + 1).passable():
      self.player.falling = True

    if self.player.needFovUpdate:
      self.player.needFovUpdate = False
      self.mapElement.calculateFovMap()
    self._updateUI()
    ########

    ########
    # Turn -based updates
    for e in self.cave.enemies:
      if self.player.distance(e.x, e.y) <= e.maxPath:
        e.aiMove()
      else:
        print "out of range"

    ########


  def setCave(self, cave):
    self.cave = cave
    self._setupView()
    self._setupInputs()
    self.placePlayer()
    self.player.setMap(cave)

  def _setupInputs(self):
    self.view.setInputs({
      'mvUp': {
        'key': libtcod.KEY_KP8,
        'ch': None,
        'fn': self.mvUp
      },
      'mvDn': {
        'key': libtcod.KEY_KP2,
        'ch': None,
        'fn': self.mvDn
      },
      'mvRgt': {
        'key': libtcod.KEY_KP6,
        'ch': None,
        'fn': self.mvRgt
      },
      'mvLft': {
        'key': libtcod.KEY_KP4,
        'ch': None,
        'fn': self.mvLft
      },
      'mvUpLft': {
        'key': libtcod.KEY_KP7,
        'ch': None,
        'fn': self.mvUpLft
      },
      'mvUpRgt': {
        'key': libtcod.KEY_KP9,
        'ch': None,
        'fn': self.mvUpRgt
      },
      'mvDnLft': {
        'key': libtcod.KEY_KP1,
        'ch': None,
        'fn': self.mvDnLft
      },
      'mvDnRgt': {
        'key': libtcod.KEY_KP3,
        'ch': None,
        'fn': self.mvDnRgt
      },
      'wait': {
        'key': libtcod.KEY_KP5,
        'ch': None,
        'fn': self.wait
      },
      'toggleRope': {
        'key': libtcod.KEY_SPACE,
        'ch': None,
        'fn': self.ropeToggle
      },
      'openCrafting': {
        'key': libtcod.KEY_TAB,
        'ch': None,
        'fn': self.toggleCrafting
      },
      'quit': {
        'key': libtcod.KEY_ESCAPE,
        'ch': None,
        'fn': self.quit
      }
    })
    self.craftingModal.setInputs({
      'closeModal': {
        'key': libtcod.KEY_TAB,
        'ch': None,
        'fn': self.toggleCrafting
      },
      })
    self.invList.setInputs({
      'invUp': {
        'key': libtcod.KEY_PAGEUP,
        'ch': None,
        'fn': self.invList.scrollUp
      },
      'invDn': {
        'key': libtcod.KEY_PAGEDOWN,
        'ch': None,
        'fn': self.invList.scrollDown
      }
    })


  def placePlayer(self):
    playerX = 1
    playerY = 1
    placed = False
    while not placed:
      c = self.cave.getCell(playerX, playerY)
      if not c.passable():
        self.cave.addEntity(self.player, playerX, playerY - 1)
        self.player.setCoords(playerX, playerY - 1)
        self.mapElement.setPlayer(self.player)
        placed = True
      else:
        playerY += 1

  def _setupView(self):

    # Most importantly, our Map Element
    self.mapElement = self.view.addElement(MyMapElement(0, 0, self.cave.width, self.view.height, self.cave))

    # Setup the right-hand pane
    panelH = 12
    panelW = self.view.width / 5
    panelX =  self.view.width - panelW

    sharedTl = libtcod.CHAR_TEEE
    sharedTr = libtcod.CHAR_TEEW

    self.statFrame = self.view.addElement(Elements.Frame(panelX, 0, panelW, panelH)) \
      .setTitle('Stats').setDefaultColors(libtcod.white, libtcod.darkest_azure)

    self.fps = self.statFrame.addElement(Elements.Label(1, 1, 'FPS:   '))
    self.fps.setDefaultColors(libtcod.magenta)
    self.fps.bgOpacity = 0

    invY = self.statFrame.y + self.statFrame.height - 1
    self.invFrame = self.view.addElement(Elements.Frame(panelX, invY, panelW, panelH)) \
      .setTitle('Inv').setDefaultColors(libtcod.white, libtcod.darkest_azure)
    self.invFrame._chars['tl'] = sharedTl
    self.invFrame._chars['tr'] = sharedTr
    self.invList = self.invFrame.addElement(Elements.List(1, 1, panelW - 2, panelH - 2)) \
      .setDefaultColors(libtcod.dark_green)
    self.invList.bgOpacity = 0

    helpY = self.invFrame.y + self.invFrame.height - 1
    self.helpFrame = self.view.addElement(Elements.Frame(panelX, helpY, panelW, panelH)) \
      .setTitle('Commands').setDefaultColors(libtcod.white, libtcod.darkest_azure)
    self.helpFrame._chars['tl'] = sharedTl
    self.helpFrame._chars['tr'] = sharedTr

    self.helpList = self.helpFrame.addElement(Elements.List(1, 1, panelW - 2, panelH - 3)) \
      .setDefaultColors(libtcod.lightest_blue)
    self.defaultHelpItems = [
      'NP 1-9:   Move/Wait',
      'NP 0  :     Aim Bow',
      'Spc   : Toggle Rope',
      'Tab   :    Crafting',
      'PgUp/Dn: Scroll Inv'

    ]
    self.helpItem = self.helpFrame.addElement(Elements.Label(1, panelH - 2, "? - Detailed Help")) \
      .setDefaultColors(libtcod.gold)
    self.helpItem.bgOpacity = 0

    self.helpList.setItems(self.defaultHelpItems)
    self.helpList.bgOpacity = 0

    craftingX = self.view.width / 3
    craftingW = self.view.width / 3
    craftingY = self.view.height / 3
    craftingH = self.view.height / 3

    self.craftingModal = self.view.addElement(Elements.Modal(craftingX, craftingY, craftingW, craftingH))
    self.craftingFrame = self.craftingModal.addElement(Elements.Frame(0, 0, craftingW, craftingH)) \
      .setTitle('Crafting') \
      .setDefaultColors(libtcod.white, libtcod.darkest_azure)


  ########
  # State transitions
  def doDeathState(self):
    self._manager.setNextState('Death')

  def quit(self):
    menuState = self._manager.getState('Menu')
    menuState.reset()
    self._manager.setNextState('Menu')
  ########

  def mvPlayer(self, deltaX, deltaY, playerFunc):
    newX= self.player.x + deltaX
    newY = self.player.y + deltaY
    newCell = self.cave.getCell(newX, newY)
    if not (newX >= 0 and newX < self.cave.width and newY >= 0 and newY < self.cave.height):
      return False

    if newCell.passable() or self.dig(newX, newY):
      if self.player.attached:
        if newY <= 5:
          # Can't climb out of the cave, if we're clipped in
          return False
        else:
          try:
            lastRope = self.ropePath[-2]
          except IndexError:
            lastRope = None

          # Going back the way we came - Retract the rope
          if lastRope == (newX,newY):
            self.ropePath = self.ropePath[:-1]
            self.cave.getCell(self.player.x, self.player.y).removeEntity(Rope)
            self.player.pickupItem(Rope)
          # Have ropes left - extend the rope, placing an anchor if necessary
          elif Rope in self.player.inventory:
            if not Anchor in newCell.entities:
              # No existing anchor, have some in inventory
              if Anchor in self.player.inventory:
                self.cave.addEntity(Anchor, newX, newY)
                self.player.dropItem(Anchor)
              # No existing anchor, none in inventory, we're not going anywhere
              else:
                return False

            self.ropePath.append((newX, newY))
            self.cave.addEntity(Rope, newX, newY)
            self.player.dropItem(Rope)
          else:
            # No Ropes left, trying to extend, can't proceed
            return False


      #Remove player from previous cell
      oldCell = self.cave.getCell(self.player.x, self.player.y)
      oldCell.removeEntity(self.player)

      # Update the player object's internal representation of its location
      playerFunc()

      # Place the player in the nex cell, and collect any items
      self.cave.addEntity(self.player, self.player.x, self.player.y)
      for i in newCell.entities:
        try:
          if i.collectible and i.collect(self.player):
            newCell.removeEntity(i)
        except ValueError:
          pass

  def ropeToggle(self):
    if self.player.attached:
      # Remove the ropes from the cave
      for (x, y) in self.ropePath:
        self.cave.getCell(x, y).removeEntity(Rope)
      self.ropePath = []
      self.player.detach()
      self.player.falling = self.cave.getCell(self.player.x, self.player.y + 1).passable()
    else:
      if self.player.y > 5 and self.player.anchorIn():
        self.ropePath.append((self.player.x, self.player.y))
        self.cave.addEntity(Anchor, self.player.x, self.player.y)
        self.cave.addEntity(Rope, self.player.x, self.player.y)
        self.player.dropItem(Rope)

  ########
  # Input handlers
  def mvUp(self) :
    if self.player.falling:
      return
    self.mvPlayer(0, -1, self.player.moveU)

  def mvDn(self) :
    if self.player.falling:
      return
    self.mvPlayer(0, 1, self.player.moveD)

  def mvLft(self) :
    if self.player.falling:
      return
    self.mvPlayer(-1, 0, self.player.moveL)

  def mvRgt(self) :
    if self.player.falling:
      return
    self.mvPlayer(1, 0, self.player.moveR)

  def mvUpLft(self) :
    if self.player.falling:
      return
    self.mvPlayer(-1, -1, self.player.moveUL)

  def mvUpRgt(self) :
    if self.player.falling:
      return
    self.mvPlayer(1, -1, self.player.moveUR)

  def mvDnLft(self) :
    if self.player.falling:
      return
    self.mvPlayer(-1, 1, self.player.moveDL)

  def mvDnRgt(self) :
    if self.player.falling:
      return
    self.mvPlayer(1, 1, self.player.moveDR)

  def wait(self):
    print "Waiting"

  def toggleCrafting(self):
    if not self.craftingModal.visible:
      self.craftingModal.show(self.view)
    else:
      self.craftingModal.hide(self.view)

  ########
  # Map interactions
  def dig(self, x, y):
    cell = self.cave.getCell(x, y)

    oldTerrain = cell.terrain
    newTerrain = oldTerrain.digTerrain
    cell.setTerrain(newTerrain)

    item = oldTerrain.itemDrop
    if item:
      cell.addEntity(item)

    libtcod.map_set_properties(self.mapElement.fovMap, x, y, cell.transparent(), cell.passable())
    return cell.passable()
  ########

  ########
  # View updates - per tick
  def _updateUI(self):
    invDict = {}
    for i in self.player.inventory:
      key = i.name
      if key not in invDict:
        invDict[key] = 0
      invDict[key] += 1
    invList = map(lambda key: key + ": " + str(invDict[key]),invDict)
    self.invList.setItems(invList)
    self.fps.setLabel('FPS: ' + str(libtcod.sys_get_fps()))
    self.fps.setDefaultColors(libtcod.magenta)





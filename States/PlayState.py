from random import random
from Player import Player
from RoguePy.UI import Elements
from MyElements import MyMapElement
from Item.itemTypes import Anchor
from Item.itemTypes import Rope
from Item.itemTypes import CopperPick
from Terrain.terrains import lava
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class PlayState(GameState):

  def __init__(self, name, manager, ui):
    super(PlayState, self).__init__(name, manager, ui)

    self.cave = None

    self.player = Player()
    self.player.setChar('@')
    self.player.setColor(libtcod.white)
    self.player.collectPick(CopperPick)

    self.ropePath = []
    self.dug = None

    self.turnTaken = False

    self.torchTicks = 100
    self.ticks = 0


  def tick(self):
    if self.player.dead():
      self.doDeathState()

    ########
    # Non-turn-based updates
    self.ticks += 1
    if not self.ticks % self.torchTicks:
      self.player.torchStrength = max(1, self.player.torchStrength - 1)
      self.player.needFovUpdate = True

    if self.player.falling:
      if self.cave.getCell(self.player.x, self.player.y + 1).passable():
        self.player.fell += 1
        self.mvPlayer(0, 1, self.player.moveD, False)
      else:
        self.player.land()
        self.turnTaken = True
    elif (not self.player.attached) and self.cave.getCell(self.player.x, self.player.y + 1).passable():
      self.player.falling = True

    if self.player.needFovUpdate:
      self.player.needFovUpdate = False
      self.mapElement.calculateFovMap()

    self.mapElement.center(self.player.x, self.player.y)
    self._updateUI()
    ########

    ########
    # Turn -based updates
    if self.turnTaken:
      for e in self.cave.enemies:
        if self.player.distance(e.x, e.y) <= e.maxPath:
          e.aiUpdate()
          if self.player.dead():
            return
        else:
          pass

    ########
    self.turnTaken = False


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
    panelX = self.view.width - 20
    panelW = 18
    panelH = 11
    panelY = self.view.height - (panelH + 2)

    self.statPanel = self.mapElement.addElement(Elements.Element(panelX, panelY, panelW, panelH))\
      .setDefaultColors(libtcod.light_azure, libtcod.azure)
    self.statPanel.bgOpacity = 0
    
    hpLabel = self.statPanel.addElement(Elements.Label(5, 0, 'HP'))
    hpLabel.bgOpacity = 0
    hpLabel.setDefaultForeground(libtcod.green)

    self.hpBar = self.statPanel.addElement(Elements.Bar(8, 0, 10))
    self.hpBar.setMinColor(libtcod.dark_red)
    self.hpBar.setMaxColor(libtcod.dark_green)
    self.hpBar.setMin(0)
    self.hpBar.setMax(self.player.maxHealth)
    self.hpBar.setVal(self.player.health)

    pickLabel = self.statPanel.addElement(Elements.Label(3, 2, 'Pick'))
    pickLabel.bgOpacity = 0
    pickLabel.setDefaultForeground(libtcod.dark_green)
    
    self.pickBar = self.statPanel.addElement(Elements.Bar(8, 2, 10))
    self.pickBar.setMinColor(libtcod.dark_red)
    self.pickBar.setMaxColor(libtcod.dark_green)
    self.pickBar.setMin(0)
    self.pickBar.setMax(self.player.maxPickStrength)
    self.pickBar.setVal(self.player.pickStrength)

    self.ropeLabel = self.statPanel.addElement(Elements.Label(3, 4, 'Rope'))
    self.ropeLabel.bgOpacity = 0
    self.ropeLabel.setDefaultForeground(libtcod.dark_green)

    self.anchorLabel = self.statPanel.addElement(Elements.Label(0, 6, 'Anchors'))
    self.anchorLabel.bgOpacity = 0
    self.anchorLabel.setDefaultForeground(libtcod.silver)

    tabLabel = self.statPanel.addElement(Elements.Label(5, 8, 'TAB Inv/Craft'))
    tabLabel.bgOpacity = 0
    tabLabel.setDefaultForeground(libtcod.yellow)

    helpLabel = self.statPanel.addElement(Elements.Label(12, 10, '?-Help'))
    helpLabel.bgOpacity = 0
    helpLabel.setDefaultForeground(libtcod.light_yellow)

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

  def mvPlayer(self, deltaX, deltaY, playerFunc, turnTaken=True):

    self.turnTaken = turnTaken

    newX= self.player.x + deltaX
    newY = self.player.y + deltaY
    newCell = self.cave.getCell(newX, newY)
    if not (newX >= 0 and newX < self.cave.width and newY >= 0 and newY < self.cave.height):
      return False

    if newCell.passable() or self.dig(newX, newY):
      # If this is a legit move, then attack one enemy in the target cell
      if turnTaken:
        for e in self.cave.enemies:
          if e.x == newX and e.y == newY:
            self.player.attackActor(e)
            if e.dead():
              if e.drops:
                rnd = random()
                if rnd <= e.dropChance:
                  self.cave.addEntity(e.drops, e.x, e.y)
              self.cave.removeEnemy(e)
            return False

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

      if newCell.terrain == lava:
        self.player.health = 0
        return False

      # Collect any items in the new cell
      for i in newCell.entities:
        try:
          if i.collectible and i.collect(self.player):
            newCell.removeEntity(i)
        except ValueError:
          pass

      # Update the player object's internal representation of its location
      playerFunc()

      # Place the player in the new cell
      self.cave.addEntity(self.player, self.player.x, self.player.y)

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
    self.turnTaken = True

  def toggleCrafting(self):
    if not self.craftingModal.visible:
      self.craftingModal.show(self.view)
    else:
      self.craftingModal.hide(self.view)

  ########
  # Map interactions
  def dig(self, x, y):
    if not self.player.damagePick():
      return False
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
    #update hp bar
    self.hpBar.setVal(self.player.health)

    # Update pick bar
    if not self.player.pickStrength:
      self.pickBar.hide()
    else:
      self.pickBar.show()
      self.pickBar.setMax(self.player.maxPickStrength)
      self.pickBar.setVal(self.player.pickStrength)
      self.pickBar.calculateColors()

    self.ropeLabel.setLabel("Rope " + str(self.player.inventory.count(Rope)))
    self.ropeLabel.bgOpacity = 0
    self.anchorLabel.setLabel("Anchors " + str(self.player.inventory.count(Anchor)))
    self.anchorLabel.bgOpacity = 0




    # invDict = {}
    # for i in self.player.inventory:
    #   key = i.name
    #   if key not in invDict:
    #     invDict[key] = 0
    #   invDict[key] += 1
    # invList = map(lambda key: key + ": " + str(invDict[key]),invDict)
    # self.invList.setItems(invList)





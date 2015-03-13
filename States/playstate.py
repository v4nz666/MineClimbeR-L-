from random import random
from player import Player
from RoguePy.UI import Elements
from UiElements import MyMapElement
from UiElements import HelpElement
from Item.itemtypes import *
from Terrain.terrains import lava
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class PlayState(GameState):

  def __init__(self, name, manager, ui):
    super(PlayState, self).__init__(name, manager, ui)
    self.torchTicks = 100
    self.msgTtl = 100.0

    self.cave = None

    self.player = Player()
    self.player.setChar('@')
    self.player.setColor(libtcod.white)
    self.player.collectPick(SteelPick)
    self.player.collectArrows(CopperArrow, 20)

    self.ropePath = []

    self.turnTaken = False

    self.ticks = 0

    self.rangedMode = False
    self.shooting = False
    self.targetX = 0
    self.targetY = 0

    self.arrowCoord = None

    self.availableCraftingRecipes = []

    self.messages = []

  def reset(self):
    self.cave = None

    self.player = Player()
    self.player.setChar('@')
    self.player.setColor(libtcod.white)
    self.player.collectPick(SteelPick)
    self.player.collectArrows(CopperArrow, 20)

    self.ropePath = []

    self.turnTaken = False

    self.ticks = 0

    self.rangedMode = False
    self.shooting = False
    self.targetX = 0
    self.targetY = 0

    self.arrowCoord = None

    self.availableCraftingRecipes = []
    self.messages = []


  def tick(self):
    if self.player.dead():
      self.doDeathState()
    if self.shooting:
      self.updateArrowPath()
    ########
    # Non-turn-based updates
    self.ticks += 1
    if not self.ticks % self.torchTicks:
      self.player.torchStrength = max(2, self.player.torchStrength - 1)
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
          if e.attacking():
            dmg = e.aiAttack()
            if dmg:
              self.addMessage(e.name + " hit you for [" + str(dmg) + "] damage.", libtcod.dark_red)
            else:
              self.addMessage("You dodged the the attack")
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
      'toggleRanged': {
        'key': libtcod.KEY_KP0,
        'ch': None,
        'fn': self.toggleRanged
      },
      'fireBow': {
        'key': libtcod.KEY_KPENTER,
        'ch': None,
        'fn': self.fireBow
      },
      'toggleHelp': {
        'key': None,
        'ch': '?',
        'fn': self.helpToggle
      },
      'quit': {
        'key': libtcod.KEY_ESCAPE,
        'ch': None,
        'fn': self.quitToggle
      }
    })
    self.helpModal.setInputs({
      'helpBackEsc': {
        'key': libtcod.KEY_ESCAPE,
        'ch': None,
        'fn': self.helpToggle
      },
      'helpBackQ': {
        'key': None,
        'ch': '?',
        'fn': self.helpToggle
      },
      'helpTabs': {
        'key': libtcod.KEY_TAB,
        'ch': None,
        'fn': self.helpElement.cycleTabs
      },
    })

    self.quitConfirm.setInputs({
      'quitBack': {
        'key': libtcod.KEY_ESCAPE,
        'ch': None,
        'fn': self.quitToggle
      },
      'quit': {
        'key': libtcod.KEY_ENTER,
        'ch': None,
        'fn': self.quit
      }
    })

    ########
    # Inventory/Crafting-specific inputs
    self.craftingModal.setInputs({
      'closeModalTab': {
        'key': libtcod.KEY_TAB,
        'ch': None,
        'fn': self.toggleCrafting
      },
      'closeModalEsc': {
        'key': libtcod.KEY_ESCAPE,
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
    
    self.craftingMenu.setInputs({
      'craftUpArrow': {
        'key': libtcod.KEY_UP,
        'ch': None,
        'fn': self.scrollCraftingUp
      },
      'craftDnArrow': {
        'key': libtcod.KEY_DOWN,
        'ch': None,
        'fn': self.scrollCraftingDown
      },
      'craftUpKP': {
        'key': libtcod.KEY_KP8,
        'ch': None,
        'fn': self.scrollCraftingUp
      },
      'craftDnKP': {
        'key': libtcod.KEY_KP2,
        'ch': None,
        'fn': self.scrollCraftingDown
      },
      'craftEnterKP': {
        'key': libtcod.KEY_KPENTER,
        'ch': None,
        'fn': self.craftingMenu.selectFn
      },
      'craftEnter': {
        'key': libtcod.KEY_ENTER,
        'ch': None,
        'fn': self.craftingMenu.selectFn
      },

    })
    self.messageBox.setInputs({
      'addMsg': {
        'key': None,
        'ch': 'm',
        'fn': self.msgTest
      }
    })

  def msgTest(self):
    self.addMessage("You pressed M", libtcod.dark_red)
    print "Added message"






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
    panelX = self.view.width - 19
    panelW = 18
    panelH = 11
    panelY = self.view.height - (panelH + 1)

    self.statPanelRight = self.mapElement.addElement(Elements.Element(panelX, panelY, panelW, panelH)) \
      .setDefaultColors(libtcod.light_azure, libtcod.azure)
    self.statPanelRight.bgOpacity = 0
    
    hpLabel = self.statPanelRight.addElement(Elements.Label(5, 0, 'HP'))
    hpLabel.bgOpacity = 0
    hpLabel.setDefaultForeground(libtcod.green)

    self.hpBar = self.statPanelRight.addElement(Elements.Bar(8, 0, 10))
    self.hpBar.setMinColor(libtcod.dark_red)
    self.hpBar.setMaxColor(libtcod.dark_green)
    self.hpBar.setMin(0)
    self.hpBar.setMax(self.player.maxHealth)
    self.hpBar.setVal(self.player.health)

    pickLabel = self.statPanelRight.addElement(Elements.Label(3, 2, 'Pick'))
    pickLabel.bgOpacity = 0
    pickLabel.setDefaultForeground(libtcod.dark_green)
    
    self.pickBar = self.statPanelRight.addElement(Elements.Bar(8, 2, 10))
    self.pickBar.setMinColor(libtcod.dark_red)
    self.pickBar.setMaxColor(libtcod.dark_green)
    self.pickBar.setMin(0)
    self.pickBar.setMax(self.player.maxPickStrength)
    self.pickBar.setVal(self.player.pickStrength)

    self.ropeLabel = self.statPanelRight.addElement(Elements.Label(3, 4, 'Rope'))
    self.ropeLabel.bgOpacity = 0
    self.ropeLabel.setDefaultForeground(libtcod.dark_green)

    self.anchorLabel = self.statPanelRight.addElement(Elements.Label(0, 6, 'Anchors'))
    self.anchorLabel.bgOpacity = 0
    self.anchorLabel.setDefaultForeground(libtcod.silver)

    tabLabel = self.statPanelRight.addElement(Elements.Label(5, 8, 'TAB Inv/Craft'))
    tabLabel.bgOpacity = 0
    tabLabel.setDefaultForeground(libtcod.yellow)

    helpLabel = self.statPanelRight.addElement(Elements.Label(12, 10, '?-Help'))
    helpLabel.bgOpacity = 0
    helpLabel.setDefaultForeground(libtcod.light_yellow)

    self.statPanelLeft = self.mapElement.addElement(Elements.Element(1, self.view.height - 5, panelW, 4)) \
      .setDefaultColors(libtcod.light_azure, libtcod.azure)
    self.statPanelLeft.bgOpacity = 0

    self.playerCoord = self.statPanelLeft.addElement(Elements.Label(0, 0, ""))
    self.playerMeleeStat = self.statPanelLeft.addElement(Elements.Label(0, 2, "")).setDefaultColors(libtcod.dark_green)
    self.playerRangedStat = self.statPanelLeft.addElement(Elements.Label(0, 3, "")).setDefaultColors(libtcod.dark_green)


    ########
    # Set up crafting/inventory modal elements
    modalW = 23
    modalH = 23

    modalX = (self.view.width - modalW) / 2
    modalY = (self.view.height -modalH) / 2
    sharedTl = libtcod.CHAR_TEEE
    sharedTr = libtcod.CHAR_TEEW

    self.craftingModal = self.view.addElement(Elements.Modal(0, modalY, self.view.width, modalH))
    self.craftingModal.bgOpacity = 0.7

    # Inventory
    self.invFrame = self.craftingModal.addElement(Elements.Frame(modalX, 0, modalW, 10)).setTitle('Inventory')
    self.invList = self.invFrame.addElement(Elements.List(1, 1, modalW - 2, 8))
    self.invList.bgOpacity = 0

    # Crafting
    self.craftFrame = self.craftingModal.addElement(Elements.Frame(modalX, 9, modalW, modalH - 9)).setTitle('Craft')
    self.craftFrame._chars['tl'] = sharedTl
    self.craftFrame._chars['tr'] = sharedTr

    self.itemLabel = self.craftFrame.addElement(Elements.Label(2, 1, "Item"))
    self.itemLabel.bgOpacity = 0
    self.recipeLabel = self.craftFrame.addElement(Elements.Label(12, 1, "Recipe"))
    self.recipeLabel.bgOpacity = 0

    self.craftingMenuMaxHeight = 11

    self.craftingMenu = self.craftFrame.addElement(Elements.Menu(1, 2, 7, self.craftingMenuMaxHeight))
    self.craftingMenu.bgOpacity = 0.5
    self.craftingRecipe1 = self.craftFrame.addElement(Elements.List(8, 2, 7, self.craftFrame.height - 3))
    self.craftingRecipe1.bgOpacity = 0
    self.craftingRecipe2 = self.craftFrame.addElement(Elements.List(15, 2, 7, self.craftFrame.height - 3))
    self.craftingRecipe2.bgOpacity = 0

    # Set colors, now that everything is in place
    self.invFrame.setDefaultColors(libtcod.lightest_azure, libtcod.darkest_azure, True)
    self.craftFrame.setDefaultColors(libtcod.lightest_azure, libtcod.darkest_azure, True)

    # self.craftingMenu.setDefaultColors(libtcod.white)
    self.itemLabel.setDefaultColors(libtcod.yellow)
    self.recipeLabel.setDefaultColors(libtcod.lighter_yellow)

    self.craftingRecipe1.setDefaultColors(libtcod.grey)
    self.craftingRecipe2.setDefaultColors(libtcod.grey * 0.8)

    self.invList.setDefaultColors(libtcod.dark_green)

    noRoomText = "No room in inventory"
    noRoomW = len(noRoomText)
    noRoomX = (modalW - noRoomW) / 2

    self.noRoomLabel = self.craftFrame.addElement(Elements.Label(noRoomX, 0, noRoomText))
    self.noRoomLabel.setDefaultColors(libtcod.dark_red)
    self.noRoomLabel.hide()
    # end crafting
    ########

    self.helpElement = HelpElement(self.view)
    self.helpModal = Elements.Modal(0, 0, self.view.width, self.view.height)

    self.view.addElement(self.helpModal)
    self.helpModal.addElement(self.helpElement)

    ########
    # Ranged mode

    # The overlay containing our crosshair
    self.rangedOverlay = self.mapElement.addElement(Elements.Element(0, 0, self.cave.width, self.mapElement.height))
    # We only want to display the "+" char, and not disturb the map underneath
    self.rangedOverlay.bgOpacity = 0
    # Override the draw method, so we can easily draw our "+"
    self.rangedOverlay.draw = self.drawOverlay

    # Cell info shown, when in ranged mode
    self.cellInfoFrame = self.view.addElement(Elements.Element(self.view.width - 15, self.statPanelRight.y - 4, 14, 4))
    self.cellInfoFrame.bgOpacity = 0.2
    self.cellInfoTerrain = self.cellInfoFrame.addElement(Elements.Text(0, 0, 14, 1))
    self.cellInfoTerrain.bgOpacity = 0
    self.cellInfoEntities = self.cellInfoFrame.addElement(Elements.List(0, 1, 14, 3))
    self.cellInfoEntities.bgOpacity = 0

    self.cellInfoFrame.setDefaultColors(libtcod.light_azure, libtcod.darker_azure, True)
    self.cellInfoFrame.hide()
    ########
    # Rope indicator
    ropeIndicator = "[TIED IN]"
    ropeX = (self.view.width - len(ropeIndicator)) / 2
    ropeY = self.view.height - 2
    self.ropeIndicator = self.view.addElement(Elements.Label(ropeX, ropeY, ropeIndicator))
    self.ropeIndicator.setDefaultColors(libtcod.lightest_azure, libtcod.darker_red)
    self.ropeIndicator.hide()
    ########
    # Quit popup
    quitStr =  "Those rumours won't prove themselves..."
    quitCmds = " <ESC> Back               <Enter> Quit "
    quitW = len(quitStr) + 2
    quitX = (self.view.width - quitW) / 2
    quitH = 3
    quitY = (self.view.height - quitH) / 2

    really = "Really Quit?"
    reallyW = len(really)
    reallyX = (quitW - reallyW) / 2
    reallyY = 0

    self.quitConfirm = self.view.addElement(Elements.Modal(quitX, quitY, quitW, quitH))
    quitFrame = self.quitConfirm.addElement(Elements.Frame(0, 0, quitW, quitH)).setDefaultColors(libtcod.dark_red)
    quitFrame.addElement(Elements.Label(reallyX, reallyY, really)).setDefaultColors(libtcod.light_red)
    quitText = quitFrame.addElement(Elements.Label(1, 1, quitStr))
    escEnter = quitFrame.addElement(Elements.Label(1, 2, quitCmds))
    escEnter.setDefaultColors(libtcod.light_red)
    escEnter.bgOpacity = 0
    ########
    # Message list
    msgW = self.view.width / 3
    msgX = (self.view.width - msgW) / 2
    msgH = 5
    msgY = self.view.height - 8

    self.messageBox = Elements.Element(msgX, msgY, msgW, msgH)
    self.messageBox.bgOpacity = 0
    self.messageElements = [self.messageBox.addElement(Elements.Text(0, y, msgW, msgH)) for y in range(msgH)]

    self.view.addElement(self.messageBox)

  def addMessage(self, message, color=libtcod.white):
    self.messages.insert(0, {'msg': message, 'ttl': self.msgTtl, 'clr': color})
    if len(self.messages) > len(self.messageElements):
      index = len(self.messageElements) - len(self.messages)
      self.messages = self.messages[:index]

  def removeMessage(self, message):
    if message in self.messages:
      self.messages.remove(message)
      return True
    else:
      return False

  def updateMessages(self):
    # We'll always have a full compliment of messageElements, they just may be blank
    height = len(self.messageElements)

    # The number of messages we'll be displaying
    count = len(self.messages)

    for y in range(height):
      _y = (height-1) - y
      el = self.messageElements[_y]
      if y < count:
        msg = msg = self.messages[y]
        msg['ttl'] -= 1
        opacity = max(0, msg['ttl'] / self.msgTtl)
        el.setText(msg['msg'])
        el.setDefaultColors(msg['clr'])
        el.fgOpacity = opacity
      else:
        el.setText('')

    self.messages = [msg for msg in self.messages if msg['ttl'] > 0]






  def drawOverlay(self):
    con = self.rangedOverlay.console
    onScreen = self.mapElement.onScreen(self.targetX, self.targetY)
    libtcod.console_put_char_ex(con, onScreen[0], onScreen[1], '+', libtcod.yellow, libtcod.black)

  ########
  # State transitions
  def doDeathState(self):
    self._manager.setNextState('Death')

  def quitToggle(self):
    if self.quitConfirm.visible:
      self.quitConfirm.hide(self.view)
    else:
      self.quitConfirm.show(self.view)

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
            dmg = self.player.defAttack(e)
            if dmg:
              self.addMessage("You hit " + e.name + " for [" + str(dmg) + "] damage.", libtcod.dark_green)
            else:
              self.addMessage(e.name + " dodged the the attack")
            if e.dead():
              self.addMessage("You killed the " + e.name, libtcod.green)
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
            self.addMessage("Picked up " + i.name, libtcod.dark_yellow)
            newCell.removeEntity(i)
        except ValueError:
          pass

      # Update the player object's internal representation of its location
      playerFunc()

      # Place the player in the new cell
      self.cave.addEntity(self.player, self.player.x, self.player.y)

  def ropeToggle(self):
    if self.rangedMode:
      return
    if self.player.attached:
      # Remove the ropes from the cave
      for (x, y) in self.ropePath:
        self.cave.getCell(x, y).removeEntity(Rope)
      self.ropePath = []
      self.player.detach()
      self.ropeIndicator.hide()
      self.player.falling = self.cave.getCell(self.player.x, self.player.y + 1).passable()
    else:
      if self.player.y > 5 and self.player.anchorIn():
        self.ropeIndicator.show()
        self.ropePath.append((self.player.x, self.player.y))
        self.cave.addEntity(Anchor, self.player.x, self.player.y)
        self.cave.addEntity(Rope, self.player.x, self.player.y)
        self.player.dropItem(Rope)

  ########
  # Input handlers
  def mvUp(self) :
    if self.rangedMode:
      self.mvTarget(0, -1)
    else:
      if self.player.falling:
        return
      self.mvPlayer(0, -1, self.player.moveU)

  def mvDn(self) :
    if self.rangedMode:
      self.mvTarget(0, 1)
    else:
      if self.player.falling:
        return
      self.mvPlayer(0, 1, self.player.moveD)

  def mvLft(self) :
    if self.rangedMode:
      self.mvTarget(-1, 0)
    else:
      if self.player.falling:
        return
      self.mvPlayer(-1, 0, self.player.moveL)

  def mvRgt(self) :
    if self.rangedMode:
      self.mvTarget(1, 0)
    else:
      if self.player.falling:
        return
      self.mvPlayer(1, 0, self.player.moveR)

  def mvUpLft(self) :
    if self.rangedMode:
      self.mvTarget(-1, -1)
    else:
      if self.player.falling:
        return
      self.mvPlayer(-1, -1, self.player.moveUL)

  def mvUpRgt(self) :
    if self.rangedMode:
      self.mvTarget(1, -1)
    else:
      if self.player.falling:
        return
      self.mvPlayer(1, -1, self.player.moveUR)

  def mvDnLft(self) :
    if self.rangedMode:
      self.mvTarget(-1, 1)
    else:
      if self.player.falling:
        return
      self.mvPlayer(-1, 1, self.player.moveDL)

  def mvDnRgt(self) :
    if self.rangedMode:
      self.mvTarget(1, 1)
    else:
      if self.player.falling:
        return
      self.mvPlayer(1, 1, self.player.moveDR)

  def mvTarget(self, x, y):
    self.targetX = max(0, min(self.cave.width - 1, self.targetX + x))
    self.targetY = max(0, min(self.cave.height - 1, self.targetY + y))

  def wait(self):
    self.turnTaken = True

  def toggleCrafting(self):
    if not self.craftingModal.visible:
      self.noRoomLabel.hide()
      self.craftingModal.show(self.view)
    else:
      self.craftingModal.hide(self.view)

  def scrollCraftingUp(self):
    self.craftingMenu.selectUp()
    self.craftingRecipe1._offset = self.craftingMenu._offset
    self.craftingRecipe2._offset = self.craftingMenu._offset
    self.noRoomLabel.hide()
  def scrollCraftingDown(self):
    self.craftingMenu.selectDown()
    self.craftingRecipe1._offset = self.craftingMenu._offset
    self.craftingRecipe2._offset = self.craftingMenu._offset
    self.noRoomLabel.hide()

  def craftItem(self, index):
    self.noRoomLabel.hide()
    recipe = self.availableCraftingRecipes[index]
    inInv = self.player.inventory.count(recipe['item'])
    if inInv >= recipe['item'].maxInv:
      self.noRoomLabel.show()
      return

    if 'dontDrop' in recipe:
      dontDrop = recipe['dontDrop']
    else:
      dontDrop = []
    for i in recipe['recipe']:
      if i not in dontDrop:
        self.player.dropItem(i)
    recipe['item'].collect(self.player)
    self.craftingMenu._offset = 0
    self.craftingMenu.selected = 0
    self.craftingRecipe1._offset = 0
    self.craftingRecipe2._offset = 0
    self.invList._offset = 0


  def toggleRanged(self):
    self.rangedMode = not self.rangedMode
    if self.rangedMode:
      self.targetX = self.player.x
      self.targetY = self.player.y

  def fireBow(self):
    if not self.rangedMode:
      return
    self.turnTaken = True
    self.rangedMode = False

    if not (Bow in self.player.inventory and Arrow in self.player.inventory):
      return
    self.player.dropItem(Arrow)

    self.shooting = True
    print "initing line", self.player.x, self.player.y, self.targetX, self.targetY
    libtcod.line_init(self.player.x, self.player.y, self.targetX, self.targetY)


  def updateArrowPath(self):
    if self.arrowCoord:
      (x, y) = self.arrowCoord
      cell = self.cave.getCell(x,y)
      if Arrow in cell.entities:
        cell.removeEntity(Arrow)

    (newX, newY) = libtcod.line_step()
    if newX is None:
      self.shooting = False
      return

    cell = self.cave.getCell(newX, newY)
    # Stop if we hit something
    if not(cell.passable()):
      self.shooting = False

    self.cave.addEntity(Arrow, newX, newY)
    self.arrowCoord = (newX, newY)


    for e in self.cave.enemies:
      if e.x == newX and e.y == newY:
        dmg = self.player.dexAttack(e)
        if dmg:
          self.addMessage("You hit " + e.name + " for [" + str(dmg) + "] damage.", libtcod.dark_green)
        else:
          self.addMessage(e.name + " dodged the the attack")
        if e.dead():
          self.addMessage("You killed the " + e.name, libtcod.green)
          if e.drops:
            rnd = random()
            if rnd <= e.dropChance:
              self.cave.addEntity(e.drops, e.x, e.y)
          self.cave.removeEnemy(e)
        return True

  def helpToggle(self):
    if not self.helpModal.visible:
      self.helpModal.show(self.view)
    else:
      self.helpModal.hide(self.view)

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

    if self.craftingModal.visible:
      self.updateCraftingUI()
      return

    self.updateMessages()

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
    self.ropeLabel.setDefaultForeground(libtcod.lighter_crimson)

    self.anchorLabel.setLabel("Anchors " + str(self.player.inventory.count(Anchor)))
    self.anchorLabel.bgOpacity = 0
    self.anchorLabel.setDefaultForeground(libtcod.silver)

    self.playerCoord.setLabel(str((self.player.x, self.player.y)))
    self.playerCoord.setDefaultColors(libtcod.silver).bgOpacity = 0
    self.playerMeleeStat.setLabel("Melee:" + str(self.player.meleeMultiplier))
    self.playerMeleeStat.setDefaultColors(libtcod.darker_green).bgOpacity = 0
    self.playerRangedStat.setLabel("Range:" + str(self.player.rangeMultiplier))
    self.playerRangedStat.setDefaultColors(libtcod.darker_green).bgOpacity = 0



    if self.rangedMode:
      self.rangedOverlay.show()
      self.cellInfoFrame.show()
      self.cellInfoUpdate()
    else:
      self.rangedOverlay.hide()
      self.cellInfoFrame.hide()

  def cellInfoUpdate(self):
    cellTerrain = "???"
    entities = []
    if self.mapElement.explored(self.targetX, self.targetY):
      cell = self.cave.getCell(self.targetX, self.targetY)
      cellTerrain = cell.terrain.desc
      for e in cell.entities:
        entities.append(e.name)
      self.cellInfoEntities.setItems(entities)

    self.cellInfoTerrain.setText(cellTerrain)

  def updateCraftingUI(self):
    invDict = {}
    for i in self.player.inventory:
      key = i.name
      if key not in invDict:
        invDict[key] = 0
      invDict[key] += 1
    invList = [self.genInvLabel(itemName, invDict[itemName]) for itemName in invDict]
    self.invList.setItems(invList)

    craftMenuItems = []

    self.availableCraftingRecipes = filter(self.filterCraftables, recipes)

    list1 = []
    list2 = []
    i = 0
    for recipe in self.availableCraftingRecipes:
      menuItem = {recipe['item'].name: self.craftItem}
      craftMenuItems.append(menuItem)
      r = recipe['recipe']
      list1.append(r[0].name)
      if len(r) > 1:
        list2.append(r[1].name)
      else:
        list2.append('n/a')
    self.craftingMenu.setItems(craftMenuItems)

    if len(craftMenuItems) > self.craftingMenu.height:
      self.craftingMenu.height = min(self.craftingMenuMaxHeight, len(craftMenuItems))
    else:
      self.craftingMenu.height = len(craftMenuItems)
    self.craftingMenu.setDefaultColors(libtcod.lightest_azure, libtcod.darkest_azure)


    self.craftingRecipe1.setItems(list1)
    self.craftingRecipe2.setItems(list2)




  def filterCraftables(self, recipe):
    recipe = recipe['recipe']
    for item in recipe:
      recipeCount = recipe.count(item)
      invCount = self.player.inventory.count(item)
      if not invCount >= recipeCount:
        return False
    return True


  def genInvLabel(self, str1, str2):
    str1 = str(str1)
    str2 = str(str2)
    countLen = len(str2)
    labelLen = len(str1)
    spaces = self.invList.width - (labelLen + countLen)
    space = ""
    for s in range(spaces):
      space += " "
    return str1 + space + str2


    # invDict = {}
    # for i in self.player.inventory:
    #   key = i.name
    #   if key not in invDict:
    #     invDict[key] = 0
    #   invDict[key] += 1
    # invList = map(lambda key: key + ": " + str(invDict[key]),invDict)
    # self.invList.setItems(invList)





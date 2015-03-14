from RoguePy.State.GameState import GameState
from RoguePy.libtcod import libtcod
from RoguePy.UI import Elements

class VictoryState(GameState):
  def __init__(self, name, manager, ui):
    super(VictoryState, self).__init__(name, manager, ui)
    self._setupView()
    self._setupInputs()
    self.step = 0

  def _setupView(self):
    pressAny = self.view.addElement(Elements.Label(self.view.width - 18, self.view.height - 1, "Press any key..."))

    congrats = "CONGRATULATIONS!"
    conW = len(congrats)
    conX = (self.view.width - conW) / 2
    conY = self.view.height / 2 - 2

    congratulationsLabel = Elements.Label(conX, conY, congrats)
    congratulationsLabel.setDefaultColors(libtcod.gold)
    self.view.addElement(congratulationsLabel)

    storyText = Elements.Text(self.view.width / 4, conY + 2, self.view.width / 2, 3,
      "Climbing to the surface, with the Dragon Scale in hand, you feel it would be hard for MineCorp to deny " + \
      "the rumours any more.").setDefaultColors(libtcod.silver)

    hero = "You are a true hero."
    heroX = (self.view.width - len(hero)) / 2
    heroY = conY + 6

    heroLabel = Elements.Label(heroX, heroY, hero).setDefaultColors(libtcod.green)
    heroLabel.hide()
    
    still = "Still though. Would have been nice if there had been a treasure. :("
    
    stillX = (self.view.width - len(still)) / 2
    stillY = heroY + 2
    stillLabel = Elements.Label(stillX, stillY, still).setDefaultColors(libtcod.grey)
    stillLabel.hide()
    
    self.frames = [
      self.view.addElement(storyText),
      self.view.addElement(heroLabel),
      self.view.addElement(stillLabel)
    ]



  def _setupInputs(self):
    self.view.setInputs({
      'proceed': {
        'key': 'any',
        'ch': None,
        'fn': self.proceed
      }
    })
    pass


  def proceed(self):
    self.step += 1
    if self.step < len(self.frames):
      self.frames[self.step].show()
    else:
      menu = self._manager.getState('Menu')
      menu.reset()
      self._manager.setNextState('Menu')

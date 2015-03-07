from RoguePy.UI import Elements
from RoguePy.State.GameState import GameState

class StoryState(GameState):

  def __init__(self, name, manager, ui):
    super(StoryState, self).__init__(name, manager, ui)
    self._setupView()
    self._setupInputs()

    self.step = 0



  def tick(self):
    print "Title"


  def _setupView(self):
    pressAny = self.view.addElement(Elements.Label(self.view.width - 18, self.view.height - 1, "Press any key..."))

    storyText1 = Elements.Text(self.view.width / 4, 15, self.view.width / 2, 4, \
      "Decades after a devastating explosion rocked the mine in your small hometown, rumours have been spreading. " + \
      "Some of the old minors say the explosion wasn't an accident, that it was set deliberately by MineCorp to " + \
      "cover up a terrifying truth.")
    storyText2 = Elements.Text(self.view.width / 4, 20, self.view.width / 2, 4, \
      "They say MineCorp got too greedy - dug too deep - in their search for the diamonds found down below, and " + \
      "unleashed  a terrible evil that lurks in the darkest depth of the mine.")
    storyText3 = Elements.Text(self.view.width / 4, 25, self.view.width / 2, 4, \
      "The sole survivor of the catastrophe - an old recluse, these days, hardly seen by anyone - was said to speak " + \
      "of monsters in the depths of the mine. People around town speak in hushed tones of an even greater treasure " + \
      "guarded by the beasts in the deepest, darkest depths of the old mine.")
    storyText4 = Elements.Text(self.view.width / 4, 30, self.view.width / 2, 4, \
      "Grabbing an old pick from the mining museum, and a handful of rock climbing supplies, you set out to reach " + \
      "the depths of the old mine, and determine once and for all the truth about the rumours.")

    storyText2.hide()
    storyText3.hide()
    storyText4.hide()

    self.frames = [
      self.view.addElement(storyText1),
      self.view.addElement(storyText2),
      self.view.addElement(storyText3),
      self.view.addElement(storyText4),
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

    print "proceeding from : " + str(self.step)
    self.step += 1
    if self.step < len(self.frames):
      self.frames[self.step].show()
    else:
      self._manager.setNextState('Menu')

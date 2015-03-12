from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod
from RoguePy.State.GameState import GameState

class AboutState(GameState):
  def __init__(self, name, manager, ui):
    super(AboutState, self).__init__(name, manager, ui)
    self._setupView()

  def tick(self):
    self._manager.setNextState('Menu')

  def _setupView(self):
    x = self.view.width / 4
    y = self.view.height / 3 - 1
    w = self.view.width / 2
    h = self.view.height / 3 + 2
    self.frame = self.view.addElement(Elements.Frame(x, y, w, h))\
      .setDefaultColors(libtcod.azure, libtcod.darkest_azure)

    titleItems = [
      "MineClimbeR(L)",
      "Written by Jeff Ripley",
      "March 2015"
    ]

    innerW = w - 2
    innerH = h - 2
    i = 0
    for item in titleItems:
      l = len(item)
      x = (innerW - l) / 2
      y = 1 + i
      label = self.frame.addElement(Elements.Label(x, y, item))
      label.bgOpacity = 0
      i += 1

    aboutText =\
      "Built using my as-yet unreleased libtcod framework, RoguePy.\n\n" + \
      "This is the first project I've undertaken, other than tech demos, with the RoguePy framework " + \
      "and, while it's been quite useful, and saved me lots of time, I've  come across many shortcomings, " + \
      "where I've needed to insert my own class to provide the functionality I've needed to make a worthwhile " + \
      "game.\n\n" + \
      "I'm looking forward to adding these features to the framework before release time.\n\n" + \
      "Watch https://github.com/v4nz666/RoguePy for updates."

    self.aboutText = self.frame.addElement(Elements.Text(1, len(titleItems) + 2, innerW, innerH))
    self.aboutText.setText(aboutText)
    self.aboutText.setDefaultForeground(libtcod.lightest_azure)
    self.aboutText.bgOpacity = 0

    # Cascade to all child elements

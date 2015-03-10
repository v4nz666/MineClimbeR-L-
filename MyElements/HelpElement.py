from helpContents import *
from RoguePy.UI import Elements
from RoguePy.libtcod import libtcod

class HelpElement(Elements.Element):
  def __init__(self, view):
    x = view.width / 4
    y = view.height / 3
    w = view.width / 2
    h = view.height / 3 + 1
    innerW = w - 2
    innerH = h - 2
    super(HelpElement, self).__init__(x, y, w, h)

    self.selectedTab = 0

    self.frame = self.addElement(Elements.Frame(0, 0, w, h))
    self.tabLabels = [
      self.frame.addElement(Elements.Label(1, 1, "General")),
      self.frame.addElement(Elements.Label(15, 1, "Basics")),
      self.frame.addElement(Elements.Label(28, 1, "Climbing")),
      self.frame.addElement(Elements.Label(43,1, "Crafting"))
    ]
    self.tabs = [
      self.frame.addElement(Elements.Text(1, 2, innerW, innerH-1, generalText))\
        .setDefaultColors(libtcod.azure, libtcod.darkest_grey),
      self.frame.addElement(Elements.Text(1, 2, innerW, innerH-1, basicsText))\
        .setDefaultColors(libtcod.light_yellow, libtcod.darkest_green),
      self.frame.addElement(Elements.Text(1, 2, innerW, innerH-1, climbingText))\
        .setDefaultColors(libtcod.white, libtcod.darkest_azure),
      self.frame.addElement(Elements.Text(1, 2, innerW, innerH-1, craftingText))\
        .setDefaultColors(libtcod.white, libtcod.darkest_crimson),
    ]

    self.helpLabel = self.addElement(Elements.Label(5, h - 1, "TAB:NEXT                        ESC:BACK"))
    self.helpLabel.bgOpacity = 0

  def cycleTabs(self):
    self.selectedTab += 1
    if self.selectedTab >= len(self.tabLabels):
      self.selectedTab = 0

  def draw(self):
    for i in range(len(self.tabs)):
      if i == self.selectedTab:
        self.tabLabels[i].setDefaultForeground(libtcod.white)
        self.tabs[i].show()
      else:
        self.tabLabels[i].setDefaultForeground(libtcod.grey)
        self.tabs[i].hide()

    super(HelpElement, self).draw()
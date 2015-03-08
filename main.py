from States import *
from RoguePy import setFps
from RoguePy.libtcod import libtcod
from RoguePy.State import StateManager
from RoguePy.UI.UI import UI

FPS = 60
UI_WIDTH = 105
UI_HEIGHT = 60
UI_FS = True


setFps(FPS)

ui = UI()
ui.init(UI_WIDTH, UI_HEIGHT, UI_FS)

# TODO: enable
libtcod.console_credits()

stateManager = StateManager()

s_Title = TitleState('Title', stateManager, ui)
s_Menu = MenuState('Menu', stateManager, ui)
s_Story = StoryState('Story', stateManager, ui)
s_WorldGen = WorldGenState('WorldGen', stateManager, ui)
s_Play = PlayState('Play', stateManager, ui)
s_Victory = VictoryState('Victory', stateManager, ui)
s_Death = DeathState('Death', stateManager, ui)

s_Help = HelpState('Help', stateManager, ui)
s_About = AboutState('About', stateManager, ui)

s_Quit = QuitState('Quit', stateManager, ui)

stateManager.addState(s_Title).setBlocking(True)
stateManager.addState(s_Menu).setBlocking(True)
stateManager.addState(s_Story).setBlocking(True)
stateManager.addState(s_WorldGen).setBlocking(True)
stateManager.addState(s_Play).setBlocking(True)
stateManager.addState(s_Victory).setBlocking(True)
stateManager.addState(s_Death).setBlocking(True)
stateManager.addState(s_Help).setBlocking(True)
stateManager.addState(s_About).setBlocking(True)
stateManager.addState(s_Quit)

stateManager.setCurrentState('Title')

while not ui.is_closed():
  stateManager.doTick()

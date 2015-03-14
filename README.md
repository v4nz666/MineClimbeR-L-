# MineClimbeR(L)

2015 7DRL Entry  
Jeff Ripley

--


Decades after a devastating explosion rocked the mine in your small hometown, rumours have been spreading.
Folks say the explosion wasn't an accident, that it was set deliberately by MineCorp to cover up a terrifying truth.

They say MineCorp got too greedy - dug too deep - in their search for the diamonds found down below, and
unleashed  a terrible evil that lurks in the darkest depth of the mine.

The sole survivor of the catastrophe - an old recluse, these days, hardly seen by anyone - was said to speak
of monsters in the depths of the mine. People around town speak in hushed tones of a Great treasure
guarded by the beasts in the deepest, darkest depths of the old mine.

Grabbing an old pick from the mining museum, and a handful of rock climbing supplies, you set out to reach
the depths of the old mine, and determine once and for all the truth about the rumours.

--

### Started 2:00PM AST Saturday Mar 7th, 2015

## Gameplay Features

Short gameplay teaser available at http://youtu.be/XO8oqFJ9gUg

- Side view, gravity-driven mine exploration
- Turn-based combat mechanics, but torch burns down in real time
- Rock climbing mechanics - attach ropes to anchors to climb to otherwise inaccessible areas of the mine
- Simple crafting mechanic to repair your tools, build new anchors, weapons, arrows,etc
- Ranged / Melee combat
- Damage / "health" multipliers for materials used during crafting - Tin, Copper, Bronze, Iron, Steel, Diamond
 
## Getting started/Installation:
To run the game, on Linux, at least for now (pre-packaged binaries to come - hopefully for windows/mac, too) simply clone this repository with the --recursive flag to pull in the RoguePy submodule:

    git clone --recursive git@github.com:v4nz666/MineClimbeR-L-.git

pygame is required for the audio

    pip install pygame

and run the game with:

    python main.py
  
## Tips and tricks

- Your torch burns down in real-time, whether you've taken a turn, or not. This includes in the inventory/crafting menu. Don't dilly dally! You'll want to replenish your torch light, periodically, through the crafting menu (TAB).
- Be very careful digging down in any way (straight down, or diagonally). You're likely to fall to your death.
- Always clip in (space bar) before moving, if you don't know what's below your destination tile.
- Ranged attacks can help you keep a distance from your enemies, and can save you some much needed HP. Press the 0 key on the numpad to aim your bow (and again to cancel your shot), and the Enter key on the numpad to fire.

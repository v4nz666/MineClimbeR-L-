from RoguePy.libtcod import libtcod
from RoguePy.Map.Terrain import Terrain

openAir = Terrain(True, True, "Open Air").setColors(libtcod.white, libtcod.lighter_blue)
openMine = Terrain(True, True, "Open Mine").setColors(libtcod.white, libtcod.light_grey)

openWoodPost = Terrain(True, False, "Wooden Post").setColors(libtcod.dark_orange, libtcod.lighter_blue)
openWoodBeam = Terrain(True, False, "Wooden Beam").setColors(libtcod.dark_orange, libtcod.lighter_blue)
caveWoodPost = Terrain(True, False, "Wooden Post").setColors(libtcod.dark_orange, libtcod.light_grey)
caveWoodBeam = Terrain(True, False, "Wooden Beam").setColors(libtcod.dark_orange, libtcod.light_grey)

caveWall = Terrain(False, False, "Rock Wall").setColors(libtcod.darkest_grey, libtcod.darkest_grey)

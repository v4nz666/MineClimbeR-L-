from RoguePy.libtcod import libtcod
from Terrain.MyTerrain import MyTerrain

openAir = MyTerrain(True, True, "Open Air").setColors(libtcod.white, libtcod.lighter_blue)
openMine = MyTerrain(True, True, "Open Mine").setColors(libtcod.white, libtcod.light_grey)

openWoodPost = MyTerrain(True, False, "Wooden Post").setColors(libtcod.dark_orange, libtcod.lighter_blue)
openWoodBeam = MyTerrain(True, False, "Wooden Beam").setColors(libtcod.dark_orange, libtcod.lighter_blue)
caveWoodPost = MyTerrain(True, False, "Wooden Post").setColors(libtcod.dark_orange, libtcod.light_grey)
caveWoodBeam = MyTerrain(True, False, "Wooden Beam").setColors(libtcod.dark_orange, libtcod.light_grey)

caveWall = MyTerrain(False, False, "Rock Wall").setColors(libtcod.darkest_grey, libtcod.darker_grey)

from RoguePy.libtcod import libtcod
from Terrain.MyTerrain import MyTerrain
from Item.itemTypes import Wood

openAir = MyTerrain(True, True, "Open Air").setColors(libtcod.white, libtcod.lighter_blue)
openMine = MyTerrain(True, True, "Open Mine").setColors(libtcod.white, libtcod.light_grey)

openWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_DVLINE)\
  .drops(Wood)
openWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_DHLINE)\
  .drops(Wood)
caveWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_DVLINE)\
  .drops(Wood)
caveWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_DHLINE)\
  .drops(Wood)

caveWall = MyTerrain(False, False, "Rock Wall").setColors(libtcod.darkest_grey, libtcod.darker_grey)

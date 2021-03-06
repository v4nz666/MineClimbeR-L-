from RoguePy.libtcod import libtcod
from Terrain.myterrain import MyTerrain
from Item.itemtypes import Wood

openAir = MyTerrain(True, True, "Open Air").setColors(libtcod.white, libtcod.lighter_blue)
openMine = MyTerrain(True, True, "Open Mine").setColors(libtcod.white, libtcod.light_grey)

openBurningWood = MyTerrain(False, False, "Burning Wood")\
  .setColors(libtcod.dark_flame, libtcod.lighter_blue)\
  .setChar("#")\
  .digs(openAir)
caveBurningWood = MyTerrain(False, False, "Burning Wood")\
  .setColors(libtcod.dark_flame, libtcod.light_grey)\
  .setChar("#")\
  .digs(openAir)

dugOpenWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_VLINE)\
  .digs(openAir)\
  .burns(openBurningWood)\
  .drops(Wood)
openWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_DVLINE)\
  .burns(openBurningWood)\
  .digs(dugOpenWoodPost)

dugOpenWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_HLINE)\
  .digs(openAir)\
  .burns(openBurningWood)\
  .drops(Wood)
openWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_DHLINE)\
  .digs(dugOpenWoodBeam)\
  .burns(openBurningWood)

dugWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_VLINE)\
  .digs(openMine)\
  .drops(Wood)\
  .burns(caveBurningWood)
caveWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_DVLINE)\
  .digs(dugWoodPost)\
  .burns(caveBurningWood)

dugWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_HLINE)\
  .digs(openMine)\
  .drops(Wood)\
  .burns(caveBurningWood)
caveWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_DHLINE)\
  .digs(dugWoodBeam)\
  .burns(caveBurningWood)

dugCaveWall = MyTerrain(False, False, "Rock Wall")\
  .setColors(libtcod.darkest_grey, libtcod.darker_grey)\
  .setChar(libtcod.CHAR_BLOCK2)\
  .digs(openMine)
caveWall = MyTerrain(False, False, "Rock Wall")\
  .setColors(libtcod.darkest_grey, libtcod.darker_grey)\
  .digs(dugCaveWall)

lava = MyTerrain(False, True, "Lava Pool")\
  .setColors(libtcod.light_flame, libtcod.orange)\
  .setChar('~')
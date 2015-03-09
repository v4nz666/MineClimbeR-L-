from RoguePy.libtcod import libtcod
from Terrain.MyTerrain import MyTerrain
from Item.itemTypes import Wood

openAir = MyTerrain(True, True, "Open Air").setColors(libtcod.white, libtcod.lighter_blue)
openMine = MyTerrain(True, True, "Open Mine").setColors(libtcod.white, libtcod.light_grey)

dugOpenWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_VLINE)\
  .digs(openAir)\
  .drops(Wood)
openWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_DVLINE)\
  .digs(dugOpenWoodPost)
dugOpenWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_HLINE)\
  .digs(openAir)\
  .drops(Wood)
openWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.lighter_blue)\
  .setChar(libtcod.CHAR_DHLINE)\
  .digs(dugOpenWoodBeam)
dugWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_VLINE)\
  .digs(openMine)\
  .drops(Wood)
caveWoodPost = MyTerrain(True, False, "Wooden Post")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_DVLINE)\
  .digs(dugWoodPost)
dugWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_HLINE)\
  .digs(openMine)\
  .drops(Wood)
caveWoodBeam = MyTerrain(True, False, "Wooden Beam")\
  .setColors(libtcod.dark_orange, libtcod.light_grey)\
  .setChar(libtcod.CHAR_DHLINE)\
  .digs(dugWoodBeam)

dugCaveWall = MyTerrain(False, False, "Rock Wall")\
  .setColors(libtcod.darkest_grey, libtcod.darker_grey)\
  .setChar(libtcod.CHAR_BLOCK2)\
  .digs(openMine)
caveWall = MyTerrain(False, False, "Rock Wall")\
  .setColors(libtcod.darkest_grey, libtcod.darker_grey)\
  .digs(dugCaveWall)

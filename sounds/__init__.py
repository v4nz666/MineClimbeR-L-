import pygame.mixer as mixer
import os

path=os.path.dirname(os.path.abspath(__file__))

mixer.init()
mixer.music.load(os.path.join(path, '3158__suonho__suonho-hypersuspance.wav'))

combatHitSound = mixer.Sound(os.path.join(path, 'combatHit.wav'))
combatMissSound = mixer.Sound(os.path.join(path, 'combatMiss.wav'))
craftSound = mixer.Sound(os.path.join(path, 'craft.wav'))
dieSound = mixer.Sound(os.path.join(path, 'die.wav'))
digSound = mixer.Sound(os.path.join(path, 'dig.wav'))
fallSound = mixer.Sound(os.path.join(path, 'fall.wav'))
pickupSound = mixer.Sound(os.path.join(path, 'pickup.wav'))
waterSound = mixer.Sound(os.path.join(path, 'water.wav'))
fireSound = mixer.Sound(os.path.join(path, 'fire.wav'))

sounds = [
  combatHitSound,
  combatMissSound,
  craftSound,
  dieSound,
  digSound,
  fallSound,
  pickupSound,
  waterSound,
  fireSound,
]

def setSoundVolume(val):
  global sounds
  for s in sounds:
    s.set_volume(val)
def getSoundVolume():
  global sounds
  return sounds[0].get_volume()

def setMusicVolume(val):
  mixer.music.set_volume(val)
def getMusicVolume():
  return mixer.music.get_volume()
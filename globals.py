import soundmanager # type: ignore

world = None

maxLevel = 2
lastCompletedLevel = 1
currentLevel = 1

CINZA_ESCURO = (50,50,50)
PRETO = (0,0,0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)

player1 = None
player2 = None
player3 = None
player4 = None
players = []

soundManager = soundmanager.SoundManager()
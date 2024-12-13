import pygame
import globals
import utils

class Level:
    def __init__(self, platforms=None, entities=None, winFunc=None, loseFunc=None, powerupSpawnPoints=None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc # guardar variável
        self.loseFunc = loseFunc # guardar variável
        self.powerupSpawnPoints = powerupSpawnPoints
    def isWon(self):
        if self.winFunc is None:
            return False
        return self.winFunc(self)
    def isLost (self):
        if self.loseFunc is None:
            return False
        return self.loseFunc(self)

# perder caso não existam jogadores vivos
def lostLevel(level):
    # o nível não está perdido caso qualquer jogador possua pelo menos 1 vida
    for entity in level.entities:
        if entity.type == "player":
            if entity.battle is not None:
                if entity.battle.vidas > 0:
                    return False
    # nível perdido
    return True

# vence caso não sobrem moedas
def wonLevel(level):
    # o nível não foi terminado caso sobrem moedas
    for entity in level.entities:
        if entity.type == "collectable":
            return False
    return True

def loadLevel(levelNumber):
    if levelNumber == 1:
        # carregar nível 1
        globals.world = Level(
            platforms = [
                    # meio
                    pygame.Rect(100,300,400,50),
                    # esquerda
                    pygame.Rect(100,250,50,50),
                    # direita
                    pygame.Rect(450,250,50,50),
                    pygame.Rect(0,200,100,50)
            ],
            entities = [
                    utils.makeCoin(105,225), #
                    utils.makeCoin(200,275), # Lista de entidades com 2 moedas
                    utils.makeEnemy(150,291),
                    utils.makePowerup("vida", 400,260),
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel,
            powerupSpawnPoints = [(400,260),(300, 100)]
        )
    if levelNumber == 2:
        # carregar nível 2
        globals.world = Level(
            platforms = [
                    # meio
                    pygame.Rect(100,300,400,50),
            ],
            entities = [
                    utils.makeCoin(105,225), #
            ],
            winFunc = wonLevel,
            loseFunc = lostLevel
        )
    
    # adicionar jogadores
    for player in globals.players:
        globals.world.entities.append(player)
   
    # reíniciar os jogadores
    for entity in globals.world.entities:
        entity.reset(entity)
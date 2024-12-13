import pygame
import engine
import globals

CINZA_ESCURO = (50,50,50)
COR_FUNDO = (232,186,79)
PRETO = (0,0,0)

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 24) # Utilizar uma fonte para que seja possível inserir texto

# função retirada de: https://nerdparadise.com/programming/pygameblitopacity
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

def drawText(screen, t, x, y, fg, alpha):
    text = font.render(t, True, fg)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)

    blit_alpha(screen, text, (x, y), alpha)

heart_image = pygame.image.load("images/heart0.png")

coin0 = pygame.image.load("images/coin0.png")
coin1 = pygame.image.load("images/coin1.png")
coin2 = pygame.image.load("images/coin2.png")
coin3 = pygame.image.load("images/coin3.png")
coin4 = pygame.image.load("images/coin4.png")
coin5 = pygame.image.load("images/coin5.png")

powerupVida = pygame.image.load("images/powerupVida.png")

def setHealth(entity):
    if entity.battle:
        entity.battle.vidas = 3

def setInvisivel(entity):
    if entity.animations:
        entity.animations.alpha = 50

def endInvisivel(entity):
    if entity.animations:
        entity.animations.alpha = 255

powerups = ["vida", "invisivel"]

powerupImages = {
    "vida" : [pygame.image.load("images/powerupVida.png")],
    "invisivel" : [pygame.image.load("images/powerupInvis.png")]
}

powerupSound = {
    "vida" : "coin",
    "invisivel" : "coin"
}

powerupApply = {
    "vida" : setHealth,
    "invisivel" : setInvisivel
}

powerupEnd= {
    "vida" : None,
    "invisivel" : endInvisivel
}

powerupEffectTimer = {
    "vida" : 0,
    "invisivel" : 1000
}

def makePowerup(type, x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,40,40)
    entityAnimation = engine.Animation(powerupImages[type])
    entity.animations.add("idle", entityAnimation)
    entity.effect = engine.Effect(
        powerupApply[type],
        powerupEffectTimer[type], 
        powerupSound[type], 
        powerupEnd[type]
    )
    return entity

def makeCoin(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,23,23) # Componente de posição da moeda 1
    entityAnimation = engine.Animation([coin1, coin2, coin3, coin4, coin5])
    entity.animations.add("idle", entityAnimation)
    entity.type = "collectable"
    return entity

enemy0 = pygame.image.load("images/spike0.png")

def makeEnemy(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,41,9) # Componente de posição do inimigo 1
    entityAnimation = engine.Animation([enemy0])
    entity.animations.add("idle", entityAnimation)
    entity.type = "dangerous"
    return entity


ativo1 = pygame.image.load("images/ativo1.png")
naoativo1 = pygame.image.load("images/naoativo1.png")

idle0 = pygame.image.load("images/pingu0.png")
idle1 = pygame.image.load("images/pingu1.png")

walking0 = pygame.image.load("images/pinguandar0.png")
walking1 = pygame.image.load("images/pinguandar1.png")
walking2 = pygame.image.load("images/pinguandar2.png")
walking3 = pygame.image.load("images/pinguandar3.png")
walking4 = pygame.image.load("images/pinguandar4.png")
walking5 = pygame.image.load("images/pinguandar5.png")

def setPlayerCameras():
     
    # jogo de 1 jogador 
    if len(globals.players) == 1:
        p = globals.players[0]
        p.camera = engine.Camera(10,10,810,810)
        p.camera.setWorldPos(p.position.initial.x, p.position.initial.y)
        p.camera.trackEntity(p)
        
    # jogo de 2 jogadores
    if len(globals.players) == 2:
        p1 = globals.players[0]
        p1.camera = engine.Camera(10,10,400,810)
        p1.camera.setWorldPos(p1.position.initial.x, p1.position.initial.y)
        p1.camera.trackEntity(p1)

        p2 = globals.players[1]
        p2.camera = engine.Camera(420,10,400,810)
        p2.camera.setWorldPos(p2.position.initial.x, p2.position.initial.y)
        p2.camera.trackEntity(p2)

    # jogo de 3 ou 4 jogadores
    if len(globals.players) >= 3:
        p1 = globals.players[0]
        p1.camera = engine.Camera(10,10,400,400)
        p1.camera.setWorldPos(p1.position.initial.x, p1.position.initial.y)
        p1.camera.trackEntity(p1)

        p2 = globals.players[1]
        p2.camera = engine.Camera(420,10,400,400)
        p2.camera.setWorldPos(p2.position.initial.x, p2.position.initial.y)
        p2.camera.trackEntity(p2)

        p3 = globals.players[2]
        p3.camera = engine.Camera(10,420,400,400)
        p3.camera.setWorldPos(p3.position.initial.x, p3.position.initial.y)
        p3.camera.trackEntity(p3)

        if len(globals.players) == 4:
            p4 = globals.players[3]
            p4.camera = engine.Camera(420,420,400,400)
            p4.camera.setWorldPos(p4.position.initial.x, p4.position.initial.y)
            p4.camera.trackEntity(p4)

def resetPlayer(entity):
    entity.score.score = 0
    entity.battle.vidas = 3
    entity.position.rect.x = entity.position.initial.x
    entity.position.rect.y = entity.position.initial.y
    entity.speed = 0
    entity.acceleration = 0.2
    entity.camera.setWorldPos(entity.position.initial.x, entity.position.initial.y)
    entity.direction = "right"
    entity.animations.alpha = 255
    entity.effect = None

def makePlayer(x,y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,32,31) # Componente de posição do inimigo 1
    entityIdleAnimation = engine.Animation([idle0, idle1])
    entityWalkingAnimation = engine.Animation([walking0, walking1, walking2, walking3, walking4, walking5])
    entity.animations.add("idle", entityIdleAnimation)
    entity.animations.add("walking", entityWalkingAnimation)
    entity.score = engine.Score()
    entity.battle = engine.Battle()
    entity.intention = engine.Intention()
    entity.acceleration = 0.2
    entity.type = "player"
    entity.reset = resetPlayer
    return entity

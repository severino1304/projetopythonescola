import pygame
import utils
import globals
import random

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen=None, inputStream=None): # Verificar cada entidade
        for entity in globals.world.entities:
            if self.check(entity): # Qualquer entidade que verifique, atualiza
                self.updateEntity(screen, inputStream, entity)
    def updateEntity(self, screen, inputStream, entity):
        pass

class PowerupSystem(System):
    def __init__(self):
        self.timer = 0
    def check(self, entity):
        return entity.effect is not None
    def update(self, screen=None, inputStream=None):
        super().update(screen, inputStream) # classe "super", que é a System()

        # contar o número de powerups no mundo
        count = 0
        for entity in globals.world.entities:
            if entity.type != "player":
                if entity.effect:
                    count += 1

        # se não existirem powerups começa um temporizador para criar um novo
        if count == 0 and self.timer == 0:
            self.timer = 500

        # criar um powerup se o timer chegar ao fim
        if self.timer > 0:
            # tirar tempo ao timer
            self.timer -= 1
            if self.timer <= 0:
                # criar um powerup
                if globals.world.powerupSpawnPoints is not None:
                    if len(globals.world.powerupSpawnPoints) > 0:
                        spawnPos = random.choice(globals.world.powerupSpawnPoints)
                        globals.world.entities.append(
                            utils.makePowerup(random.choice(utils.powerups), spawnPos[0], spawnPos[1])
                        )

        print("count:", count, "timer", self.timer)

    def updateEntity(self, screen, inputStream, entity):

        # coletar os powerups
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == "player" and entity.type != "player":
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # dar a componente efeito ao jogador
                    otherEntity.effect = entity.effect
                    globals.soundManager.playSound(entity.effect.sound)
                    # remover do mundo o powerup coletado
                    globals.world.entities.remove(entity)

        # aplicar os efeitos dos powerups aos jogadores
        if entity.type == "player":
            entity.effect.apply(entity)
            entity.effect.timer -= 1
            # se acabar o efeito
            if entity.effect.timer <= 0:
                # dar reset à entidade se for apropriado
                if entity.effect.end:
                    entity.effect.end(entity)
                # destroi o efeito
                entity.effect = None

class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None
    def updateEntity(self, screen, inputStream, entity):
        entity.animations.animationList[entity.state].update()  

class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None
    def updateEntity(self, screen, inputStream, entity):
        new_x = entity.position.rect.x # Atualizar a posição de uma entidade para a variável "new_x"
        new_y = entity.position.rect.y # Atualizar a posição de uma entidade para a variável "new_y"

        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x -= 2
                entity.direction = "left" # Muda a direção para que está virado o personagem do jogador
                entity.state = "walking"
            if entity.intention.moveRight:
                new_x += 2
                entity.direction = "right" # Muda a direção para que está virado o personagem do jogador
                entity.state = "walking"
            if  not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = "idle"
            if entity.intention.jump and entity.on_ground:
                globals.soundManager.playSound("jump")
                entity.speed = -5

        # movimento horizontal

        new_x_rect = pygame.Rect(
            int(new_x),
            int(entity.position.rect.y),
            entity.position.rect.width,
            entity.position.rect.height) # Novo retângulo com a posição nova do jogador de acordo com o sprite
    
        x_colisao = False # Sem colisão inicialmente

        #... verificar contra todas as plataformas
        for platform in globals.world.platforms:
            if platform.colliderect(new_x_rect):
                x_colisao = True # Colisão
                break

        if x_colisao == False: # Se não houver colisão, atualizar a posição do jogador
            entity.position.rect.x = new_x

        # movimento vertical (gravidade)

        entity.speed += entity.acceleration
        new_y += entity.speed 

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(new_y),
            entity.position.rect.width,
            entity.position.rect.height) # Novo retângulo com a posição nova do jogador de acordo com o sprite
        
        y_colisao = False # Sem colisão inicialmente
        entity.on_ground = False

        #... verificar contra todas as plataformas
        for platform in globals.world.platforms:
            if platform.colliderect(new_y_rect):
                y_colisao = True # Colisão
                entity.speed = 0
                # Se a plataforma estiver debaixo do jogador então queremos colocar o jogador na plataforma
                if platform[1] >  new_y:
                    entity.position.rect.y = platform[1] - entity.position.rect.height
                    entity.on_ground = True
                break

        if y_colisao == False: # Se não houver colisão, atualizar a posição do jogador
            entity.position.rect.y = int(new_y)

        # reínicar as intenções
        if entity.intention is not None:
            entity.intention.moveLeft = False
            entity.intention.moveRight = False
            entity.intention.jump = False

class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.intention is not None
    def updateEntity(self, screen, inputStream, entity):
        # up = jump
        if inputStream.keyboard.isKeyDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # left = walkLeft
        if inputStream.keyboard.isKeyDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False
        # right = moveRight
        if inputStream.keyboard.isKeyDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False
        # b1 = zoomOut
        if inputStream.keyboard.isKeyDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False
        # b2 = zoomIn
        if inputStream.keyboard.isKeyDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False

class CollectionSystem(System):
    def check(self, entity):
        return entity.type == "player" and entity.score is not None
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == "collectable": # Se não for outra entidade
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    globals.soundManager.playSound("coin")
                    globals.world.entities.remove(otherEntity)
                    entity.score.score += 1

class BattleSystem(System):
    def check(self, entity):
        return entity.type == "player" and entity.battle is not None
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == "dangerous": # Se não for outra entidade
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.battle.onCollide(entity, otherEntity)
                    entity.battle.vidas -= 1
                    
                    # dar reset à posição do jogador
                    entity.position.rect.x = entity.position.initial.x
                    entity.position.rect.y = entity.position.initial.y
                    entity.speed = 0

                    # remover o jogador caso não sobrem vidas
                    if entity.battle.vidas <= 0:
                        globals.world.entities.remove(entity)

class CameraSystem(System):
    def check(self, entity): # Correr o sistema camera apenas nas entidades que contêm "camera", ou seja, que têm componente camera
        return entity.camera is not None
    def updateEntity(self, screen, inputStream, entity):

        # zoom
        if entity.intention is not None:
            if entity.intention.zoomIn:
                entity.camera.zoomLevel += 0.01
            if entity.intention.zoomOut:
                entity.camera.zoomLevel -= 0.01

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        # atualizar a camera caso esteja a dar track numa entidade
        if entity.camera.entityToTrack is not None:

            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.worldX = (currentX * 0.95) + (targetX * 0.05)
            entity.camera.worldY = (currentY * 0.95) + (targetY * 0.05)

        # calcular offsets
        offsetX = cameraRect.x + cameraRect.w/2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h/2 - (entity.camera.worldY * entity.camera.zoomLevel)

        # preencher o background da camera
        screen.fill(globals.PRETO)

        # renderizar plataformas
        for p in globals.world.platforms: # Para cada plataforma da lista, chamar "p" às plataformas
            newPosRect = pygame.Rect(
                p.x * entity.camera.zoomLevel + offsetX, 
                p.y * entity.camera.zoomLevel + offsetY, 
                p.w * entity.camera.zoomLevel, 
                p.h * entity.camera.zoomLevel)
            pygame.draw.rect(screen, (232, 186, 79), newPosRect) # Desenhar retângulo

        # renderizar entidades
        for e in globals.world.entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen, 
                   (e.position.rect.x * entity.camera.zoomLevel) + offsetX, 
                   (e.position.rect.y * entity.camera.zoomLevel) + offsetY, 
                   e.direction == "right", False, entity.camera.zoomLevel, e.animations.alpha)

        # HUD das entidades

        # score
        if entity.score is not None:
            screen.blit(utils.coin0, (entity.camera.rect.x + 10, entity.camera.rect.y + 10))
            utils.drawText(screen, str(entity.score.score), entity.camera.rect.x + 50, 20, globals.BRANCO, 255)

        # Vidas
        if entity.battle is not None:
            for v in range(entity.battle.vidas):
                screen.blit(utils.heart_image, (entity.camera.rect.x + 200 + (v*50),entity.camera.rect.y + 10))

        # unset clipping rectangle
        screen.set_clip(None)

class Camera:
    def __init__(self, x, y, w, h): # Componente da camera
        self.rect = pygame.Rect(x,y,w,h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1
    def setWorldPos(self, x, y):
        self.worldX = x
        self.worldY = y
    def trackEntity(self, e):
        self.entityToTrack = e

class Position: # Componente da posição
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.initial = pygame.Rect(x, y, w, h) # posição inicial

class Animations: # Dicionário onde estão várias animações e estados
    def __init__(self):
        self.animationList = {}
        self.alpha = 255
    def add(self, state, animation):
        self.animationList[state] = animation

class Animation: # Componente de animação
    def __init__(self, imageList):
        self.imageList = imageList # Lista das imagens da animação
        self.imageIndex = 0 # Frames da animação
        self.animationTimer = 0
        self.animationSpeed = 10
    def update(self):
        self.animationTimer += 1 # Aumentar o timer
        if self.animationTimer >= self.animationSpeed: # Se o timer aumentar demasiado: mudar a imagem da animação
            self.animationTimer = 0 # Reset no timer
            self.imageIndex +=1 # Mudar a imagem
            if self.imageIndex > len(self.imageList) - 1: # Se o index for superior ao número de itens na lista de imagens:
                self.imageIndex = 0
    def draw(self, screen, x, y, flipX, flipY, zoomLevel, alpha):
        image = self.imageList[self.imageIndex]
        image.set_alpha(alpha)
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (newWidth,newHeight)), (x, y)) # Desenho da animação

class Score: # Componente da posição
    def __init__(self):
        self.score = 0

class Battle: # Componente da posição
    def __init__(self):
        self.vidas = 3

class Input:
    def __init__(self, up, down, left, right, b1, b2):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.b1 = b1
        self.b2 = b2

class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False

class Effect:
    def __init__(self, apply, timer, sound, end):
        self.apply = apply
        self.timer = timer
        self.sound = sound
        self.end = end

def resetEntity(entity):
    pass

class Entity:
    def __init__(self):
        self.state = "idle" # Todas as entidades começam no estado "idle"
        self.type = "normal"
        self.position = None # Varíavel que guarda o componente da posição
        self.animations = Animations()
        self.direction = "right"
        self.camera = None
        self.score = None
        self.battle = None
        self.speed = 0
        self.input = None
        self.intention = None
        self.on_ground = False
        self.acceleration = 0
        self.effect = None
        self.reset = resetEntity # guardar referencia a "self.reset" para correr a função
import pygame
import utils
import globals # type: ignore
import engine
import ui
import level

class Scene:
    def __init__(self):
        pass
    def onEnter (self):
        pass
    def onExit (self):
        pass
    def input(self, sm, inputStream):
        pass
    def update(self, sm, inputStream):
        pass
    def draw(self, sm, screen):
        pass

class MainMenuScene(Scene): # Primeira cena (predifinido)
    def __init__(self):
        self.enter = ui.ButtonUI(pygame.K_RETURN, "[ENTER=Próximo]", 50, 200)
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, "[ESCAPE=Voltar]", 50, 250)
    def onEnter(self):
        globals.soundManager.playMusicFade("nome1")
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            sm.push(FadeTransitionScene([self], [PlayerSelectScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
    def update(self, sm, inputStream):
        self.enter.update(inputStream)
        self.esc.update(inputStream)
    def draw(self, sm, screen):
        # background
        screen.fill(globals.CINZA_ESCURO)
        utils.drawText(screen, "Menu Principal", 50, 50, globals.BRANCO, 255)
        self.enter.draw(screen)
        self.esc.draw(screen)

class LevelSelectScene(Scene):
    def __init__(self):
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, "[ESCAPE=Voltar]", 50, 300)
    def onEnter(self):
       globals.soundManager.playMusicFade("nome1")
    def update(self, sm, inputStream):
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_a):
            globals.currentLevel = max(globals.currentLevel-1, 1)
        if inputStream.keyboard.isKeyPressed(pygame.K_d):
            globals.currentLevel = min(globals.currentLevel+1, globals.lastCompletedLevel)
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            level.loadLevel(globals.currentLevel)
            sm.push(FadeTransitionScene([self], [GameScene()]))

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE): # Tecla "ESCAPE" leva para o Selecionador de Niveis
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
    def draw(self, sm, screen):
        # background
        screen.fill(globals.CINZA_ESCURO)
        utils.drawText(screen, "Selecionar Nível", 50, 50, globals.BRANCO, 255)
        self.esc.draw(screen)

        # desenhar o selecionador de nível
        for levelNumber in range(1, globals.maxLevel+1):
            c = globals.BRANCO
            if levelNumber == globals.currentLevel:
                c = globals.VERDE
            a = 255
            if levelNumber > globals.lastCompletedLevel:
                a = 100
            utils.drawText(screen, str(levelNumber), levelNumber*100, 100, c, a)

class PlayerSelectScene(Scene):
    def __init__(self):
        self.enter = ui.ButtonUI(pygame.K_RETURN, "[ENTER=Próximo]", 50, 200)
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, "[ESCAPE=Voltar]", 50, 250)
    def onEnter(self):
       globals.soundManager.playMusicFade("nome1")
    def update(self, sm, inputStream):
        self.enter.update(inputStream)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):

        # lidar com cada jogador
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:

            # adicionar ao jogo
            if inputStream.keyboard.isKeyPressed(player.input.b1):
                if player not in globals.players:
                    globals.players.append(player)
        
            # remover do jogo
            if inputStream.keyboard.isKeyPressed(player.input.b2):
                if player in globals.players:
                    globals.players.remove(player)

        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            if len(globals.players) > 0:
                utils.setPlayerCameras()
                sm.push(FadeTransitionScene([self], [LevelSelectScene()]))

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE): # Tecla "ESCAPE" leva para o Selecionador de Niveis
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
    def draw(self, sm, screen):
        # background
        screen.fill(globals.CINZA_ESCURO)
        utils.drawText(screen, "Selecionar Personagem", 50, 50, globals.BRANCO, 255)
        self.esc.draw(screen)
        self.enter.draw(screen)

        # desenhar os jogadores selecionados
        if globals.player1 in globals.players:
            screen.blit(utils.ativo1, (100,100))
        else:
            screen.blit(utils.naoativo1, (100,100))

        if globals.player2 in globals.players:
            screen.blit(utils.ativo1, (150,100))
        else:
            screen.blit(utils.naoativo1, (150,100))

        if globals.player3 in globals.players:
            screen.blit(utils.ativo1, (200,100))
        else:
            screen.blit(utils.naoativo1, (200,100))

        if globals.player4 in globals.players:
            screen.blit(utils.ativo1, (250,100))
        else:
            screen.blit(utils.naoativo1, (250,100))


class GameScene(Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = engine.CollectionSystem()
        self.battleSystem = engine.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()
        self.powerupSystem = engine.PowerupSystem()
    def onEnter(self):
        globals.soundManager.playMusicFade("nome2")
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop() # pop na gamescene
            sm.push(FadeTransitionScene([self], []))
        if globals.world.isWon():
            # atualiza o mapa do selecionador dos níveis acessíveis
            nextLevel = min(globals.currentLevel+1, globals.maxLevel)
            levelToUnlock = max(nextLevel, globals.lastCompletedLevel)
            globals.lastCompletedLevel = levelToUnlock
            globals.currentLevel = nextLevel
            sm.push(WinScene())
        if globals.world.isLost():
            sm.push(LoseScene())
    def update(self, sm, inputStream):
        self.inputSystem.update(inputStream=inputStream)
        self.collectionSystem.update()
        self.battleSystem.update()
        self.physicsSystem.update()
        self.animationSystem.update()
        self.powerupSystem.update()
    def draw(self, sm, screen):
        # background
        screen.fill(globals.CINZA_ESCURO)
        self.cameraSystem.update(screen)

class WinScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, "[ESC=Sair]", 50, 200)
    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # desenhar um fundo transparente
        bgSurf = pygame.Surface((830, 830))
        bgSurf.fill((globals.PRETO))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, "Venceste!", 50, 50, globals.BRANCO, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)

class LoseScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, "[ESC = Sair]", 50, 200)
    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([self], [MainMenuScene(), LevelSelectScene()])])
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # desenhar um fundo transparente
        bgSurf = pygame.Surface((830, 830))
        bgSurf.fill((globals.PRETO))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, "Perdeste!, pressiona ESCAPE", 150, 150, globals.BRANCO, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)

class TransitionScene(Scene):
    def __init__(self, fromScenes, toScenes):
        self.currentPercentage = 0 # Contador para a transição da cena
        self.fromScenes = fromScenes
        self.toScenes = toScenes
    def update(self, sm, inputStream):
        self.currentPercentage += 2 # Somar 2 ao contador
        if self.currentPercentage >= 100:
            sm.pop()
            for s in self.toScenes:
                sm.push(s)
        for scene in self.fromScenes:
            scene.update(sm, inputStream)
        if len(self.toScenes) > 0:
            for scene in self.toScenes:
                scene.update(sm, inputStream)
        else:
            if len(sm.scenes) > 1:
                sm.scenes[-2].update(sm, inputStream)

class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            for s in self.fromScenes:
                s.draw(sm, screen)
        else:
            if len(self.toScenes) == 0:
                if len(sm.scenes) > 1:
                    sm.scenes[-2].draw(sm,screen) # Caso não haja uma cena especificada desenhar a anterior
            else:
                for s in self.toScenes:
                    s.draw(sm, screen) # Caso haja uma cena especificada, desenha-a
        # fade overlay
        overlay = pygame.Surface((830, 830))
        # 0 = transparente, 255 = opaco
        # 0% = 0
        # 50% = 255
        # 100% = 0
        alpha = int(abs((255-(255/50)*self.currentPercentage))) # Transparência
        overlay.set_alpha(255 - alpha)
        overlay.fill(globals.PRETO)
        screen.blit(overlay, (0,0))
    
class SceneManager:
    def __init__(self):
        self.scenes = [] # Lista de cenas
    def isEmpty(self): # A lista está vazia?
        return len(self.scenes) == 0
    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()
    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()
    def input(self, inputStream):
        if len(self.scenes) > 0: # Se o comprimento da lista for > 0:
            self.scenes[-1].input(self, inputStream) # Ultimo item da lista (cimo)
    def update(self, inputStream):
        if len(self.scenes) > 0: # Se o comprimento da lista for > 0:
            self.scenes[-1].update(self, inputStream) # Ultimo item da lista (cimo)
    def draw(self, screen):
        if len(self.scenes) > 0: # Se o comprimento da lista for > 0:
            self.scenes[-1].draw(self, screen) # Ultimo item da lista (cimo)
        # apresentação do ecrã
        pygame.display.flip()
    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()
    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()
    def set(self, scenes):
        # dar pop em todas as cenas
        while len(self.scenes) > 0:
            self.pop()
        # acrescentar nova cena
        for s in scenes:
            self.push(s)
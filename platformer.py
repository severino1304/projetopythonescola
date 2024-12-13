import pygame # type: ignore
import engine
import utils # type: ignore
import level # type: ignore
import scene
import globals
import inputstream
import soundmanager # type: ignore

# variavaveis constantes
SCREEN_SIZE = (830,830)
CINZA_ESCURO = (50,50,50)
COR_FUNDO = (232,186,79)

# init
pygame.init() # iniciar o pygame
screen = pygame.display.set_mode(SCREEN_SIZE) # Tamanho do ecrã
pygame.display.set_caption("Jogo Plataforma") # Nome da janela
clock = pygame.time.Clock()

# estados do jogo = playing // win // lose
game_state = "playing"

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu) # stack com 1 scene (para já)

inputStream = inputstream.InputStream()

# criar o jogador 1
globals.player1 = utils.makePlayer(300,0)
#globals.player1.camera = engine.Camera(10,10,400,400)
#globals.player1.camera.setWorldPos(300, 0)
#globals.player1.camera.trackEntity(globals.player1)
globals.player1.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)

# criar o jogador 2
globals.player2 = utils.makePlayer(350,0)
#globals.player2.camera = engine.Camera(420,10,400,400)
#globals.player2.camera.setWorldPos(350, 0)
#globals.player2.camera.trackEntity(globals.player2)
globals.player2.input = engine.Input(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_o, pygame.K_p)

# criar o jogador 3
globals.player3 = utils.makePlayer(400,0)
#globals.player3.camera = engine.Camera(10,420,400,400)
#globals.player3.camera.setWorldPos(400, 0)
#globals.player3.camera.trackEntity(globals.player3)
globals.player3.input = engine.Input(pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_x)

# criar o jogador 4
globals.player4 = utils.makePlayer(450,0)
#globals.player4.camera = engine.Camera(420,420,400,400)
#globals.player4.camera.setWorldPos(450, 0)
#globals.player4.camera.trackEntity(globals.player4)
globals.player4.input = engine.Input(pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_z, pygame.K_x)

running = True
while running:
# game loop
    
    # verificar para "quit"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Fecha a janela do jogo
    
    inputStream.processInput()
    globals.soundManager.update()

    if sceneManager.isEmpty():
        running = False
    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    
    clock.tick(90) # Corre no máx. 90 FPS

# quit
pygame.quit()

"""
Ideias:
Fazer 2 personagems (alto e baixo) e colocar tuneis em que so o baixo consegue aceder

# desenho do retangulo de colisão para debugging
    pygame.draw.rect(screen, (255, 0, 0), new_player_rect, 2)


Fazer o nível recomeçar automaticamente após perder

Som "noot noot" ao vencer com o pingu

spinning cat inimigo
maxwell
"""




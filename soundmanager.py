import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.soundVolume = 0.2 # definir o volume dos sons atuais
        self.musicVolume = 0 # definir o volume da música atual
        self.targetMusicVolume = 0.1 # relembra o valor do volume da música
        self.nextMusic = None
        self.currentMusic = None
        self.sounds = {
            "jump" : pygame.mixer.Sound("sons/salto1.ogg"),
            "coin" : pygame.mixer.Sound("sons/apanharmoeda1.ogg")
        }
        self.music = {
            "nome1" : "musica/musicamenu1.ogg",
            "nome2" : "musica/musicaniveis1.ogg"
        }
    def playSound(self, soundName):
        self.sounds[soundName].set_volume(self.soundVolume) # Definir o volume para o "self.soundVolume"
        self.sounds[soundName].play()
    def playMusic(self, musicName):
        print(self.musicVolume)

        # não tocar a música caso já esteja a tocar
        if musicName is self.currentMusic:
            return
        
        pygame.mixer.music.load(self.music[musicName]) # Definir o volume para o "self.musicVolume"
        pygame.mixer.music.set_volume(self.musicVolume)
        self.currentMusic = musicName
        pygame.mixer.music.play(-1) # Manter a música em loop até que seja introduzida outra
    def playMusicFade(self, musicName):

        # não tocar a música caso já esteja a tocar
        if musicName is self.currentMusic:
            return
        
        self.nextMusic = musicName # adiciona música à "lista de espera"
        self.fadeOut() # dá fade out à musica atual
    def fadeOut(self):
        pygame.mixer.music.fadeout(500) # duração do "fade/transição" = 500 milissegundos
    def update(self):
         # aumenta o volume da música até ao "targetMusicVolume" (0.2):
        if self.musicVolume < self.targetMusicVolume:
            self.musicVolume = min(self.musicVolume + 0.005, self.targetMusicVolume)
            pygame.mixer.music.set_volume(self.musicVolume) # definir o novo volume (de forma a fazer a transição/fade)
        # tocar a próxima música caso seja apropriado:
        if self.nextMusic is not None:
            # caso a música anterior ja terminou o seu "fade out"
            if not pygame.mixer.music.get_busy():
                self.currentMusic = None
                self.musicVolume = 0
                pygame.mixer.music.set_volume(self.musicVolume) # definir o novo volume (de forma a fazer a transição/fade)
                self.playMusic(self.nextMusic)
                # remover da fila de músicas:
                self.nextMusic = None
import pygame
import pygame.gfxdraw as gfxdraw
import time
import itertools as ito
import cv2


class TestSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color = None, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if color != None:
            self.color = color
            self.image.fill(color)

class TestGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

def percent(x, y = 0):
    return x * (y / 100)
class Game:
    WIDTH = 1250
    HEIGHT = 680
    FPS = 120
    gameSurfaceVideo = cv2.VideoCapture('main_menu_background.mp4')
    titleMenuGif = cv2.VideoCapture('title_menu.gif')
    __singleton = False
    @staticmethod
    def percentX(x):
        return Game.WIDTH * (x/100)
    @staticmethod
    def percentY(y):
        return Game.HEIGHT * (y/100)
    def __init__(self):
        if Game.__singleton:
            raise Exception("`Game` class must be initiated just once.")
        super().__init__()
        Game.__singleton = True
    def __init(self):
        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.tick = 0
        self.gameSurfaceWidth = Game.percentX(100)
        self.gameSurfaceHeight = Game.percentY(100)
        self.sideBar = pygame.transform.scale(pygame.image.load('beside_options_copy.png'),(Game.percentX(29.75), Game.HEIGHT))
        self.sideBar_rect = self.sideBar.get_rect()
        # self.game_surface = pygame.Surface((self.gameSurfaceWidth, self.gameSurfaceHeight)).convert_alpha()
        self.titleMenu = pygame.transform.scale(pygame.image.load('title_menu_copy.png'),(Game.percentX(32), percent(self.sideBar_rect.height, 34)))
        self.titleMenu_rect = self.titleMenu.get_rect()
        self.titleMenuPaddingX = Game.percentX(11)
        self.titleMenuPaddingY = Game.percentY(5)
        # self.game_surface.fill((0,0,0,16))
        # self.game_surface_rect = self.game_surface.get_rect()
    def __enter__(self):
        pygame.init()
        self.__init()
        return self
    def __terminate(self):
        pygame.quit()
    def __exit__(self, exc_type, exc_value, traceback):
        self.__terminate()

    def windowEventHandler(self):
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                self.running = False
    def startRender(self):
        success , video_image = Game.gameSurfaceVideo.read()
        if not success:
            Game.gameSurfaceVideo.set(cv2.CAP_PROP_POS_MSEC, 0)
            success , video_image = Game.gameSurfaceVideo.read()
        self.game_surface = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (Game.WIDTH,Game.HEIGHT + Game.percentY(1)))
        self.game_surface.blit(self.sideBar, (0, 0))
        
        # success , gif_image = Game.titleMenuGif.read()
        # if not success:
        #     Game.titleMenuGif.set(cv2.CAP_PROP_POS_MSEC, 0)
        #     success , gif_image = Game.titleMenuGif.read()
        # titleMenu = pygame.transform.scale(pygame.image.frombuffer(gif_image.tobytes(), gif_image.shape[1::-1], "BGR"), (Game.percentX(30), percent(self.sideBar_rect.height, 30)))
        self.screen.blit(self.game_surface, ((Game.WIDTH / 2) - (self.gameSurfaceWidth / 2) + (self.sideBar_rect.width / 1.5) ,0))
        self.surface.blit(self.titleMenu, ((self.sideBar_rect.width / 4) - (self.sideBar_rect.width / 3) + self.titleMenuPaddingX, percent(self.sideBar_rect.height, 8)+ self.titleMenuPaddingY) )
    def endRender(self):
        pygame.display.flip()
        self.tick = self.clock.tick(Game.FPS) / 1000
    def start(self):
        return self.run()
    def run(self):
        while self.running:
            self.windowEventHandler()
            self.startRender()
            self.endRender()
    @staticmethod
    def _static_run():
        with Game() as game:
            game.start()

if __name__ == '__main__':
    Game._static_run()
import pygame
import pygame.gfxdraw as gfxdraw
import time
import itertools as ito
import cv2
import random
import csv

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

class OptionSprite(pygame.sprite.Sprite):
    def __init__(self, /, image, x, y, value, *groups):
        super().__init__(groups)
        image_rect = image.get_rect()
        self.image = pygame.Surface((image_rect.width, image_rect.height))
        self.option_image = image
        self.image.blit(image,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = value
    @classmethod
    def fromSurface(cls, surface):
        rect = surface.get_rect()
        return cls(surface, rect.width, rect.height, rect.x, rect.y)
class MenuGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

class KeyComponent(pygame.sprite.Sprite):
    SPEED = 360
    def __init__(self, image, width, height, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(image,(width,height)).convert_alpha()
        self.rect = self.image.get_rect()
    def update(self, dt, *args, **kwargs):
        self.rect.y += KeyComponent.SPEED * dt
        if self.rect.y > Game.HEIGHT:
            self.kill()
        return super().update(*args, **kwargs)
class KeyGroup(pygame.sprite.Group):
    def update(self, dt, *args, **kwargs):
        return super().update(dt,*args,**kwargs)
class LineComponent(pygame.sprite.Sprite):
    def __init__(self, image, width, height, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(image,(width,height)).convert_alpha()
        self.rect = self.image.get_rect()
class LineGroup(pygame.sprite.Group):
    pass

def percent(x, y = 0):
    return x * (y / 100)
class Game:
    WIDTH = 1260
    HEIGHT = 720
    FPS = 70
    gameSurfaceVideo = cv2.VideoCapture('main_menu_background.mp4')
    titleMenuGif = cv2.VideoCapture('title_menu.gif')
    mainGameBackgroundGif = cv2.VideoCapture('main_game_background.gif')
    helpPageGif = cv2.VideoCapture('help_page.gif')
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
        # self.sideBar = pygame.transform.scale(pygame.image.load('beside_options_copy.png'),(Game.percentX(28.5), Game.HEIGHT))
        self.sideBar = pygame.transform.scale(pygame.image.load('beside_options_copy2.png').convert_alpha(),(Game.percentX(48.25), Game.HEIGHT))
        self.sideBar_rect = self.sideBar.get_rect()
        self.inMenu = True
        self.inGame = False
        # self.game_surface = pygame.Surface((self.gameSurfaceWidth, self.gameSurfaceHeight)).convert_alpha()
        self.titleMenu = pygame.transform.scale(pygame.image.load('title_menu_copy.png'),(Game.percentX(32.375), percent(self.sideBar_rect.height, 32.75)))
        self.titleMenu_rect = self.titleMenu.get_rect()
        self.titleMenuPaddingX = Game.percentX(12.375)
        self.titleMenuPaddingY = Game.percentY(4.75)
        self.menuOptions = pygame.Surface((Game.percentX(30),Game.percentY(40))).convert_alpha()
        self.menuOptions_rect = self.menuOptions.get_rect()
        self.menuOptionMaxWidth = percent(self.menuOptions_rect.width, 80)
        menuOptionsTrail = pygame.image.load('option_trail_copy.png').convert_alpha()
        self.menuOptionsTrail_widthPercent = 35
        self.menuOptionsTrail_borderBoxWidth = percent(self.menuOptionMaxWidth, self.menuOptionsTrail_widthPercent)
        self.menuOptionsTrail = pygame.transform.scale(menuOptionsTrail, (percent(self.menuOptionMaxWidth, self.menuOptionsTrail_widthPercent + 0.125), percent(self.menuOptions_rect.height, 16.5)))
        self.menuOptionsTrail_rect = self.menuOptionsTrail.get_rect()
        self.settingsOptionRawImage = pygame.image.load('settings_option_copy.png').convert_alpha()
        howToPlayImage = pygame.image.load('how_to_play_option_copy.png').convert_alpha()
        exitGameOption = pygame.image.load('exit_game_option_copy.png').convert_alpha()
        self.optionSize = (percent(self.menuOptionMaxWidth, 77.5), percent(self.menuOptions_rect.height, 21.5))
        self.settingsOptionImage = pygame.transform.scale(self.settingsOptionRawImage, self.optionSize).convert_alpha()
        self.settings_rect = self.settingsOptionImage.get_rect()
        self.howToPlayImage = pygame.transform.scale(howToPlayImage, self.optionSize).convert_alpha()
        self.howToPlay_rect = self.howToPlayImage.get_rect()
        self.exitGameOption = pygame.transform.scale(exitGameOption, self.optionSize).convert_alpha()
        self.exit_rect = self.exitGameOption.get_rect()
        self.trailOptionGapX = percent(self.menuOptions_rect.width, 0)
        self.trailOptionGapY = percent(self.menuOptions_rect.height, 2)
        self.settingsOptionSprite = OptionSprite(self.settingsOptionImage,*(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,0),"settings")
        self.howToPlaySprite = OptionSprite(self.howToPlayImage,*(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,self.settings_rect.y + self.settings_rect.height + self.trailOptionGapY), "howToPlay")
        self.exitGameOptionSprite = OptionSprite(self.exitGameOption,*(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,self.settings_rect.y + self.settings_rect.height + self.howToPlay_rect.height + self.trailOptionGapY + percent(self.menuOptions_rect.height, 2.375)), "exit")
        self.menuOptionsPoints = (0, self.titleMenu_rect.height * 1.68)
        self.menuGroup = MenuGroup(self.howToPlaySprite, self.exitGameOptionSprite, self.settingsOptionSprite)
        self.optionMap = {"settings":0b01, "howToPlay":0b10,"exit":0b00}
        self.optionStatus = 0b11
        pygame.mixer.music.load('bitch lasagna.mp3')
        self.optionOnHover = False
        self.main_game = pygame.Surface((Game.percentX(60), Game.HEIGHT)).convert_alpha()
        self.main_game_rect = self.main_game.get_rect()
        self.keys = 6
        self.keyComponentWidth = self.main_game_rect.width / self.keys
        # self.keyComponentHeight = Game.percentY(14)
        self.keyComponentHeight = self.keyComponentWidth
        self.songFinished = pygame.event.custom_type()
        self.dropDelay = 0
        self.lastDropTime = 0
        lineImage = pygame.image.load("line_copy2.png").convert_alpha()
        lineImage.set_alpha(2)
        self.lineSprite = LineComponent(lineImage,self.main_game_rect.width, Game.percentY(12))
        self.lineSprite = LineComponent(lineImage,self.main_game_rect.width, Game.percentY(8))
        linePaddingBottom = 30
        self.lineSprite.image.set_alpha(230)
        self.lineSprite.rect.y = self.main_game_rect.height - self.lineSprite.rect.height - linePaddingBottom
        self.lineGroup = LineGroup(self.lineSprite)
        self.songKeyMapFiles = {"test":"forsen_level1.csv"}
        self.keyGroup = KeyGroup()
        self.KeyAImage = pygame.image.load("KeyA.png")
        pygame.mixer.music.set_endevent(self.songFinished)
        # pygame.mixer.music.play()
        
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

    def windowEventHandler(self, keys):
        for key in keys:
            if key.type == pygame.QUIT:
                self.running = False
    def menuEventHandler(self):
        for sprite in self.menuGroup.sprites():
            if sprite.rect.move(self.menuOptionsPoints).collidepoint(pygame.mouse.get_pos()):
                if not self.optionOnHover:
                    self.optionOnHover = True
                    overlay = pygame.Surface((sprite.rect.width, sprite.rect.height)).convert_alpha()
                    overlay.set_alpha(75)
                    sprite.image.blit(sprite.option_image,(0,0))
                    sprite.image.blit((overlay),(0,0))
                    break
            else:
                self.optionOnHover = False
                sprite.image.fill((0,0,0,0))
                sprite.image.blit(sprite.option_image, (0,0))
        
        keys = pygame.event.get()
        self.windowEventHandler(keys)
        for key in keys:
            match key.type:
                case pygame.KEYDOWN:
                    if key.dict.get('unicode') == 'y':
                        # pygame.mixer.music.rewind()
                        # pygame.mixer.music.play()
                        # pygame.mixer.music.set_pos(120)
                        self.inGame = True
                        self.inMenu = False
                case pygame.MOUSEBUTTONDOWN:
                    for sprite in self.menuGroup.sprites():
                        if sprite.rect.move(self.menuOptionsPoints).collidepoint(pygame.mouse.get_pos()):
                            self.optionStatus = 0b11 & self.optionMap.get(sprite.value,0b11)
                        # print(self.optionStatus, sprite.value)
    def helpPageEventHandler(self):
        keys = pygame.event.get()
        self.windowEventHandler(keys)
        for key in keys:
            match key.type:
                case pygame.KEYDOWN:
                    if key.dict.get('unicode') == '\x1b':
                        self.inHelpPage = False
                        self.optionStatus = 0b11
    def helpPageRender(self):
        success , video_image = Game.helpPageGif.read()
        if not success:
            Game.helpPageGif.set(cv2.CAP_PROP_POS_MSEC, 0)
            success , video_image = Game.helpPageGif.read()
        self.game_surface = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (Game.WIDTH,Game.HEIGHT))
        self.screen.blit(self.game_surface,(0, 0))
    def menuRender(self):
        self.menuEventHandler()
        success , video_image = Game.gameSurfaceVideo.read()
        if not success:
            Game.gameSurfaceVideo.set(cv2.CAP_PROP_POS_MSEC, 0)
            success , video_image = Game.gameSurfaceVideo.read()
        self.game_surface = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (Game.WIDTH,Game.HEIGHT + Game.percentY(1)))
        
        # success , gif_image = Game.titleMenuGif.read()
        # if not success:
        #     Game.titleMenuGif.set(cv2.CAP_PROP_POS_MSEC, 0)
        #     success , gif_image = Game.titleMenuGif.read()
        # titleMenu = pygame.transform.scale(pygame.image.frombuffer(gif_image.tobytes(), gif_image.shape[1::-1], "BGR"), (Game.percentX(30), percent(self.sideBar_rect.height, 30)))
        self.screen.blit(self.game_surface, ((Game.WIDTH / 2) - (self.gameSurfaceWidth / 2) + (self.sideBar_rect.width / 2) ,0))
        self.surface.blit(self.sideBar, (0, 0))
        self.surface.blit(self.titleMenu, ((self.sideBar_rect.width / 4) - (self.sideBar_rect.width / 3) + self.titleMenuPaddingX, percent(self.sideBar_rect.height, 8)+ self.titleMenuPaddingY))
        self.surface.blit(self.menuOptions, self.menuOptionsPoints)

        self.menuOptions.blit(self.menuOptionsTrail,(0,0 + percent(self.menuOptions_rect.height, 2.375)))
        # self.menuOptions.blit(self.settingsOptionImage,(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,0))
        self.menuOptions.blit(self.menuOptionsTrail,(0,self.settings_rect.y + self.settings_rect.height + self.trailOptionGapY + percent(self.menuOptions_rect.height, 2.375)))
        # self.menuOptions.blit(self.howToPlayImage,(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,self.settings_rect.y + self.settings_rect.height + self.trailOptionGapY))
        self.menuOptions.blit(self.menuOptionsTrail,(0,self.settings_rect.y + self.settings_rect.height + self.howToPlay_rect.height + self.trailOptionGapY + (percent(self.menuOptions_rect.height, 2.375) * 2)))
        # self.menuOptions.blit(self.exitGameOption,(self.menuOptionsTrail_borderBoxWidth + self.trailOptionGapX,self.settings_rect.y + self.settings_rect.height + self.howToPlay_rect.height + self.trailOptionGapY + percent(self.menuOptions_rect.height, 2.375)))
        self.menuGroup.draw(self.menuOptions)
        
        match self.optionStatus:
            case 0b00:
                self.running = False
            case 0b10:
                self.inHelpPage = True
                while self.running and self.inHelpPage:
                    self.helpPageEventHandler()
                    self.helpPageRender()
                    self.endRender()
    def endRender(self):
        pygame.display.flip()
        self.tick = self.clock.tick(Game.FPS) / 1000
    def gameEventHandler(self):
        keys = pygame.event.get()
        self.windowEventHandler(keys)
        for key in keys:
            match key.type:
                case pygame.KEYDOWN:
                    if key.dict.get('unicode') == '\x1b':
                        pygame.mixer.music.rewind()
                        self.keyGroup.empty()
                        self.inGame = False
                        self.inMenu = True
                case self.songFinished:
                    self.inMenu = True
                    self.inGame = False
    def gameRender(self):
        self.gameEventHandler()
        success, video_image = Game.mainGameBackgroundGif.read()
        if not success:
            Game.mainGameBackgroundGif.set(cv2.CAP_PROP_POS_MSEC, 0)
            success, video_image = Game.mainGameBackgroundGif.read()
        self.game_surface = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (Game.WIDTH, Game.HEIGHT))
        game_surface_rect = self.game_surface.get_rect()
        self.surface.blit(self.game_surface, (0,0))
        self.main_game.fill((0,0,0,4))
        self.keyGroup.update(self.tick)
        self.keyGroup.draw(self.main_game)
        self.lineGroup.draw(self.main_game)
        self.surface.blit(self.main_game,(game_surface_rect.centerx - (self.main_game_rect.width / 2), 0))
        
        # if self.dropDelay / 1000 <= (time.time() - self.lastDropTime):
    
    def start(self):
        return self.run()
    def run(self):
        while self.running:
            if self.inMenu:
                while self.running and self.inMenu:
                    self.menuRender()
                    self.endRender()
            elif self.inGame:
                with open(self.songKeyMapFiles["test"], "r", newline="") as file:
                    levelMap = list(csv.reader(file, delimiter=","))
                    levelMapLen = len(levelMap)
                    i = 0
                    while self.running and self.inGame:
                        if i < levelMapLen:
                            if self.dropDelay / 1000 <= (time.time() - self.lastDropTime):
                                keyComponentInstance = KeyComponent(self.KeyAImage,self.keyComponentWidth, self.keyComponentHeight)
                                self.keyGroup.add(keyComponentInstance)
                                self.dropDelay = float(levelMap[i][1])
                                self.lastDropTime = time.time()
                                print(self.dropDelay)
                                i+=1
                        self.gameRender()
                        self.endRender()
    @staticmethod
    def _static_run():
        with Game() as game:
            game.start()

if __name__ == '__main__':
    Game._static_run()
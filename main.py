import pygame, sys, time

import ScreenManager
import ValueManager

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(ValueManager.screen_size)
pygame.display.set_caption("Crossover Weather")
pygame.mouse.set_visible(False)
pygame.display.set_icon(pygame.image.load("./images/icon.ico"))

if __name__ == "__main__":
    prev_time = time.time()

    # TODO: LOAD DATA FOR EACH SCREEN
    intro_screen = ScreenManager.IntroScreen()
    select_screen = ScreenManager.SelectScreen()
    playing_screen = ScreenManager.PlayingScreen()
    
    # TODO: SET BGM FOR EACH SCREEN
    intro_bgm = pygame.mixer.Channel(0)
    intro_bgm.play(pygame.mixer.Sound("./sound/IntroBGM.mp3"), loops=-1, fade_ms=1000)
    intro_bgm.set_volume(0.5)

    playing_bgm = pygame.mixer.Channel(1)
    playing_bgm.play(pygame.mixer.Sound("./sound/PlayingBGM.mp3"), loops=-1, fade_ms=1000)
    playing_bgm.set_volume(0.5)
    
    # TODO: GAME LOOP
    while True:
        # TODO: GET THE DELTATIME
        dt = time.time() - prev_time
        prev_time = time.time()
        
        # TODO: SET THE CONDITION TO QUIT
        if ValueManager.screen_mode == "Quit":
            pygame.quit()
            sys.exit()
            
        # TODO: PLAY THE BGM
        if ValueManager.screen_mode == "Intro" or ValueManager.screen_mode == "Select":
            playing_bgm.pause()
            intro_bgm.unpause()
        else:
            intro_bgm.pause()        
            playing_bgm.unpause()
                    
        # TODO: SHOW EACH SCREEN
        if ValueManager.screen_mode == "Intro":
            intro_screen.show_screen(dt)
            if ValueManager.screen_mode == "Select":
                select_screen.reset()
        elif ValueManager.screen_mode == "Select":
            intro_screen.clean_screen()
            select_screen.show_screen(dt)
            if ValueManager.screen_mode == "Intro":
                intro_screen.reset()
        elif ValueManager.screen_mode == "Playing":
            select_screen.clean_screen()
            playing_screen.show_screen(dt)
            if ValueManager.screen_mode == "Intro":
                intro_screen.reset()
        
        version_font = pygame.font.Font(None, 40)
        version = version_font.render(" Version 1.7", True, "white")
        screen.blit(version, (0, 670))
            
        # TODO: UPDATE SCREEN EVERY 60 FRAMES PER SECOND
        pygame.display.update()
        clock.tick(60)
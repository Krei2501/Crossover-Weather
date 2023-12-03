import pygame, sys, random

import GameMechanism
import ValueManager
import MapGenerator
import ObjectManager

from report import report

class IntroScreen:
    def __init__(self):
        self.background = pygame.image.load("./images/objects/Title_Background.png").convert_alpha()

        self.title = ObjectManager.Title(75, 150)
        self.mouse = ObjectManager.Mouse(600, 350)

        self.objects = pygame.sprite.Group()
        self.animations = ObjectManager.BackgroundEffect()

        self.reset()
    
    def clean_screen(self):
        self.objects.empty()
        self.animations.empty()
     
    def reset(self):        
        self.objects.add(ObjectManager.Button(625, 400, "PlayButton"))
        self.objects.add(ObjectManager.Button(625, 520, "QuitButton"))
        
        for x in range(0, 1250, 200):
            self.animations.add(ObjectManager.Object(x, random.randint(0, 700), "Leaf"))
            self.animations.add(
                ObjectManager.Object(x + 100, random.randint(0, 700), "Snow")
            )
    
    def show_screen(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen = pygame.display.get_surface()

        screen.blit(self.background, (0, 0))

        self.animations.update(dt)
        self.animations.draw(screen)

        self.title.update(dt)
        screen.blit(self.title.image, self.title.rect)

        self.objects.draw(screen)
        self.objects.update(self.mouse, dt)

        self.mouse.update()
        screen.blit(self.mouse.image, self.mouse.rect)

class SelectScreen:
    def __init__(self):
        self.background = pygame.Surface((1250, 700))
        self.background.fill((64, 188, 239))

        self.mouse = ObjectManager.Mouse(600, 350)

        self.objects = pygame.sprite.Group()
        self.menu = pygame.sprite.Group()

        self.reset()
        
        self.cd = 0
    
    def clean_screen(self):
        self.objects.empty()
        self.menu.empty()
    
    def reset(self):
        self.objects.add(ObjectManager.Button(1000, 620, "PlayButton"))
        self.objects.add(ObjectManager.Button(75, 75, "HomeButton"))
        self.objects.add(ObjectManager.Button(680, 620, "EasyMode"))

        x = 220
        y = 130
        for name in [
            "cat",
            "chicken",
            "dog",
            "duck",
            "frog",
            "rabbit",
            "penguin",
            "dinosaur",
        ]:
            if name == "frog":
                x = 220
                y += 220
            self.objects.add(ObjectManager.Character(x, y, name))
            x += 220
    
    def show_screen(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen = pygame.display.get_surface()

        screen.blit(self.background, (0, 0))

        title_font = pygame.font.Font(ValueManager.font, 60)
        screen.blit(
            title_font.render("CHOOSE YOUR CHARACTER", True, "white"), (150, 35)
        )
        name_font = pygame.font.Font(ValueManager.font, 30)
        screen.blit(
            name_font.render(
                f"Your character: {ValueManager.player_name.capitalize()}",
                True,
                "white",
            ),
            (80, 600),
        )

        self.objects.draw(screen)
        self.objects.update(self.mouse, dt)

        if self.cd < 1 and ValueManager.report_message != "":
            self.cd += dt
            report(ValueManager.report_message)
        else:
            self.cd = 0
            ValueManager.report_message = ""

        self.mouse.update()
        screen.blit(self.mouse.image, self.mouse.rect)

class PlayingScreen:
    transparency = 200
    cd = 0

    def __init__(self):
        self.large_font = pygame.font.Font(ValueManager.font, 60)
        self.normal_font = pygame.font.Font(ValueManager.font, 30)

        self.left_surface = pygame.image.load("./images/objects/LeftScreen.png")
        self.right_surface = pygame.Surface((1250 - 850, 700))
        self.right_surface.fill((74, 190, 249))
        self.mid_surface = pygame.Surface((500, 50))
        self.mid_surface.fill((74, 190, 249))

        self.mouse = ObjectManager.Mouse(
            ValueManager.screen_size[0] / 2, ValueManager.screen_size[1] / 2
        )
        self.show_mouse = True
        
        self.snow_effect = ObjectManager.EnvironmentEffect("Snow")
        self.game_over_sound = pygame.mixer.Sound("./sound/GameOver.wav")
        self.play_sound = True
        
        self.func_button = ObjectManager.Button(75, 75, "PauseButton")
        self.scoreboard = ObjectManager.Table(900, 50, "CurrentScore")

        self.objects_over = pygame.sprite.Group()
        self.objects_over.add(ObjectManager.Button(570, 500, "RestartButton"))
        self.objects_over.add(ObjectManager.Button(650, 500, "HomeButton"))

        self.keyboard = pygame.sprite.Group()
        self.keyboard.add(ObjectManager.Key(115, 345, "WButton"))
        self.keyboard.add(ObjectManager.Key(45, 415, "AButton"))
        self.keyboard.add(ObjectManager.Key(115, 415, "SButton"))
        self.keyboard.add(ObjectManager.Key(185, 415, "DButton"))
        self.keyboard.add(ObjectManager.Key(30, 575, "SpaceButton"))

        self.players = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        
        self.is_special_map = False

    def draw_all(self, players, obstacles, background, dt):
        player = players.sprite
        screen = pygame.display.get_surface()
        background.draw(screen)

        final_layer = pygame.sprite.Group()

        for obstacle in sorted(
            obstacles.sprites(), key=lambda sprite: sprite.rect.centery
        ):
            match obstacle.name:
                case "green_tree" | "snow_tree":
                    if obstacle.rect.centery <= player.rect.bottom:
                        screen.blit(obstacle.image, obstacle.rect)
                    else:
                        final_layer.add(obstacle)
                case "snowball":
                    if obstacle.rect.bottom <= player.rect.bottom:
                        screen.blit(obstacle.image, obstacle.rect)
                    else:
                        final_layer.add(obstacle)
                case _:
                    screen.blit(obstacle.image, obstacle.rect)

        screen.blit(player.image, player.rect)

        for obstacle in sorted(
            final_layer.sprites(), key=lambda sprite: sprite.rect.centery
        ):
            screen.blit(obstacle.image, obstacle.rect)

    def show_screen(self, dt):
        screen = pygame.display.get_surface()

        if GameMechanism.game_state == "New Map":
            if GameMechanism.num_stage % 10 == 1:
                self.is_special_map = False
            elif GameMechanism.num_stage % 10 == 6:
                self.is_special_map = True
            MapGenerator.new_map(
                players=self.players,
                obstacles=self.obstacles,
                background=self.background,
                difficulty=GameMechanism.game_mode,
                special=self.is_special_map,
            )

            GameMechanism.game_state = "Changing"

            self.play_sound = True
            
        self.draw_all(self.players, self.obstacles, self.background, dt)
        
        if self.is_special_map:
            self.snow_effect.update(dt)
            self.snow_effect.draw(screen)    
        
        if GameMechanism.game_state == "Game Over":
            game_over_surf = pygame.Surface((500, 600))
            game_over_surf.fill((40, 42, 54))
            game_over_surf.set_alpha(150)

            self.players.sprite.GameOver_animation(dt)
            if self.play_sound:
                self.play_sound = False
                self.game_over_sound.play()
            
            if self.players.sprite.transparency < 150:
                screen.blit(game_over_surf, (350, 50))
                title_font = pygame.font.Font(ValueManager.font, 60)
                screen.blit(title_font.render("Game Over", True, "white"), (400, 200))

                detail_font = pygame.font.Font(ValueManager.font, 30)
                screen.blit(
                    detail_font.render(
                        f"Highest score: {int(GameMechanism.highest_score):^}",
                        True,
                        "white",
                    ),
                    (370, 300),
                )
                screen.blit(
                    detail_font.render(
                        f"Your score: {int(GameMechanism.game_score):^}", True, "white"
                    ),
                    (370, 350),
                )

                self.objects_over.update(self.mouse, dt)
                self.objects_over.draw(screen)

        if GameMechanism.game_state == "Playing":
            GameMechanism.control_game(
                players=self.players,
                obstacles=self.obstacles,
                background=self.background,
                deltatime=dt,
            )

        if GameMechanism.game_state == "Paused":
            pause_surf = pygame.Surface((500, 600))
            pause_surf.fill((40, 42, 54))
            pause_surf.set_alpha(150)

            screen.blit(pause_surf, (350, 50))
            screen.blit(self.large_font.render("Paused", True, "white"), (470, 200))

            self.objects_over.update(self.mouse, dt)
            self.objects_over.draw(screen)

        if GameMechanism.game_state == "Changing":
            new_map_surf = pygame.Surface((500, 600))

            if self.transparency > 0:
                self.cd += dt
                if self.cd > 0.75:
                    self.transparency -= 255 * dt
                if self.transparency < 0:
                    self.transparency = 0

                new_map_surf.fill((40, 42, 54))
                new_map_surf.set_alpha(self.transparency)
                color = (
                    "Green"
                    if GameMechanism.game_mode == "Easy"
                    else "Orange"
                    if GameMechanism.game_mode == "Medium"
                    else "Red"
                )
                stage_surf = self.large_font.render(
                    f"Stage {GameMechanism.num_stage}", True, color
                )
                stage_rect = stage_surf.get_rect(topleft=(470, 200))
                stage_surf.set_alpha(self.transparency)
                mode_surf = self.normal_font.render(
                    f"{GameMechanism.game_mode}", True, color
                )
                mode_rect = mode_surf.get_rect(topleft=(550, 275))
                mode_surf.set_alpha(self.transparency)
                
                screen.blit(new_map_surf, (350, 50))
                screen.blit(stage_surf, stage_rect)
                screen.blit(mode_surf, mode_rect)
            else:
                self.transparency = 255
                GameMechanism.game_state = "Playing"

        screen.blit(self.left_surface, (0, 0))
        screen.blit(self.right_surface, (850, 0))
        screen.blit(self.mid_surface, (350, 0))
        screen.blit(self.mid_surface, (350, 650))

        # TODO: Show keyboard
        self.keyboard.update()
        self.keyboard.draw(screen)

        # TODO: Show function button
        self.func_button.update(self.mouse, dt)
        screen.blit(self.func_button.image, self.func_button.rect)

        # TODO: Show scoreboard
        self.scoreboard.update()
        screen.blit(self.scoreboard.image, self.scoreboard.rect)
        score_font = self.normal_font
        score = score_font.render(f"{int(GameMechanism.game_score):09}", True, "white")
        screen.blit(score, (940, 100))

        # TODO: Show extra features
        stage_surf = self.normal_font.render(
            f"Stage: {GameMechanism.num_stage}", True, "white"
        )
        stage_rect = stage_surf.get_rect(topleft=(900, 500))
        mode_surf = self.normal_font.render(
            f"Mode: {GameMechanism.game_mode}", True, "white"
        )
        mode_rect = mode_surf.get_rect(topleft=(900, 550))
        
        screen.blit(stage_surf, stage_rect)
        screen.blit(mode_surf, mode_rect)
        
        # TODO: Show description Pause/ Resume Button
        state_button = self.normal_font.render(
            "Pause" if GameMechanism.game_state != "Paused" else "Resume", True, "white"
        )
        screen.blit(state_button, (110, 55))

        # TODO: Show mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if GameMechanism.game_state == "Playing":
                    GameMechanism.game_state = "Paused"
                elif GameMechanism.game_state == "Paused":
                    GameMechanism.game_state = "Playing"
            if event.type == pygame.KEYDOWN:
                self.show_mouse = False
            if event.type == pygame.MOUSEMOTION:
                self.show_mouse = True

        if self.show_mouse:
            self.mouse.update()
            screen.blit(self.mouse.image, self.mouse.rect)

import pygame, random

import GameMechanism
import ValueManager

from report import report

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"./images/objects/{name}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(self.rect.center)

class BackgroundEffect(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.angle = 0
        self.direction = 1

    def update(self, dt):
        self.time += dt
        self.angle += 50 * dt * self.direction
        if self.time > 0.8:
            self.add(Object(random.randint(-50, 600), -100, "Leaf"))
            self.add(Object(random.randint(-50, 600), -100, "Snow"))
            self.add(Object(random.randint(600, 1250), -50, "Leaf"))
            self.add(Object(random.randint(600, 1250), -50, "Snow"))
            self.time = 0

        if -45 > self.angle or self.angle > 20:
            self.direction *= -1

        for sprite in self.sprites():
            if sprite.name == "Snow":
                sprite.pos.x += 25 * dt
                sprite.pos.y += 100 * dt
            elif sprite.name == "Leaf":
                sprite.pos.x += 50 * dt
                sprite.pos.y += 200 * dt
                sprite.image = pygame.transform.rotozoom(
                    pygame.image.load(f"./images/objects/{sprite.name}.png").convert_alpha(),
                    self.angle,
                    1,
                )

            sprite.rect.x = int(sprite.pos.x)
            sprite.rect.y = int(sprite.pos.y)
            if sprite.rect.y > 700:
                sprite.kill()

class EnvironmentEffect(pygame.sprite.Group):
    def __init__(self, name = "Leaf"):
        super().__init__()
        self.name = name
        self.time = 0
        self.angle = 0
        self.direction = 1

    def update(self, dt):
        self.time += dt
        self.angle += 50 * dt * self.direction
        if self.time > 0.5:
            self.add(Object(random.randint(300, 500), -50, self.name))
            self.add(Object(random.randint(600, 850), 0, self.name))
            self.time = 0

        if -20 > self.angle or self.angle > 20:
            self.direction *= -1

        for sprite in self.sprites():
            sprite.pos.x += 20 * dt
            sprite.pos.y += 100 * dt
            sprite.image = pygame.transform.rotozoom(
                pygame.image.load(f"./images/objects/{sprite.name}.png").convert_alpha(),
                self.angle,
                0.5,
            )
        
            sprite.rect.x = int(sprite.pos.x)
            sprite.rect.y = int(sprite.pos.y)
            if sprite.rect.y > 700:
                sprite.kill()

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"./images/objects/char_selection/{name}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(self.rect.center)
        self.cd = 0
        self.get_touch = False
        
        self.touch_sound = pygame.mixer.Sound("./sound/TouchButton.wav")
        self.touch_sound.set_volume(0.3)
        self.press_sound = pygame.mixer.Sound("./sound/PressButton.wav")
        self.press_sound.set_volume(0.3)
    
    def update(self, mouse, dt):
        image = pygame.image.load(f"./images/objects/char_selection/{self.name}.png").convert_alpha()
        if (
            pygame.sprite.collide_mask(self, mouse)
            and self.rect.topleft < mouse.rect.topleft < self.rect.bottomright
        ):  
            if not self.get_touch:
                self.get_touch = True
                self.touch_sound.play()
                
            keys = pygame.mouse.get_pressed()
            self.image = pygame.transform.rotozoom(image, 0, 1.2)
            self.cd += dt
            if keys[0]:
                if self.cd > 0.5:
                    self.cd = 0
                    self.press_sound.play()
                    ValueManager.player_name = self.name   
                                     
        else:
            self.get_touch = False
            if ValueManager.player_name == self.name:
                self.image = pygame.transform.rotozoom(image, 0, 1.2)
            else:   
                self.image = image
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

class Title(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "Title")
        self.scale = 0.9
        self.direction = 1

    def update(self, dt):
        self.scale += dt * self.direction / 5
        if self.scale > 1.1:
            self.scale = 1.1
            self.direction *= -1
        if self.scale < 0.9:
            self.scale = 0.9
            self.direction *= -1

        self.image = pygame.transform.scale_by(
            pygame.image.load(f"./images/objects/{self.name}.png").convert_alpha(), self.scale
        )
        self.rect = self.image.get_rect(center=self.pos)

class Table(Object):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)

class Mouse(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "Mouse")
        
    def update(self):
        self.rect = self.image.get_rect(topleft=pygame.mouse.get_pos())

class Key(Object):
    def __init__(self, x, y, name):
        super().__init__(x, y, f"{name}_Unpressed")
    
    def update(self):
        keys = pygame.key.get_pressed()
        new_name = f"{self.name.split(sep = "_")[0]}_Unpressed"
        name = self.name.split(sep = "_")[0]
        
        match name:
            case "WButton":
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    new_name = f"{name}_Pressed"
            case "AButton":
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    new_name = f"{name}_Pressed"
            case "SButton":
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    new_name = f"{name}_Pressed"
            case "DButton":
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    new_name = f"{name}_Pressed"
            case "SpaceButton":
                if keys[pygame.K_SPACE]:
                    new_name = f"{name}_Pressed"
                    
        self.name = new_name
        self.image = pygame.image.load(f"./images/objects/{new_name}.png").convert_alpha()
        
class Button(Object):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=(x, y))
        self.cd = 0
        self.get_touch = False
        
        self.touch_sound = pygame.mixer.Sound("./sound/TouchButton.wav")
        self.touch_sound.set_volume(0.3)
        self.press_sound = pygame.mixer.Sound("./sound/PressButton.wav")
        self.press_sound.set_volume(0.3)
        
    def change_skin(self, name):
        self.name = name
        self.image = pygame.image.load(f"./images/objects/{self.name}.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, mouse, dt):
        if self.name == "PauseButton" or self.name == "ResumeButton":
            if GameMechanism.game_state != "Paused":
                self.name = "PauseButton"
            else:
                self.name = "ResumeButton"
                
        image = pygame.image.load(f"./images/objects/{self.name}.png").convert_alpha()
        if (
            pygame.sprite.collide_mask(self, mouse)
            and self.rect.top < mouse.rect.top < self.rect.bottom
        ):
            if not self.get_touch:
                self.get_touch = True
                self.touch_sound.play()
                
            keys = pygame.mouse.get_pressed()
            self.image = pygame.transform.rotozoom(image, 0, 1.2)
            self.cd += dt
            if keys[0]:
                if self.cd > 0.5:
                    self.cd = 0
                    self.press_sound.play()
                    match self.name:
                        case "HomeButton":
                            ValueManager.screen_mode = "Intro"

                        case "PauseButton" | "ResumeButton":
                            if GameMechanism.game_state == "Playing":
                                GameMechanism.game_state = "Paused"
                            elif GameMechanism.game_state == "Paused":
                                GameMechanism.game_state = "Playing"

                        case "EasyMode" | "MediumMode" | "HardMode":
                            if self.name == "EasyMode":
                                ValueManager.game_mode = "Medium"
                                self.name = "MediumMode"
                            elif self.name == "MediumMode":
                                ValueManager.game_mode = "Hard"
                                self.name = "HardMode"
                            elif self.name == "HardMode":
                                ValueManager.game_mode = "Easy"
                                self.name = "EasyMode"
                        
                        case "PlayButton":
                            if ValueManager.screen_mode == "Intro":
                                ValueManager.screen_mode = "Select"
                            elif ValueManager.screen_mode == "Select":
                                if ValueManager.player_name == "":
                                    ValueManager.report_message = "You haven't chosen a player!"
                                else:
                                    ValueManager.screen_mode = "Playing"
                                    GameMechanism.reset_new_game()
                        
                        case "RestartButton":
                            GameMechanism.reset_new_game()
                        
                        case "QuitButton":
                            ValueManager.screen_mode = "Quit"

        else:
            self.get_touch = False
            self.image = image
            
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
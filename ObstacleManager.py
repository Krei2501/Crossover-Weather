import pygame, random
import ValueManager


class Obstacle(pygame.sprite.Sprite):
    # TODO: SET THE ATTRIBUTE FOR THE OBSTACLE
    def __init__(self, x, y, name, state, direction, type):
        super().__init__()
        self.type = type
        self.direction = direction
        self.change_skin(name, state)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = ValueManager.obstacle_speed
        self.is_clone = False
        self.touch_clock = 0

    # TODO: SET THE METHOD FOR THE OBSTACLE
    def change_skin(self, name, state):
        self.name = name
        self.state = state
        self.image = pygame.image.load(
            f"./images/obstacles/{self.name}s/{self.state}_{self.name}.png"
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

    def get_x(self, y):
        x = ValueManager.game_screen_pos[0]

        if self.direction == 1:
            x = x - self.image.get_size()[0]
        elif self.direction == -1:
            x = x + ValueManager.game_screen_size[0]

        return x

    def is_out_bound(self):
        left_limit = 350
        right_limit = 850

        if self.rect.right < left_limit or self.rect.left > right_limit:
            return True
        return False

    def is_collide_bound(self):
        left_limit = 350
        right_limit = 850

        if self.rect.left <= left_limit and self.direction == -1:
            return True
        if self.rect.right >= right_limit and self.direction == 1:
            return True
        return False

class Plank(Obstacle):
    def __init__(self, x, y, state="normal", direction=1, type="support"):
        super().__init__(x, y, "plank", state, direction, type)
        self.speed = ValueManager.obstacle_speed
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.current_image = 1

    def update(self, dt):
        match self.type:
            case "support" | "attack":
                self.pos.x += self.direction * self.speed * dt
                self.rect.x = round(self.pos.x)     
                self.rect.y = round(self.pos.y)
            case _:
                pass
            
    def animate(self, dt):
        self.current_image += 8 / 3 * dt
        if self.current_image < 5:
            self.image = pygame.image.load(f"./images/obstacles/planks/cracked_plank_{int(self.current_image)}.png").convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
        
class Ice(Obstacle):
    def __init__(self, x, y, state="normal", direction=1, type="support"):
        super().__init__(x, y, "ice", state, direction, type)
        self.speed = ValueManager.obstacle_speed
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.current_image = 1

    def update(self, dt):
        match self.type:
            case "support" | "attack":
                self.pos.x += self.direction * self.speed * dt
                self.rect.x = round(self.pos.x)     
                self.rect.y = round(self.pos.y)
            case _:
                pass

    def animate(self, dt):
        self.current_image += 8 / 3 * dt
        if self.current_image < 5:
            self.image = pygame.image.load(f"./images/obstacles/ices/cracked_ice_{int(self.current_image)}.png").convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)

class Tree(pygame.sprite.Sprite):
    is_rotate = False
    angle = 0

    def __init__(self, x, y, name="green_tree", direction = 0, state="up", type="block"):
        super().__init__()
        self.type = type
        self.speed = ValueManager.obstacle_speed / 2
        self.direction = direction
        self.change_skin(name, state)
        self.pos_x, self.pos_y = x, y
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def change_skin(self, name, state):
        self.name = name
        self.state = state
        self.file = f"./images/obstacles/trees/{self.name}/{self.name}_{self.state}.png"
        self.image = pygame.image.load(self.file).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        if self.is_rotate and self.angle < 90:
            self.type = "none"
            self.state = "down"
            self.angle += self.speed * dt
            if self.angle > 60:
                self.type = "attack"
                self.state = "down"
            
            if self.angle >= 90:
                self.file = f"./images/obstacles/trees/{self.name}/{self.name}_down_3_{self.direction}.png"
                self.type = "block"
            elif self.angle >= 60:
                self.file = f"./images/obstacles/trees/{self.name}/{self.name}_down_2_{self.direction}.png"
            elif self.angle >= 45:
                self.file = f"./images/obstacles/trees/{self.name}/{self.name}_down_1_{self.direction}.png"

            rotated_surface = pygame.transform.rotozoom(
                pygame.image.load(self.file).convert_alpha(), self.angle * self.direction, 1
            )
            self.image = rotated_surface
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

class Snowball(pygame.sprite.Sprite):
    is_clone = False
    angle = 0
    scale = 1

    def __init__(self, x, y, direction=1, type="attack"):
        super().__init__()
        self.name = "snowball"
        self.state = "rolling"
        self.direction = direction
        self.speed = ValueManager.obstacle_speed
        self.type = type
        self.file = f"./images/obstacles/others/{self.name}.png"
        self.image = pygame.image.load(self.file).convert_alpha()
        self.pos_x, self.pos_y = x, y
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt):
        self.pos.x += self.direction * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)
        self.angle += self.speed * self.direction * dt * -1
        self.scale += 0.001 * self.speed * dt
        self.image = pygame.transform.rotozoom(
            pygame.image.load(self.file), self.angle, self.scale
        ).convert_alpha()
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.pos_y))
        self.mask = pygame.mask.from_surface(self.image)

    def get_x(self, y):
        x = ValueManager.game_screen_pos[0]

        if self.direction == 1:
            x = x - 75
        elif self.direction == -1:
            x = x + ValueManager.game_screen_size[0] + 25

        return x

    def is_out_bound(self):
        left_limit = 350 - 5
        right_limit = 850 + 5

        if self.rect.right < left_limit or self.rect.left > right_limit:
            return True
        return False

    def is_collide_bound(self):
        left_limit = 350
        right_limit = 850

        if self.rect.left <= left_limit and self.direction == -1:
            return True
        if self.rect.right >= right_limit and self.direction == 1:
            return True
        return False

class River(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=1, name="river", state="running", type="attack"):
        super().__init__()
        self.name = name
        self.state = state
        self.type = type
        self.direction = direction
        if self.direction == 1:
            self.current_image = 1
        else:
            self.current_image = 7
        self.speed = ValueManager.obstacle_speed / 25
        self.file = f"./images/obstacles/river/river_{self.current_image}.png"
        self.image = pygame.image.load(self.file).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        if self.direction == 1:
            self.current_image += self.speed * dt

            if self.current_image > 7:
                self.current_image = 1
        elif self.direction == -1:
            self.current_image -= 0.1

            if self.current_image < 1:
                self.current_image = 7

        self.image = pygame.image.load(
            f"./images/obstacles/river/river_{int(self.current_image)}.png"
        ).convert_alpha()

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, name = "ground", state = "grass", type = "support"):
        super().__init__()
        self.name = name
        self.state = state
        self.type = type
        self.change_skin(state)
        self.rect = self.image.get_rect(topleft = (x, y))

    def change_skin(self, state):
        self.image = pygame.image.load(f"./images/obstacles/{self.state}_ground.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
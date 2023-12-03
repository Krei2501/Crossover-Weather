import pygame, ValueManager


class Player(pygame.sprite.Sprite):
    # TODO: SET THE ATTRIBUTE FOR THE PLAYER
    def __init__(self, name, state="Playing"):
        super().__init__()
        self.state = state
        self.speed = ValueManager.player_speed
        self.change_skin(name, "front")
        self.rect = self.image.get_rect(center=ValueManager.player_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.transparency = 255

    # TODO: SET THE METHOD FOR THE PLAYER
    def GameOver_animation(self, dt):
        if self.transparency > 200:
            self.move("up", dt, self.speed, False)
            self.transparency -= 120 * dt
            self.image.set_alpha(self.transparency)
        elif self.transparency > 150:
            self.move("down", dt, self.speed, False)
            self.transparency -= 120 * dt
            self.image.set_alpha(self.transparency)
    
    def change_skin(self, name, face):
        self.name = name
        self.face = face
        self.image = pygame.image.load(
            f"./images/players/{self.name}/{self.name}_{self.face}.png"
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

    # TODO: CONTROL THE MOVEMENT OF THE PLAYER
    def move(self, direction, deltatime, speed, is_change_state=True):
        before_x = self.rect.x
        before_y = self.rect.y
        match direction:
            case "left":
                self.pos.x -= speed * deltatime
            case "right":
                self.pos.x += speed * deltatime
            case "up":
                self.pos.y -= speed * deltatime
            case "down":
                self.pos.y += speed * deltatime

        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)

        if self.is_collide_bound():
            self.rect.x = self.pos.x = before_x
            self.rect.y = self.pos.y = before_y
            is_change_state = False

        if is_change_state:
            match direction:
                case "up":
                    self.change_skin(self.name, "back")
                case "down":
                    self.change_skin(self.name, "front")
                case "left" | "right":
                    self.change_skin(self.name, direction)

    def is_collide_bound(self):
        player = self.rect
        left_limit = 350
        right_limit = 850
        top_limit = 40
        bottom_limit = 650

        if (
            left_limit <= player.left < player.right <= right_limit
            and top_limit < player.bottom < bottom_limit
        ):
            return False

        return True

    # TODO: SET THE BASIC INTERACTIVE METHODS
    def is_collide_obstacle(self, obstacle):
        return pygame.sprite.collide_mask(self, obstacle)

    def is_on_line(self, limit_top, limit_bottom):
        if limit_top <= self.rect.bottom <= limit_bottom:
            return True
        return False

    def is_in_range(self, limit_left, limit_right):
        if self.rect.right > limit_left and self.rect.left < limit_right:
            return True
        return False

    def is_on_obstacle(self, obstacle):
        player = self.rect
        left_limit = obstacle.rect.left - 10
        right_limit = obstacle.rect.right + 10
        top_limit = obstacle.rect.top
        bottom_limit = obstacle.rect.bottom

        if (
            left_limit < player.centerx < right_limit
            and top_limit <= player.bottom <= bottom_limit
        ):
            return True
        return False

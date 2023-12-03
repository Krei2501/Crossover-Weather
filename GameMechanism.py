import pygame

from PlayerManager import Player
import ObstacleManager
import ValueManager
import FileManager

# * Game elements
current_time = pygame.time.get_ticks()
ready_time = 0
delta = ValueManager.delta

game_state = "New Map"
game_score = 0
highest_score = FileManager.read_score("./User.txt")
game_mode = ValueManager.game_mode
num_stage = 1

longest_distance = 0
height = 0
play_time = 0

# * Player State
is_player_can_move_up = is_player_can_move_down = True
is_player_can_move_left = is_player_can_move_right = True

def reset_new_game():
    global current_time, ready_time, delta
    global game_state, game_score, game_mode
    global num_stage
    global longest_distance, height, play_time
    
    current_time = pygame.time.get_ticks()
    ready_time = 0
    delta = ValueManager.delta

    game_state = "New Map"
    game_score = 0
    game_mode = ValueManager.game_mode
    num_stage = 1
    
    longest_distance = 0
    height = 0
    play_time = 0

def sign_value():
    global is_player_can_move_up, is_player_can_move_down
    global is_player_can_move_left, is_player_can_move_right
    global current_time, is_player_on_obstacle

    is_player_can_move_up = is_player_can_move_down = True
    is_player_can_move_left = is_player_can_move_right = True
    is_player_on_obstacle = False

    current_time = pygame.time.get_ticks()

def move_one_obstacle(player, obstacle, dt):
    if obstacle.direction == 1:
        player.move(
            direction="right",
            deltatime=dt,
            speed=obstacle.speed,
            is_change_state=False,
        )
    elif obstacle.direction == -1:
        player.move(
            direction="left",
            deltatime=dt,
            speed=obstacle.speed,
            is_change_state=False,
        )

def block_player(player, obstacle_left, obstacle_right, obstacle_top, obstacle_bottom):
    if player.is_in_range(obstacle_left, obstacle_right):
        if -delta < player.rect.bottom - obstacle_bottom < delta:
            global is_player_can_move_up
            is_player_can_move_up = False
        if -delta < player.rect.bottom - obstacle_top < delta:
            global is_player_can_move_down
            is_player_can_move_down = False
    if player.is_on_line(obstacle_top, obstacle_bottom):
        if -delta < player.rect.left - obstacle_right < delta:
            global is_player_can_move_left
            is_player_can_move_left = False
        if -delta < player.rect.right - obstacle_left < delta:
            global is_player_can_move_right
            is_player_can_move_right = False

def control_movement_player(player, dt):
    keys = pygame.key.get_pressed()
    
    speed = player.speed
    if keys[pygame.K_SPACE]:
        speed += ValueManager.obstacle_speed

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if is_player_can_move_up:
            player.move(direction = "up", deltatime = dt, speed = speed)
        else:
            player.change_skin(player.name, "back")
            
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if is_player_can_move_down:
            player.move(direction = "down", deltatime = dt, speed = speed)
        else:
            player.change_skin(player.name, "front")
            
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if is_player_can_move_left:
            player.move(direction = "left", deltatime = dt, speed = speed)
        else:
            player.change_skin(player.name, "left")
            
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if is_player_can_move_right:
            player.move(direction = "right", deltatime = dt, speed = speed)
        else:
            player.change_skin(player.name, "right")

def interact_with_obstacles(player, obstacles, dt):
    global game_state

    for obstacle in obstacles.sprites():
        match obstacle.type:
            case "support":
                if player.is_on_obstacle(obstacle):
                    move_one_obstacle(player, obstacle, dt)
            
            case "attack":
                match [obstacle.state, obstacle.name]:
                    case ["cracked", "plank" | "ice"]:
                        if player.is_collide_obstacle(obstacle):
                            if player.is_on_obstacle(obstacle):
                                obstacle.animate(dt)
                                obstacle.touch_clock += dt
                                
                                if obstacle.touch_clock > 1.3:
                                    game_state = "Game Over"
                                
                                move_one_obstacle(player, obstacle, dt)                           

                    case ["down", "green_tree" | "snow_tree"]:
                        if player.is_collide_obstacle(obstacle) and player.is_on_line(
                            obstacle.rect.centery - 15, obstacle.rect.centery + 15
                        ):
                            if obstacle.direction == -1 and player.is_in_range(
                                obstacle.rect.centerx + 20, obstacle.rect.centerx + 150
                            ):
                                game_state = "Game Over"

                            if obstacle.direction == 1 and player.is_in_range(
                                obstacle.rect.centerx - 150, obstacle.rect.centerx - 20
                            ):
                                game_state = "Game Over"

                    case ["rolling", "snowball"]:
                        if (
                            player.is_collide_obstacle(obstacle)
                            and player.is_on_line(obstacle.rect.bottom - 20,obstacle.rect.bottom)
                            and player.rect.left > obstacle.rect.x - 20
                        ):
                            game_state = "Game Over"
                            
            case "block":
                if obstacle.name != "green_tree" and obstacle.name != "snow_tree":
                    block_player(
                        player,
                        obstacle.rect.left,
                        obstacle.rect.right,
                        obstacle.rect.top,
                        obstacle.rect.bottom,
                    )
                else:
                    if obstacle.state == "up":
                        block_player(
                            player,
                            obstacle.rect.centerx - 20,
                            obstacle.rect.centerx + 20,
                            obstacle.rect.centery - 10,
                            obstacle.rect.centery + 10,
                        )
                    elif obstacle.state == "down":
                        if obstacle.direction == -1:
                            block_player(
                                player,
                                obstacle.rect.centerx,
                                obstacle.rect.centerx + 150,
                                obstacle.rect.centery - 15,
                                obstacle.rect.centery + 15,
                            )
                        elif obstacle.direction == 1:
                            block_player(
                                player,
                                obstacle.rect.centerx - 150,
                                obstacle.rect.centerx,
                                obstacle.rect.centery - 15,
                                obstacle.rect.centery + 15,
                            )

def control_movement_obstacles(player, obstacles, dt):
    obstacles.update(dt)
    list_obstacle = obstacles.sprites()
    for obstacle in list_obstacle:
        match obstacle.name:
            case "plank" | "ice" | "snowball":
                if obstacle.is_out_bound() and obstacle.is_clone:
                    obstacles.remove(obstacle)
                if obstacle.is_collide_bound() and not obstacle.is_clone:
                    global clone
                    match obstacle.name:
                        case "plank" | "ice":
                            y = obstacle.rect.top
                            x = obstacle.get_x(y)
                            if obstacle.name == "plank":
                                clone = ObstacleManager.Plank(x, y, obstacle.state)
                            else:
                                clone = ObstacleManager.Ice(x, y, obstacle.state)
                        case "snowball":
                            y = obstacle.pos_y
                            x = obstacle.get_x(y)
                            clone = ObstacleManager.Snowball(x, y)
                    clone.direction = obstacle.direction
                    clone.type = obstacle.type
                    obstacles.add(clone)

                    obstacle.is_clone = True
                    
            case "green_tree" | "snow_tree":
                if player.is_on_line(obstacle.rect.centery - 15, obstacle.rect.centery + 15):
                    if (
                        obstacle.rect.centerx < player.rect.centerx < obstacle.rect.centerx + 150
                        and obstacle.direction == -1
                    ):
                        obstacle.is_rotate = True
                    if (
                        obstacle.rect.centerx - 150 < player.rect.centerx < obstacle.rect.centerx
                        and obstacle.direction == 1
                    ):
                        obstacle.is_rotate = True

def is_on_any_obstacle(player, obstacles):
    list_obstacles = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_rect) 
    for obstacle in list_obstacles:
        if player.is_on_obstacle(obstacle) and obstacle.name in ["plank", "ice"]:
            return True
    return False

def interact_with_background(player, obstacles, background, dt):
    global game_state
    
    background.update(dt)
    for ground in background:
        if ground.name == "river":
            if not is_on_any_obstacle(player, obstacles):
                if player.is_collide_obstacle(ground) and player.is_on_line(ground.rect.top, ground.rect.bottom):
                    game_state = "Game Over"

def get_score(player):
    global game_score, highest_score
    global longest_distance, height
    global play_time
        
    ratio = 0.5 if game_mode == "Easy" else 0.8 if game_mode == "Medium" else 1

    height = max(height, 600 - player.rect.bottom)
    game_score = int((longest_distance + height) / 50) * 200 * ratio
    
    if game_state == "New Map":
        longest_distance += height
        height = 0
        
    if game_state == "Game Over":
        if game_score > highest_score:
            highest_score = game_score
        FileManager.write_score("./User.txt", highest_score)
        
def control_game(players, obstacles, background, deltatime):
    global ready_time
    global game_state, game_mode
    global num_stage
    global longest_distance
    
    player = players.sprite
    ready_time += deltatime
    
    sign_value()
    if player.rect.top < 10:
        game_state = "New Map"
        num_stage += 1
        ready_time = 0

    match ValueManager.game_mode:
        case "Easy":
            if num_stage > 10:
                game_mode = "Hard"
            elif num_stage > 5:
                game_mode = "Medium"
        case "Medium":
            if num_stage > 5:
                game_mode = "Hard"
    
    control_movement_obstacles(player, obstacles, deltatime)
    interact_with_obstacles(player, obstacles, deltatime)
    interact_with_background(player, obstacles, background, deltatime)
    control_movement_player(player, deltatime)
    get_score(player)
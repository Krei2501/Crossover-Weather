import pygame, random

from PlayerManager import Player
import ObstacleManager, ValueManager


def easy_mode(obstacles, background, special):
    pre_direction = 0
    num_obstacle = 0
    pre_x_left = pre_x_right = 0
    pre_tree = 0

    for y in range(550, 49, -50):
        # * Get direction of obstacles
        cur_direction = random.choice([-1, 0, 1])
        if cur_direction == pre_direction:
            if cur_direction == 0:
                cur_direction = random.choice([-1, 1])
            else:
                cur_direction *= -1

        # * Check if has more two obstacles next to each other
        num_obstacle += int(cur_direction != 0)
        if num_obstacle > 2:
            cur_direction = 0

        # * Get the ground and obstacles
        if cur_direction == 0:
            num_obstacle = 0
            background.add(
                ObstacleManager.Ground(350, y, state="snow" if special else "grass")
            )

            is_has_obstacle = random.choice([True, False])
            if is_has_obstacle:
                block_x = random.randrange(450, 601, 60)
                obstacles.add(
                    ObstacleManager.Plank(
                        block_x, y, state="snow" if special else "stop", type="block"
                    )
                )

            if y > 50:
                tree_x = random.choice([375, 825])
                if tree_x == pre_tree:
                    tree_x = 1200 - pre_tree
                pre_tree = tree_x
                obstacles.add(
                    ObstacleManager.Tree(
                        tree_x, y + 25, name="snow_tree" if special else "green_tree"
                    )
                )
        else:
            x = 0
            if cur_direction == 1:
                x = random.choice([200, 450])
                if x == pre_x_right:
                    x = 650 - pre_x_right
                pre_x_right = x
            else:
                x = random.choice([600, 850])
                if x == pre_x_left:
                    x = 1450 - pre_x_left
                pre_x_left = x

            if not special:
                background.add(ObstacleManager.River(350, y, direction=cur_direction))
                obstacles.add(ObstacleManager.Plank(x, y, direction=cur_direction))
            else:
                is_snowball = random.choice([True, False, False, False])
                if is_snowball:
                    background.add(ObstacleManager.Ground(350, y, state="snow"))
                    obstacles.add(
                        ObstacleManager.Snowball(350, y, direction=cur_direction)
                    )
                    obstacles.add(
                        ObstacleManager.Snowball(600, y, direction=cur_direction)
                    )
                else:
                    background.add(
                        ObstacleManager.River(350, y, direction=cur_direction)
                    )
                    obstacles.add(ObstacleManager.Ice(x, y, direction=cur_direction))

        pre_direction = cur_direction


def medium_mode(obstacles, background, special):
    pre_direction = 0
    num_obstacle = 0
    pre_x_left = pre_x_right = 0
    pre_tree = 0

    for y in range(550, 49, -50):
        # * Get direction of obstacles
        cur_direction = random.choice([-1, 0, 1])
        if cur_direction == pre_direction:
            if cur_direction == 0:
                cur_direction = random.choice([-1, 1])
            else:
                cur_direction *= -1

        # * Check if has more two obstacles next to each other
        num_obstacle += int(cur_direction != 0)
        if num_obstacle > 2:
            cur_direction = 0

        # * Get the ground and obstacles
        if cur_direction == 0:
            num_obstacle = 0
            background.add(
                ObstacleManager.Ground(350, y, state="snow" if special else "grass")
            )

            block_x = random.randrange(450, 601, 60)
            obstacles.add(
                ObstacleManager.Plank(
                    block_x, y, state="snow" if special else "stop", type="block"
                )
            )

            if y > 50:
                tree_x = random.choice([375, 825])
                if tree_x == pre_tree:
                    tree_x = 1200 - pre_tree
                pre_tree = tree_x

                tree_direction = 0
                if tree_x - (block_x + 150) >= 200:
                    tree_direction = 1
                elif block_x - tree_x >= 200:
                    tree_direction = -1

                obstacles.add(
                    ObstacleManager.Tree(
                        tree_x,
                        y + 25,
                        name="snow_tree" if special else "green_tree",
                        direction=tree_direction,
                    )
                )

        else:
            x = 0
            if cur_direction == 1:
                x = random.choice([200, 450])
                if x == pre_x_right:
                    x = 650 - pre_x_right
                pre_x_right = x
            else:
                x = random.choice([600, 850])
                if x == pre_x_left:
                    x = 1450 - pre_x_left
                pre_x_left = x

            type = random.choice(["support", "attack"])
            state = "normal" if type == "support" else "cracked"
            if not special:
                background.add(ObstacleManager.River(350, y, direction=cur_direction))
                obstacles.add(
                    ObstacleManager.Plank(
                        x, y, state=state, direction=cur_direction, type=type
                    )
                )
            else:
                is_snowball = random.choice([True, False, False, False])
                if is_snowball:
                    background.add(ObstacleManager.Ground(350, y, state="snow"))
                    obstacles.add(
                        ObstacleManager.Snowball(350, y, direction=cur_direction)
                    )
                    obstacles.add(
                        ObstacleManager.Snowball(600, y, direction=cur_direction)
                    )
                else:
                    background.add(
                        ObstacleManager.River(350, y, direction=cur_direction)
                    )
                    obstacles.add(
                        ObstacleManager.Ice(
                            x, y, state=state, direction=cur_direction, type=type
                        )
                    )

        pre_direction = cur_direction


def hard_mode(obstacles, background, special):
    prev_direction = 0
    num_obstacle = 0
    pre_x_left = pre_x_right = 0
    pre_tree = 0

    for y in range(550, 49, -50):
        # * Get direction of obstacles
        cur_direction = random.choice([-1, 0, 1])
        if cur_direction == prev_direction:
            if cur_direction == 0:
                cur_direction = random.choice([-1, 1])
            else:
                cur_direction *= -1

        # * Check if has more two obstacles next to each other
        num_obstacle += int(cur_direction != 0)
        if num_obstacle > 3:
            cur_direction = 0

        # * Get the ground and obstacles
        if cur_direction == 0:
            num_obstacle = 0
            background.add(
                ObstacleManager.Ground(350, y, state="snow" if special else "grass")
            )

            block_x = random.randrange(450, 601, 60)
            obstacles.add(
                ObstacleManager.Plank(
                    block_x, y, state="snow" if special else "stop", type="block"
                )
            )

            if y > 50:
                tree_x = random.choice([375, 825])
                if tree_x == pre_tree:
                    tree_x = 1200 - pre_tree
                pre_tree = tree_x

                tree_direction = 0
                if tree_x - (block_x + 150) >= 200:
                    tree_direction = 1
                elif block_x - tree_x >= 200:
                    tree_direction = -1

                obstacles.add(
                    ObstacleManager.Tree(
                        tree_x,
                        y + 25,
                        name="snow_tree" if special else "green_tree",
                        direction=tree_direction,
                    )
                )

        else:
            x = 0
            if cur_direction == 1:
                x = random.choice([200, 450])
                if x == pre_x_right:
                    x = 650 - pre_x_right
                pre_x_right = x
            else:
                x = random.choice([600, 850])
                if x == pre_x_left:
                    x = 1450 - pre_x_left
                pre_x_left = x

            type = random.choice(["support", "attack"])
            state = "normal" if type == "support" else "cracked"
            if not special:
                background.add(ObstacleManager.River(350, y, direction=cur_direction))
                obstacles.add(
                    ObstacleManager.Plank(
                        x, y, state=state, direction=cur_direction, type=type
                    )
                )
            else:
                is_snowball = random.choice([True, False, False, False])
                if is_snowball:
                    background.add(ObstacleManager.Ground(x=350, y=y, state="snow"))
                    obstacles.add(
                        ObstacleManager.Snowball(350, y, direction=cur_direction)
                    )
                    obstacles.add(
                        ObstacleManager.Snowball(600, y, direction=cur_direction)
                    )
                else:
                    background.add(
                        ObstacleManager.River(350, y, direction=cur_direction)
                    )
                    obstacles.add(
                        ObstacleManager.Ice(
                            x, y, state=state, direction=cur_direction, type=type
                        )
                    )

        prev_direction = cur_direction


def new_map(players, obstacles, background, difficulty, special=False):
    obstacles.empty()
    background.empty()

    players.empty()
    players.add(Player(name=ValueManager.player_name))

    match difficulty:
        case "Easy":
            easy_mode(obstacles, background, special)

        case "Medium":
            medium_mode(obstacles, background, special)

        case "Hard":
            hard_mode(obstacles, background, special)

    if not special:
        background.add(ObstacleManager.Ground(350, 600))
    else:
        background.add(ObstacleManager.Ground(350, 600, state="snow"))

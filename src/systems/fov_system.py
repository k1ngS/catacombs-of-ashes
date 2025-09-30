import math

from systems.ecs import Direction, Position


def system_update_fov(world_state):
    """
    Update the field of view (FOV) for the player.
    """
    ecs_world = world_state.world  # Access the ECS world dictionary
    world_state.visible_tiles = [[False for _ in range(world_state.width)] for _ in range(world_state.height)]

    player_pos = world_state.world[Position][world_state.player_id]
    player_direction = world_state.world[Direction][world_state.player_id]

    FOV_DEPTH = 5  # How far the player can see
    FOV_WIDTH = 0.8  # How wide the FOV is on each side

    if world_state.player_id in ecs_world[Position]:
        for y in range(world_state.height):
            for x in range(world_state.width):
                vector_x = x - player_pos.x
                vector_y = y - player_pos.y

                distance = math.sqrt(vector_x ** 2 + vector_y ** 2)

                if distance > 0 and distance <= FOV_DEPTH:
                    # Normalize the vector
                    norm_vector_x = vector_x / distance
                    norm_vector_y = vector_y / distance

                    # Calculate the dot product to determine if within FOV cone
                    dot_product = (norm_vector_x * player_direction.dx) + (norm_vector_y * player_direction.dy)

                    if dot_product > FOV_WIDTH:
                        world_state.visible_tiles[y][x] = True

                        player_pos = world_state.world[Position][world_state.player_id]
                        world_state.visible_tiles[player_pos.y][player_pos.x] = True  # Ensure player's tile is always visible
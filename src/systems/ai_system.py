import random

from systems.combat_system import system_resolve_combat
from systems.ecs import AI, Combat, Position


def simple_ai_system(world_state):
    """
    Simple AI system that makes enemies move randomly.
    """

    ecs_world = world_state.world  # Access the ECS world dictionary

    for entity_id, _ in ecs_world[AI].items():
        pos_component = ecs_world[Position][entity_id]

        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0,0)])  # Including (0,0) to allow no movement
        new_x = pos_component.x + dx
        new_y = pos_component.y + dy
        target_id = world_state.get_entity_at_position(new_x, new_y)
        if target_id == world_state.player_id:
            # Initiate combat
            system_resolve_combat(world_state, entity_id, target_id)

        elif target_id is None:
            # Check boundaries (assuming the map is a grid of '.' and '#')
            if (0 <= new_x < world_state.width and
                0 <= new_y < world_state.height and
                world_state.map[new_y][new_x] == "[grey50]░[/]"):

                pos_component.x = new_x
                pos_component.y = new_y
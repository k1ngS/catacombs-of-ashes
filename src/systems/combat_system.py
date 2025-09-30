from systems.ecs import Combat


def system_resolve_combat(world_state, attacker_id: int, defender_id: int):
    """
    Simple combat resolution system where the attacker always hits and deals fixed damage.
    """
    ecs_world = world_state.world  # Access the ECS world dictionary

    if attacker_id in ecs_world[Combat] and defender_id in ecs_world[Combat]:
        attacker_combat = ecs_world[Combat][attacker_id]
        defender_combat = ecs_world[Combat][defender_id]

        # Simple combat logic: attacker always hits and deals fixed damage
        defender_combat.current_hp -= attacker_combat.attack

        # Log the combat event
        world_state.add_message(f"Entity {attacker_id} attacks Entity {defender_id} for {attacker_combat.attack} damage!")

        # Check if defender is defeated
        if defender_combat.current_hp <= 0:
            if defender_combat == world_state.player_id:
                world_state.add_message("You have been defeated! Game Over.")
                world_state.game_over = True  # Set game over state
            else:
                world_state.add_message(f"Entity {defender_id} has been defeated!")
                # Remove defender from the world
                world_state.remove_entity(defender_id)
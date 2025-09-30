# Catacombs of Ashes

Catacombs of Ashes is a terminal-based game that combines elements of exploration, combat, and procedural generation. The project is developed in Python and uses an ECS (Entity-Component-System) architecture.

## Project Structure

The project is organized as follows:

```
LICENSE
poetry.lock
pyproject.toml
src/
	cli.py
	engine/
		__init__.py
		game_loop.py
		world_state.py
	renderer/
		__init__.py
		terminal_ui.py
	systems/
		__init__.py
		ai_system.py
		combat_system.py
		ecs.py
		fov_system.py
		procedural_gen.py
```

### Main Directories

- **engine/**: Contains the core game logic, including the game loop and world state.
- **renderer/**: Responsible for rendering the user interface in the terminal.
- **systems/**: Implements ECS systems such as AI, combat, procedural generation, and field of view.

## Requirements

This project uses [Poetry](https://python-poetry.org/) to manage dependencies. Make sure you have Poetry installed before proceeding.

### Dependencies
The project dependencies are listed in the `pyproject.toml` file and can be installed with the following command:

```bash
poetry install
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/k1ngS/catacombs-of-ashes.git
   ```

2. Navigate to the project directory:
   ```bash
   cd catacombs-of-ashes
   ```

3. Install the dependencies:
   ```bash
   poetry install
   ```

4. Run the game:
   ```bash
   poetry run python src/cli.py
   ```

## Contributing

Contributions are welcome! Follow the steps below to contribute:

1. Fork the repository.
2. Create a branch for your feature or bug fix:
   ```bash
   git checkout -b my-feature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push your changes:
   ```bash
   git push origin my-feature
   ```
5. Open a Pull Request in the original repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
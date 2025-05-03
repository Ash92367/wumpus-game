
Wumpus World Simulation Documentation

Overview:
This code simulates the Wumpus World, where an agent navigates a grid to find gold while avoiding pits and the Wumpus. The agent uses a knowledge base to make decisions based on its percepts (sensory inputs).

Classes and Methods:

1. Environment:
   Simulates the Wumpus World environment.

   Methods:
   - __init__(self, size=4): Initializes the environment with a specified grid size. Places pits, the Wumpus, and gold randomly in the grid.
     size: The size of the grid (default is 4).
   - place_pits(self): Randomly places pits in the grid.
   - place_wumpus(self): Randomly places the Wumpus in the grid.
   - place_gold(self): Randomly places gold in the grid.
   - get_percepts(self, x, y): Returns the percepts (sensory inputs) for the given position.
     x: The row index.
     y: The column index.
     Returns: A list of percepts (e.g., 'Breeze', 'Stench', 'Glitter').
   - is_valid_position(self, x, y): Checks if a position is valid within the grid boundaries.
     x: The row index.
     y: The column index.
     Returns: True if the position is valid, False otherwise.
   - remove_wumpus(self): Removes the Wumpus from the grid.
   - print_grid(self, agent_position): Prints the current state of the grid with the agent's position.
     agent_position: The current position of the agent as a tuple (x, y).

2. KB_Agent:
   Represents the agent that navigates the Wumpus World using a knowledge base.

   Methods:
   - __init__(self, env): Initializes the agent with a reference to the environment.
     env: An instance of the Environment class.
   - move(self, direction): Moves the agent in the specified direction if the move is valid.
     direction: The direction to move ('up', 'down', 'left', 'right').
   - update_kb(self, pos): Updates the agent's knowledge base with percepts from the given position.
     pos: The current position as a tuple (x, y).
   - mark_adjacent_as_dangerous(self, pos): Marks adjacent cells as dangerous if a breeze is perceived.
     pos: The current position as a tuple (x, y).
   - shoot_arrow(self): Shoots an arrow if the agent has any arrows left and updates the knowledge base accordingly.
     Returns: True if an arrow is shot, False otherwise.
   - pick_up_gold(self): Picks up gold if the agent perceives glitter.
     Returns: True if gold is collected, False otherwise.
   - make_decision(self): Makes a decision on the next move based on the agent's knowledge base.
   - move_to(self, x, y): Moves the agent to the specified position (x, y) by determining the appropriate direction to move.
   - play_game(self): Simulates the agent playing the game until gold is collected.
   - print_kb(self): Prints the current state of the agent's knowledge base.

3. test_agent:
   Function to test the agent's behavior in the Wumpus World.

   Methods:
   - test_agent(): Initializes the environment and the agent, then simulates the agent playing the game.

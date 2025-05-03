

import random

class Environment:
    def __init__(self, size=4):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.place_pits()
        self.place_wumpus()
        self.place_gold()
        self.agent_position = (0, 0)

    def place_pits(self):
        num_pits = random.randint(1, self.size)
        for _ in range(num_pits):
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if self.grid[x][y] == '':
                    self.grid[x][y] = 'P'
                    break

    def place_wumpus(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.grid[x][y] == '':
                self.grid[x][y] = 'W'
                break

    def place_gold(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.grid[x][y] == '':
                self.grid[x][y] = 'G'
                break

    def get_percepts(self, x, y):
        percepts = []
        if self.grid[x][y] == 'P':
            percepts.append('Breeze')
        if self.grid[x][y] == 'W':
            percepts.append('Stench')
        if self.grid[x][y] == 'G':
            percepts.append('Glitter')

        # Check adjacent cells for breeze and stench
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.grid[nx][ny] == 'P':
                    percepts.append('Breeze')
                if self.grid[nx][ny] == 'W':
                    percepts.append('Stench')

        return percepts

    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def remove_wumpus(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 'W':
                    self.grid[i][j] = ''
                    return

    def print_grid(self, agent_position):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == agent_position:
                    print('A', end=' ')
                else:
                    print(self.grid[i][j] if self.grid[i][j] else '.', end=' ')
            print()
        print()

class KB_Agent:
    def __init__(self, env):
        self.env = env
        self.position = (0, 0)
        self.kb = {}  # Knowledge base to store known facts
        self.visited = set()
        self.arrows = 1
        self.gold_collected = False
        self.path = []
        self.dangerous = set()

    def move(self, direction):
        x, y = self.position
        if direction == 'up':
            new_pos = (x-1, y)
        elif direction == 'down':
            new_pos = (x+1, y)
        elif direction == 'left':
            new_pos = (x, y-1)
        elif direction == 'right':
            new_pos = (x, y+1)

        if self.env.is_valid_position(*new_pos):
            self.position = new_pos
            self.update_kb(new_pos)
            self.path.append(new_pos)
            self.visited.add(new_pos)

    def update_kb(self, pos):
        percepts = self.env.get_percepts(*pos)
        self.kb[pos] = percepts
        if 'Glitter' in percepts:
            self.pick_up_gold()
        if 'Breeze' in percepts:
            self.mark_adjacent_as_dangerous(pos)

    def mark_adjacent_as_dangerous(self, pos):
        x, y = pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.env.is_valid_position(nx, ny):
                self.dangerous.add((nx, ny))

    def shoot_arrow(self):
        if self.arrows > 0:
            self.arrows -= 1
            print("Arrow shot!")
            self.env.remove_wumpus()
            # Update knowledge base to reflect that the Wumpus is dead
            for pos, percepts in self.kb.items():
                if 'Stench' in percepts:
                    percepts.remove('Stench')
            return True
        return False

    def pick_up_gold(self):
        if 'Glitter' in self.kb.get(self.position, []):
            self.gold_collected = True
            print("Gold collected!")
            return True
        return False

    def make_decision(self):
        # Explore unvisited, safe neighbors first
        x, y = self.position
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in self.visited and self.env.is_valid_position(nx, ny) and (nx, ny) not in self.dangerous:
                self.move_to(nx, ny)
                return

        # If all safe neighbors are visited, move to a random visited position
        if self.path:
            self.position = self.path.pop()

    def move_to(self, x, y):
        if x < self.position[0]:
            self.move('up')
        elif x > self.position[0]:
            self.move('down')
        elif y < self.position[1]:
            self.move('left')
        elif y > self.position[1]:
            self.move('right')

    def play_game(self):
        while not self.gold_collected:
            self.make_decision()
            self.env.print_grid(self.position)  # Print the board state after each move
            self.print_kb()
            if 'Stench' in self.kb[self.position]:
                self.shoot_arrow()
        print("Game over! Gold collected.")

    def print_kb(self):
        for pos, percepts in self.kb.items():
            print(f"Position {pos}: Percepts: {percepts}")

def test_agent():
    env = Environment(size=4)
    agent = KB_Agent(env)

    # Simulate agent playing the game
    agent.play_game()

test_agent()


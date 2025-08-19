import heapq
import itertools

class Puzzle:
    def __init__(self, f, c, g, w):
        self.f = f  # farmer
        self.c = c  # cabbage
        self.g = g  # goat
        self.w = w  # wolf

    def __eq__(self, other):
        return (self.f, self.c, self.g, self.w) == (other.f, other.c, other.g, other.w)

    def __hash__(self):
        return hash((self.f, self.c, self.g, self.w))

    def is_valid(self):
        # Goat with cabbage without farmer → invalid
        if (self.f != self.g) and (self.g == self.c):
            return False
        # Goat with wolf without farmer → invalid
        if (self.f != self.g) and (self.g == self.w):
            return False
        return True

    def __repr__(self):
        return f"Farmer:{self.f}, Cabbage:{self.c}, Goat:{self.g}, Wolf:{self.w}"


def move(state, item):
    """Move farmer and optionally one item."""
    new_state = Puzzle(state.f, state.c, state.g, state.w)
    new_pos = "right" if state.f == "left" else "left"

    if item == "c":
        new_state.c = new_pos
    elif item == "g":
        new_state.g = new_pos
    elif item == "w":
        new_state.w = new_pos

    new_state.f = new_pos
    return new_state


def heuristic(state, goal):
    """Heuristic: count how many are not yet at goal side."""
    return sum(getattr(state, x) != getattr(goal, x) for x in ["f", "c", "g", "w"])


def astar():
    """Solve puzzle using A* search with tie-breaker."""
    start = Puzzle("left", "left", "left", "left")
    goal = Puzzle("right", "right", "right", "right")

    counter = itertools.count()  # unique sequence numbers for tie-breaking
    frontier = [(heuristic(start, goal), 0, next(counter), start, [])]
    explored = set()

    while frontier:
        f, g, _, state, path = heapq.heappop(frontier)

        if state in explored:
            continue
        explored.add(state)

        if state == goal:
            return path + [state]

        for item in ["c", "g", "w", None]:
            new_state = move(state, item)
            if new_state.is_valid():
                new_g = g + 1
                new_f = new_g + heuristic(new_state, goal)
                heapq.heappush(frontier, (new_f, new_g, next(counter), new_state, path + [state]))
    return None
def play():
    """Interactive play mode."""
    print("\nCabbage, Goat, and Wolf Puzzle")
    print("Farmer must get all items across the river.")
    print("Commands: 'c' = cabbage, 'g' = goat, 'w' = wolf, 'n' = none")

    state = Puzzle("left", "left", "left", "left")
    goal = Puzzle("right", "right", "right", "right")

    while state != goal:
        print(state)
        move_item = input("What to move (c/g/w/n): ").strip().lower()

        if move_item not in ["c", "g", "w", "n"]:
            print("Invalid command! Use c/g/w/n.")
            continue

        state = move(state, None if move_item == "n" else move_item)

        if not state.is_valid():
            print("Invalid move! The goat gets eaten!")
            return

    print("🎉 Congratulations! You've solved the puzzle!")

if __name__ == "__main__":
    print("Auto-solving with A*...\n")
    solution = astar()
    if solution:
        for step in solution:
            print(step)
    else:
        print("No solution found.")

    print("\nNow try it yourself in interactive mode!")
    play()
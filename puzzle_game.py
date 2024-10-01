class puzzle:
    def __init__(self,f,c,g,w):
        #contructor initialising instance variables
        self.f=f
        self.c=c
        self.g=g
        self.w=w
    
    def __eq__(self,other):
        #check if current state is equal to goal state or not
        return(self.f,self.c,self.g,self.w) == (other.f,other.c,other.g,other.w)

    def __hash__(self):
        #provides hash value for the state
        return hash((self.f, self.c, self.g, self.w))

    def is_valid(self):
        #check if goat is not alone with either cabbage or wolf(absence of farmer)
        #illegal state
        if(self.f!=self.g) and (self.g==self.c or self.g==self.w):
            return False
        return True

    def __repr__(self):
        #represent a string representation for state
        return f"Farmer:{self.f}, Cabbage:{self.c}, Goat:{self.g}, Wolf:{self.w}"

def move(state, item):
    new_state = puzzle(state.f, state.c, state.g, state.w)
    new_pos ='right' if state.f=='left' else 'left'
    if item == 'c':
        new_state.c = new_pos
    elif item == 'g':
        new_state.g = new_pos
    elif item == 'w':
        new_state.w = new_pos

    new_state.f = new_pos
    return new_state
    
def solve():
    i_state = puzzle('right','right','right','right')
    g_state = puzzle('left','left','left','left')
    frontier = [(i_state,[])]
    #[] is empty set for path storage
    explored = set()
    while frontier:
        state,path = frontier.pop(0)
        if state in explored:
            continue
        explored.add(state)
        if state == g_state:
            return path+[state]
    for item in ['c', 'g', 'w', None]:
        new_state = move(state, item)
        if new_state.is_valid():
            frontier.append((new_state, path + [state]))
    return None
# MAIN
print("Cabbage, Goat, and Wolf Puzzle")
print("Farmer needs to get all items across the river.")
print("Commands: 'c:cabbage', 'g:goat', 'w:wolf', 'n:none'")

state = puzzle('left', 'left', 'left', 'left')
while state != puzzle('right', 'right', 'right', 'right'):
    print(state) 
    move_item = input("What to move: ").strip().lower()
    state = move(state, move_item)
    if not state.is_valid():
        print("Invalid move! You can't leave the goat alone with the cabbage or the wolf alone with the goat.")
        break
else:
    print("Congratulations! You've solved the puzzle.")

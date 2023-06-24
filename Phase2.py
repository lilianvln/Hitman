import hitman
from phase1-LV import *

# 0 = North
# 1 = East
# 2 = South
# 3 = West

plateau, points_parcours, point_garde_range = main()

def create_state0(plateau, N, M) :
    guards = []
    civils = []
    target = []
    empty = []
    wall = []
    suit = []
    piano = []
    for i in range (N-1) :
        for j in range (M-1) :
            if plateau[i][j] == HC.CIVIL_N :
                civils.append([(i, j), 0])
            elif plateau[i][j] == HC.CIVIL_E :
                civils.append([(i, j), 1])
            elif plateau[i][j] == HC.CIVIL_S :
                civils.append([(i, j), 2])
            elif plateau[i][j] == HC.CIVIL_W :
                civils.append([(i, j), 3])
            if plateau[i][j] == HC.GUARD_N :
                guards.append([(i, j), 0])
            elif plateau[i][j] == HC.GUARD_E :
                guards.append([(i, j), 1])
            elif plateau[i][j] == HC.GUARD_S :
                guards.append([(i, j), 2])
            elif plateau[i][j] == HC.GUARD_W :
                guards.append([(i, j), 3])
            elif plateau[i][j] == HC.TARGET :
                target.append((i, j))
            elif plateau[i][j] == HC.EMPTY :
                empty.append((i,j))
            elif plateau[i][j] == HC.WALL :
                wall.append((i,j))
            elif plateau[i][j] == HC.SUIT:
                suit.append((i, j))
            elif plateau[i][j] == HC.PIANO_WIRE :
                piano.append((i,j))


    state0 = {"hitman": [(0,0), 0],
              "empty" : empty,
              "target": target,
              "guards" : guards,
              "civils" : civils,
              "piano": piano,
              "suit": suit,
              "wall" : wall}

    return state0







def turn_clockwise(state) :
    orientation = state["hitman"][1]
    precond = 0<= orientation <=3
    if not precond :
        return None
    orientation +=1
    if orientation == 4 : orientation = 0
    state["hitman"][1] = orientation
    return state

def turn_anti_clockwise(state) :
    orientation = state["hitman"][1]
    precond = 0 <= orientation <= 3
    if not precond:
        return None
    orientation -= 1
    if orientation == -1: orientation = 0
    state["hitman"][1] = orientation
    return state


def case_ahead(x, y, orientation) :
    if orientation == (0 or 2) :
        x2 = x
        if orientation == 0 :
            y2 = y+1
        else :
            y2 = y-1
    elif orientation == (1 or 3) :
        y2 = y
        if orientation == 1:
            x2 = y + 1
        else:
            x2 = y - 1
    return x2, y2


def move(state, N, M) :
    x, y = state["hitman"][0]
    orientation = state["hitman"][1]
    x2, y2 = case_ahead(x, y, orientation)
    precond = ((x2, y2) not in state["wall"]) and (0<=x2<M) and (0<=y2<N)
    if not precond :
        return None
    for i in state["guards"] :
        if i[0] == (x2, y2) :
            return None
    state["hitman"][0] = (x2, y2)
    return state

def kill_target(state) :
    x, y = state["hitman"][0]
    xT, yT = state["target"]
    precond = ((xT, yT)==(x,y)) and (state["piano"] == None)
    if not precond :
        return None
    state["target"] = None
    return state

def opposite_number(num):
    if num == 0:
        return 2
    elif num == 1:
        return 3
    elif num == 2:
        return 0
    elif num == 3:
        return 1
    return None
def kill_guard(state) :
    x, y = state["hitman"][0]
    orientation = state["hitman"][1]
    x2, y2 = case_ahead(x, y, orientation)
    g = False
    for i in state["guards"] :
        if i[0] == (x2, y2) :
            g = True
            o = i[1]
    precond = g and (o != opposite_number(o) )
    if not precond :
        return None
    state["gards"].remove([(x2, y2), o])
    state["empty"].append((x2, y2))

def kill_civil(state) :
    x, y = state["hitman"][0]
    orientation = state["hitman"][1]
    x2, y2 = case_ahead(x, y, orientation)
    c = False
    for i in state["civils"] :
        if i[0] == (x2, y2) :
            c = True
            o = i[1]
    precond = c and (o != opposite_number(o) )
    if not precond :
        return None
    state["civils"].remove([(x2, y2), o])
    state["empty"].append((x2, y2))

def get_suit(state) :
    x, y = state["hitman"][0]
    precond = (x,y) == state["suit"][0]
    if not precond :
        return None
    state["empty"].append((x, y))
    state["suit"] = None

def get_piano(state) :
    x, y = state["hitman"][0]
    precond = (x, y) == state["piano"][0]
    if not precond:
        return None
    state["empty"].append((x, y))
    state["piano"] = "got"

def wear_suit(state) :
    precond = state["suit"] == "got"
    if not precond:
        return None
    state["suit"] == "wear"

def goal(state) :
    if (state["target"] == None) and (state["hitman"][0] == (0,0)) :
        return True
    return False
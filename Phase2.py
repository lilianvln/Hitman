import hitman
from phase1-LV import *
from queue import PriorityQueue

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
    for i in range (M-1) :
        for j in range (N-1) :
            if plateau[i][j] == HC.CIVIL_N :
                civils.append([(j, M-1-i), 0])
            elif plateau[i][j] == HC.CIVIL_E :
                civils.append([(j, M-1-i), 1])
            elif plateau[i][j] == HC.CIVIL_S :
                civils.append([(j, M-1-i), 2])
            elif plateau[i][j] == HC.CIVIL_W :
                civils.append([(j, M-1-i), 3])
            if plateau[i][j] == HC.GUARD_N :
                guards.append([(j, M-1-i), 0])
            elif plateau[i][j] == HC.GUARD_E :
                guards.append([(j, M-1-i), 1])
            elif plateau[i][j] == HC.GUARD_S :
                guards.append([(j, M-1-i), 2])
            elif plateau[i][j] == HC.GUARD_W :
                guards.append([(j, M-1-i), 3])
            elif plateau[i][j] == HC.TARGET :
                target.append((j, M-1-i))
            elif plateau[i][j] == HC.EMPTY :
                empty.append((j, M-1-i))
            elif plateau[i][j] == HC.WALL :
                wall.append((j, M-1-i))
            elif plateau[i][j] == HC.SUIT:
                suit.append((j, M-1-i))
            elif plateau[i][j] == HC.PIANO_WIRE :
                piano.append((j, M-1-i))


    state0 = {"hitman": [(0,0), 0],
              "empty" : empty,
              "target": target,
              "guards" : guards,
              "civils" : civils,
              "piano": piano,
              "suit": suit,
              "wall" : wall}

    return state0

#class State :










"""
class case :
    def __init__(self, position, g=0, h=0):
        self.position = position
        self.g = g  # Coût du chemin depuis le nœud initial
        self.h = h  # Estimation du coût restant pour atteindre le nœud final
        self.f = g + h  # Coût total f = g + h
        self.parent = None
def etoile(target, heuristique) :

    open = []
    close = []
    start = case((0,0), 0, heuristique[0][0])
    open.append(start)
    while open :
        current = open[0]
        for el in open :
            if el.f < current.f :
                current = el
        if current.position == target :
            break
        open.remove(current)
        close.add(current)
"""


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

class Noeud:
    def __init__(self, state, parent=None, cost_g=0, cost_h=0):
        self.state = state
        self.parent = parent
        self.cost_g = cost_g
        self.cost_h = cost_h
        self.cost_f = cost_g + cost_h

    def turn_clockwise(self, state):
        orientation = state["hitman"][1]
        precond = 0 <= orientation <= 3
        if not precond:
            return None
        orientation += 1
        if orientation == 4: orientation = 0
        state["hitman"][1] = orientation
        return state

    def turn_anti_clockwise(self, state):
        orientation = state["hitman"][1]
        precond = 0 <= orientation <= 3
        if not precond:
            return None
        orientation -= 1
        if orientation == -1: orientation = 0
        state["hitman"][1] = orientation
        return state


    def move(self, state, N, M):
        x, y = state["hitman"][0]
        orientation = state["hitman"][1]
        x2, y2 = case_ahead(x, y, orientation)
        precond = ((x2, y2) not in state["wall"]) and (0 <= x2 < M) and (0 <= y2 < N)
        if not precond:
            return None
        for i in state["guards"]:
            if i[0] == (x2, y2):
                return None
        state["hitman"][0] = (x2, y2)
        return state

    def kill_target(self, state):
        x, y = state["hitman"][0]
        xT, yT = state["target"]
        precond = ((xT, yT) == (x, y)) and (state["piano"] == None)
        if not precond:
            return None
        state["target"] = None
        return state


    def kill_guard(self, state):
        x, y = state["hitman"][0]
        orientation = state["hitman"][1]
        x2, y2 = case_ahead(x, y, orientation)
        g = False
        for i in state["guards"]:
            if i[0] == (x2, y2):
                g = True
                o = i[1]
        precond = g and (o != opposite_number(o))
        if not precond:
            return None
        state["gards"].remove([(x2, y2), o])
        state["empty"].append((x2, y2))

    def kill_civil(self, state):
        x, y = state["hitman"][0]
        orientation = state["hitman"][1]
        x2, y2 = case_ahead(x, y, orientation)
        c = False
        for i in state["civils"]:
            if i[0] == (x2, y2):
                c = True
                o = i[1]
        precond = c and (o != opposite_number(o))
        if not precond:
            return None
        state["civils"].remove([(x2, y2), o])
        state["empty"].append((x2, y2))

    def get_suit(self, state):
        x, y = state["hitman"][0]
        precond = (x, y) == state["suit"][0]
        if not precond:
            return None
        state["empty"].append((x, y))
        state["suit"] = None

    def get_piano(self, state):
        x, y = state["hitman"][0]
        precond = (x, y) == state["piano"][0]
        if not precond:
            return None
        state["empty"].append((x, y))
        state["piano"] = "got"

    def wear_suit(self, state):
        precond = state["suit"] == "got"
        if not precond:
            return None
        state["suit"] == "wear"


def goal(state):
    if (state["target"] == None) and (state["hitman"][0] == (0, 0)):
        return True
    return False

def case_ahead(x, y, orientation):
    if orientation == (0 or 2):
        x2 = x
        if orientation == 0:
            y2 = y + 1
        else:
            y2 = y - 1
    elif orientation == (1 or 3):
        y2 = y
        if orientation == 1:
            x2 = y + 1
        else:
            x2 = y - 1
    return x2, y2
"""
def heuristique(plateau, N, M, target):
    x, y = target
    h = []
    ligne = 0
    for i in range(M - 1, 0, -1):
        for j in range(N - 1):
            if plateau[i][j] == (HC.WALL or HC.GUARD_E or HC.GUARD_N or HC.GUARD_S or HC.GUARD_W):
                h[ligne].append((i - y) + abs(j - x))
            else:
                h[ligne].append(None)
        ligne += 1
    return h
"""

def heurisitque(state) :
    return h_turn(state) + h_move(state)


def h_turn(state) : # calcul de l'heuristique pour tourner
    xT, yT = state["target"][0]
    xH, yH = state["hitman"][0]
    h = 0
    if state["hitman"][1] == 0:  # hitman orienté nord
        if not (xH == xT and yT >= yH) :
            h += 1
            if yT < yH :
                h +=1
    elif state["hitman"][1] == 1:  # hitman orienté est
        if not (yH == yT and xT >= xH) :
            h += 1
            if xT < xH :
                h +=1
    elif state["hitman"][1] == 2:  # hitman orienté sud
        if not (xH == xT and yT <= yH) :
            h += 1
            if yT > yH :
                h +=1
    elif state["hitman"][1] == 3:  # hitman orienté ouest
        if not (yH == yT and xT <= xH) :
            h += 1
            if xT > xH :
                h +=1
    else :
        return None
    return h

def h_move(state) : #calcul de l'heuristique pour avancer
    xT, yT = state["target"][0]
    xH, yH = state["hitman"][0]
    return abs(xT-xH) + abs(yT-yH)


def initial_node(state, h, N, M) :
    node0 = Noeud(create_state0(plateau,N,M))
    return node0

def generate_children(node) :
    childrens = []
    state = node.state
    g = node.cost_g
    state_after_action = [node.turn_clockwise(state), node.turn_anti_clockwise(state), node.move(state), node.kill_civil(state),
                          node.kill_guard(state), node.kill_target(state), node.get_suit(state), node.get_piano(state), node.wear_suit]
    for i in range (9) :
        noeud = Noeud(state_after_action[i], node) #, g+1, heurisitque(state_after_action[i]))
        if noeud :
            childrens.append(noeud)
    return childrens

def astar(node0):
    open = []
    closed = []

    open.append(node0)

    while not open.empty():
        current = open[0]
        for el in open :
            if el.cost_f < current.cost_f :
                current = el

        if goal(current.state): # l'étant courant est l'état final
            path = []
            while current is not None:
                path.append(current.state)
                current = current.parent
            path.reverse()
            return path # retourne une liste d'états correspondant au chemin le plus efficace

        closed.add(current.state)

        children = generate_children(current) # tous les mouvement possibles

        for child in children:
            if not (child in closed) :
                if not (child in open) :
                    open.append(child)
                    child.cost_g = current.cost_g + 1
                    child.cost_h = heurisitque(child.state)
                    child.cost_f = child.cost_g + child.cost_h
                else :
                    if child.cost_g > (current.cost_g +1) :
                        child.cost_g = current.cost_g + 1
                    if child.cost_h > heurisitque(child.state) :
                        child.cost_h = heurisitque(child.state)
                    child.cost_f = child.cost_g + child.cost_h

    return None  # Aucun chemin trouvé


import hitman
from phase1LV import *
from queue import PriorityQueue

# 0 = North
# 1 = East
# 2 = South
# 3 = West

plateau, points_parcours, point_garde_range = main()

def create_state0(plateau, N, M) :
    guards = []
    guards_range = []
    civils = []
    civil_range =[]
    target = []
    empty = []
    wall = []
    suit = []
    piano = []
    M = M-1
    N = N-1
    for i in range (M+1) :
        for j in range (N+1) :
            if plateau[i][j] == HC.CIVIL_N :
                civils.append([(j, M-i), 0])
                if M-i+1 <= M :
                    civil_range.append((j, M-i+1))
            elif plateau[i][j] == HC.CIVIL_E :
                civils.append([(j, M-i), 1])
                if j+1 <= N :
                    civil_range.append((j+1, M-i))
            elif plateau[i][j] == HC.CIVIL_S :
                civils.append([(j, M-i), 2])
                if (i+1) <= M :
                    civil_range.append((j, M-i-1))
            elif plateau[i][j] == HC.CIVIL_W :
                civils.append([(j, M-i), 3])
                if j-1 >= 0 :
                    civil_range.append((j-1, M-i))
            elif plateau[i][j] == HC.GUARD_N :
                guards.append([(j, M-i), 0])
                if M - i + 1 <= M:
                    guards_range.append((j, M - i + 1))
                if M - i + 2 <= M:
                    guards_range.append((j, M - i + 2))
            elif plateau[i][j] == HC.GUARD_E :
                guards.append([(j, M-i), 1])
                if j+1 <= N :
                    guards_range.append((j+1, M-i))
                if j+2 <= N :
                    guards_range.append((j+2, M-i))
            elif plateau[i][j] == HC.GUARD_S :
                guards.append([(j, M-i), 2])
                if (i+1) <= M :
                    guards_range.append((j, M-i-1))
                if (i+2) <= M:
                    guards_range.append((j, M - i - 2))
            elif plateau[i][j] == HC.GUARD_W :
                guards.append([(j, M-i), 3])
                if j - 1 >= 0:
                    guards_range.append((j - 1, M - i))
                if j - 2 >= 0:
                    guards_range.append((j - 2, M - i))
            elif plateau[i][j] == HC.TARGET :
                target.append((j, M-i))
            elif plateau[i][j] == HC.EMPTY :
                empty.append((j, M-i))
            elif plateau[i][j] == HC.WALL :
                wall.append((j, M-i))
            elif plateau[i][j] == HC.SUIT:
                suit.append((j, M-i))
            elif plateau[i][j] == HC.PIANO_WIRE :
                piano.append((j, M-i))


    state0 = {"hitman": [(0,0), 0],
              "empty" : empty,
              "target": target,
              "guards" : guards,
              "guard_range" : guards_range, # liste des cases vues par un gardes
              "civils" : civils,
              "civil_range" : civil_range, # liste des cases vues par un gardes
              "piano": piano,
              "suit": suit,
              "wall" : wall,
              "action" : None}

    return state0


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
        state["action"] = "turn_clockwise"
        pena = 1
        return state, pena

    def turn_anti_clockwise(self, state):
        orientation = state["hitman"][1]
        precond = 0 <= orientation <= 3
        if not precond:
            return None
        orientation -= 1
        if orientation == -1: orientation = 0
        state["hitman"][1] = orientation
        pena = 1
        state["action"] = "turn_anti_clockwise"
        return state, pena


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
        pena = 1,
        if (x,y) in state["guards_range"] :
            pena += 5
        state["action"] = "move"
        return state, pena

    def kill_target(self, state):
        x, y = state["hitman"][0]
        xT, yT = state["target"]
        precond = ((xT, yT) == (x, y)) and (state["piano"] == None)
        if not precond:
            return None
        state["target"] = None
        pena = 1
        if (x,y) in state["guard_range"] :
            pena += 100
        if (x,y) in state["civil_range"] :
            pena += 100
        state["action"] = "kill_target"
        return state, pena


    def kill_guard(self, state):
        x, y = state["hitman"][0]
        orientation = state["hitman"][1]
        x2, y2 = case_ahead(x, y, orientation)
        g = False
        for i in state["guards"]:
            if i[0] == (x2, y2):
                g = True
                o = i[1]
        precond = g and (orientation != opposite_number(o))
        if not precond:
            return None

        #supprime les cases qui étaient regardées par le garde
        xA, yA = case_ahead(x2, y2, o)
        if (xA, yA) in state["gards_range"] :
            state["gards_range"].remove((xA, yA))
        xA, yA = case_ahead(xA, yA, o)
        if (xA, yA) in state["gards_range"]:
            state["gards_range"].remove((xA, yA))


        state["gards"].remove([(x2, y2), o])
        state["empty"].append((x2, y2))

        pena = 21 # 1 point d'action + 20 point pour personne neutralisée
        if (x,y) in state["guard_range"] :
            pena += 100
        if (x,y) in state["civil_range"] :
            pena += 100
        state["action"] = "kill_guard"
        return state, pena

    def kill_civil(self, state):
        x, y = state["hitman"][0]
        orientation = state["hitman"][1]
        x2, y2 = case_ahead(x, y, orientation)
        c = False
        for i in state["civils"]:
            if i[0] == (x2, y2):
                c = True
                o = i[1]

        precond = c and (orientation != opposite_number(o))
        if not precond:
            return None

        # supprime les cases qui étaient regardées par le civil
        xA, yA = case_ahead(x2, y2, o)
        if (xA, yA) in state["civil_range"]:
            state["civil_range"].remove((xA, yA))

        state["civils"].remove([(x2, y2), o])
        state["empty"].append((x2, y2))

        pena = 21  # 1 point d'action + 20 point pour personne neutralisée
        if (x, y) in state["guard_range"]:
            pena += 100
        if (x, y) in state["civil_range"]:
            pena += 100

        state["action"] = "kill_civil"
        return state, pena

    def get_suit(self, state):
        x, y = state["hitman"][0]
        precond = (x, y) == state["suit"][0]
        if not precond:
            return None
        state["empty"].append((x, y))
        state["suit"] = None
        pena = 1
        state["action"] = "get_suit"
        return state, pena

    def get_piano(self, state):
        x, y = state["hitman"][0]
        precond = (x, y) == state["piano"][0]
        if not precond:
            return None
        state["empty"].append((x, y))
        state["piano"] = "got"
        pena = 1
        state["action"] = "get_piano"
        return state, pena

    def wear_suit(self, state):
        x, y = state["hitman"][0]
        precond = state["suit"] == "got"
        if not precond:
            return None
        state["suit"] == "wear"
        pena = 1
        if (x, y) in state["guard_range"]:
            pena += 100
        if (x, y) in state["civil_range"]:
            pena += 100
        state["action"] = "wear_suit"
        return state, pena


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


def initial_node(plateau, N, M) :
    node0 = Noeud(create_state0(plateau,N,M))
    return node0

def generate_children(node) :
    childrens = []
    state = node.state
    g = node.cost_g
    state_after_action = [node.turn_clockwise(state), node.turn_anti_clockwise(state), node.move(state), node.kill_civil(state),
                          node.kill_guard(state), node.kill_target(state), node.get_suit(state), node.get_piano(state), node.wear_suit]
    for i in range (9) :
        state_i, pena = state_after_action[i]
        noeud = Noeud(state_i, node, g+pena, heurisitque(state_i))
        if noeud :
            childrens.append(noeud)
    return childrens

def a_star(node0):
    open = []
    closed = []

    open.append(node0)

    while not open.empty():
        current = open[0]
        for el in open :
            if el.cost_f < current.cost_f :
                current = el

        if goal(current.state): # l'état courant est l'état final
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
                child.cost_f = child.cost_g + child.cost_h
                if not (child in open) :
                    open.append(child)
                else :
                    if child.cost_g > (current.cost_g +1) :
                        child.cost_g = current.cost_g + 1
                    if child.cost_h > heurisitque(child.state) :
                        child.cost_h = heurisitque(child.state)
                    child.cost_f = child.cost_g + child.cost_h

    return None  # Aucun chemin trouvé

def state_to_action(path, hr) :
    for mov in path :
        if mov.state["action"] == "turn_clockwise" :
            hr.turn_clockwise()
        if mov.state["action"] == "turn_anti_clockwise":
            hr.turn_anti_clockwise()
        if mov.state["action"] == "move":
            hr.move()
        if mov.state["action"] == "kill_target":
            hr.kill_target()
        if mov.state["action"] == "kill_guard":
            hr.neutralize_guard()
        if mov.state["action"] == "kill_civil":
            hr.neutralize_civil()
        if mov.state["action"] == "get_suit":
            hr.take_suit()
        if mov.state["action"] == "get_piano":
            hr.take_weapon()
        if mov.state["action"] == "wear_suit":
            hr.put_on_suit()


hr = HitmanReferee()
b, score, history, map = hr.end_phase1()
print (map)
#state0 = create_state0(map, M, N)


# def parcours(path) :
    #fonction qui effectue le parcours le plus efficace

# def return_to_0()
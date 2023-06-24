from typing import List, Tuple, Dict
from itertools import combinations
from hitman import *
import subprocess
from pprint import pprint
import random

# alias de types
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
Coordinates = Tuple[int, int]
ListCoordinates = List[Coordinates]


def cell_to_variable(m: int, n: int, i: int, j: int, val: int) -> int:
    # Check that the input coordinates are within bounds
    if i < 0 or i >= n or j < 0 or j >= m:
        raise ValueError("Invalid cell coordinates", (i, j))
    # Compute the unique index of the cell
    cell_index = j*n + i if n > m else i*m + j
    # Compute the unique index of the variable
    var_index = cell_index*13 + val
    # Return the variable index
    return var_index

def variable_to_cell(var: int, m: int, n: int) -> Dict[Tuple[int, int], HC]:
    # Compute the cell index and value from the variable index
    cell_index, val = divmod(var, 13)
    # Compute the row and column indices from the cell index
    if val == 0:
        val = 13
        cell_index -= 1
    if n > m:
        j, i = divmod(cell_index, n)
    else:
        i, j = divmod(cell_index, m)
    # Create a dictionary mapping the cell coordinates to the value
    cell_dict = {(i, j): HC(val)}
    # Return the dictionary
    return cell_dict

def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    """Return a clause that is true if at least one of the variables is true"""
    return variables[:]

def at_most_one(variables: List[PropositionnalVariable]) -> ClauseBase:
    """Return a clause base that is true if at most one of the variables is true"""
    return [[-x, -y] for x, y in combinations(variables, 2)]

def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    """Return a clause base that is true if exactly one of the variables is true"""
    return [at_least_one(variables)] + at_most_one(variables)


def at_least_x(x: int, vars: list[int]):
    clauses = []
    for c in combinations(vars, len(vars)-(x-1)):
        clauses.append(list(c))
    return clauses

#retourne l'ensemble de clause traitant la contrainte : "au plus n variables vraies dans la liste"
def at_most_x(x: int, vars: list[int]):
    clauses = []
    varsNeg = [-i for i in vars]
    for c in combinations(varsNeg, x+1):
        clauses.append(list(c))
    return clauses

#retourne l'ensemble de clause traitant la contrainte : "exactement n variables vraies dans la liste" (appeler la fonction avec GUARD_N ou CIVIL_N)
def exactly_x(m: int, n: int, x: int, item: HC):
    vars = []
    for i in range(n):
        for j in range(m):
            for val in range(item.value, item.value + 4):
                vars.append(cell_to_variable(m, n, i, j, val))
    # print("\n\n")
    # print(vars)

    if vars == []:
        return []
    if x==0:
        return at_most_x(0, vars)
    if x==len(vars):
        return at_least_x(x, vars)
    clauses = at_most_x(x, vars)
    clauses += at_least_x(x, vars)
    return clauses



def insert_uniques_rule(m: int, n: int, item: HC) -> ClauseBase:
    """Inserts the uniques rule in a Clause Base"""
    clauses = []
    for i in range(n):
        for j in range(m):
            clauses.append(cell_to_variable(m, n, i, j, item.value))

    return unique(clauses)


def insert_only_one_per_case_rule(m: int, n: int) -> ClauseBase:
    """Create the rules that says that there is only one item/person per case"""
    clauses = []
    for i in range(n):
        for j in range(m):
            clauses += (unique([cell_to_variable(m, n, i, j, val) for val in range(1,14)]))
    return clauses



def add_vision_to_clause_base(status: Dict) -> List[int]:
    """Add the vision rules to a clause base"""
    ### 'vision': [((4, 4), <HC.EMPTY: 1>), ((4, 5), <HC.GUARD_S: 5>)]}
    m = status["m"]
    n = status["n"]
    vision = status["vision"]
    vision_clauses = [cell_to_variable(m, n, case[0][0], case[0][1], case[1].value) for case in vision]
    return vision_clauses


def add_vision_to_explored_cases(status: Dict) -> List[int]:
    """Add the vision to a explored cases"""
    ### 'vision': [((4, 4), <HC.EMPTY: 1>), ((4, 5), <HC.GUARD_S: 5>)]}

    vision = status["vision"]
    vision_base = [c[0] for c in vision]
    return vision_base



def generate_problem(status: Dict) -> ClauseBase:
    """Generate a problem from a grid"""
    m = status["m"]
    n = status["n"]

    # x_guard = status["guard_count"]
    # x_civil = status["civil_count"]

    clauses = []
    clauses += insert_uniques_rule(m, n, HC.TARGET)  # One target on the map
    clauses += insert_uniques_rule(m, n, HC.PIANO_WIRE)  # One piano wire on the map
    clauses += insert_uniques_rule(m, n, HC.SUIT)  # One suit on the map
    clauses += insert_only_one_per_case_rule(m, n)  # Only one item/person per case
    # clauses += exactly_x(m, n, x_guard, HC.GUARD_N) # Un seul garde nord sur la carte
    # clauses += exactly_x(m, n, x_civil, HC.CIVIL_N) # Un seul garde sud sur la carte

    # Player's position and orientation
    # pos = status["position"]
    # orientation = status["orientation"]

    # # Add player's position to vision clauses
    # vision = status["vision"]
    # vision_clauses = [cell_to_variable(m, n, case[0][0], case[0][1], case[1].value) for case in vision]
    # vision_clauses.append(cell_to_variable(m, n, pos[0], pos[1], orientation.value))

    return clauses


# def get_next_position(pos: Tuple[int, int], direction: HC) -> Tuple[int, int]:
#     """Get the next position based on the current position and direction"""
#     if direction == HC.N:
#         return pos[0], pos[1] + 1
#     elif direction == HC.E:
#         return pos[0] + 1, pos[1]
#     elif direction == HC.S:
#         return pos[0], pos[1] - 1
#     elif direction == HC.W:
#         return pos[0] - 1, pos[1]


def is_valid_position(pos: Tuple[int, int], m: int, n: int) -> bool:
    #print(pos, m, n)
    """Check if the position is within the grid bounds"""
    return 0 <= pos[0] < n and 0 <= pos[1] < m

def add_guard_vision(status: Dict) -> List[Coordinates]:
    """Add the vision of the guards to the list of non safe cases"""
    unsafe_cases = []
    for case, object in status["vision"]:
        if object == HC.GUARD_S:
            unsafe_cases.extend([(case[0], case[1]-i) for i in range(3)])
        elif object == HC.GUARD_N:
            unsafe_cases.extend([(case[0], case[1]+i) for i in range(3)])
        elif object == HC.GUARD_E:
            unsafe_cases.extend([(case[0]+i, case[1]) for i in range(3)])
        elif object == HC.GUARD_W:
            unsafe_cases.extend([(case[0]-i, case[1]) for i in range(3)])

    return unsafe_cases

def exec_gophersat(filename: str, cmd: str = "ia02_p23/gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run([cmd, filename], capture_output=True, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]



def write_dimacs_file(clauses: ClauseBase, nb_vars: int, filename: str) -> None:
    with open(filename, "w", newline="") as cnf:
        cnf.write(f"p cnf {nb_vars} {len(clauses)}\n")
        for clause in clauses:
            cnf.write(" ".join([str(x) for x in clause]) + " 0\n")



def is_unexplored_or_safe(direction: str, status: Dict, explored_cases: ListCoordinates, vision_clauses: ClauseBase, unsafe_cases : ListCoordinates) -> bool:
    m = status["m"]
    n = status["n"]
    x, y = status["position"]
    orientation = status["orientation"]
    if direction == 'left':
        if orientation == HC.N:
            x, y = x - 1, y
        elif orientation == HC.E:
            x, y = x, y + 1
        elif orientation == HC.S:
            x, y = x + 1, y
        elif orientation == HC.W:
            x, y = x, y - 1
    elif direction == 'right':
        if orientation == HC.N:
            x, y = x + 1, y
        elif orientation == HC.E:
            x, y = x, y - 1
        elif orientation == HC.S:
            x, y = x - 1, y
        elif orientation == HC.W:
            x, y = x, y + 1
    else: ## front
        if orientation == HC.N:
            x, y = x, y + 1
        elif orientation == HC.E:
            x, y = x + 1, y
        elif orientation == HC.S:
            x, y = x, y - 1
        elif orientation == HC.W:
            x, y = x - 1, y
    if not is_valid_position((x, y), status["m"], status["n"]): return False
    clauses = generate_problem(status)
    guard_variables = [[- cell_to_variable(status["m"], status["n"], x, y, guard.value)] for guard in [HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]]
    wall = [ - cell_to_variable(m, n, x, y, HC.WALL.value)]
    clauses.extend(vision_clauses)
    clauses.extend(guard_variables)
    clauses.extend([wall])
    write_dimacs_file(clauses, m*n*13, "ia02_p23/test.cnf")
    is_sat, _ = exec_gophersat("ia02_p23/test.cnf")

    return ((x, y) not in explored_cases) and is_sat and ((x, y) not in unsafe_cases)

def update_vision_and_unsafe_case(status: Dict, vision_clauses, unsafe_cases) -> Tuple[ClauseBase, ListCoordinates]:
    vision_clauses.extend([[var] for var in add_vision_to_clause_base(status) if [var] not in vision_clauses])
    unsafe_cases.extend([case for case in add_guard_vision(status) if case not in unsafe_cases])
    return vision_clauses, unsafe_cases

def explore_map(status: Dict) -> Tuple[ClauseBase, Dict]:
    # Initialize variables
    explored_cases = []
    vision_clauses = [[cell_to_variable(status["m"], status["n"], status["position"][0], status["position"][1], HC.EMPTY.value)]]
    unsafe_cases = []
    path = []


    vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
    # Move forward initially
    status = hr.move()
    vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
    explored_cases.append(status["position"])


    # Continue exploring until all cases are explored
    while len(path) < status["m"] * 2 + status["n"] * 2 :
        print(status["position"])
        # Check conditions in order
        if is_unexplored_or_safe('left', status, explored_cases, vision_clauses, unsafe_cases):
            try:
                status = hr.turn_anti_clockwise()
                vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
                status = hr.move()
                if status["status"] != "OK": raise Exception("Error")
            except Exception as e:
                print(e, status["position"], status["orientation"])
                status = hr.turn_clockwise()

        elif is_unexplored_or_safe('front', status, explored_cases, vision_clauses, unsafe_cases):
            try:
                status = hr.turn_clockwise()
                vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
                status = hr.turn_anti_clockwise()
                vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
                status = hr.move()
            except Exception as e:
                print(e, status["position"], status["orientation"])
                status = hr.turn_anti_clockwise()

        elif is_unexplored_or_safe('right', status, explored_cases, vision_clauses, unsafe_cases):
            try:
                status = hr.turn_clockwise()
                vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
                status = hr.move()
            except Exception as e:
                print(e, status["position"])
                status = hr.turn_anti_clockwise()

        else:
            status = hr.turn_anti_clockwise()
            status = hr.turn_anti_clockwise()
            explored_cases.clear()

        # Update unsafe cases and explored cases
        vision_clauses, unsafe_cases = update_vision_and_unsafe_case(status, vision_clauses, unsafe_cases)
        path.append(status["position"])
        if status["position"] not in explored_cases:
            explored_cases.append(status["position"])
        # print(len(path), path)
        # print("Unsafe: ", unsafe_cases)

        # pprint(status)
        #print(explored_cases)
        #print(len(vision_clauses), vision_clauses)
        print(vision_clauses)

    return vision_clauses, status




hr = HitmanReferee()
vision_clauses = []
unsafe_cases = []
cases_seen = []
status = hr.start_phase1()
pprint(status)
#print(status["civil_count"])
m = status["m"]
n = status["n"]

clauses = generate_problem(status)
write_dimacs_file(clauses, m*n*13, "ia02_p23/test.cnf")
print("OK")
#print(explore_maze(status))
vision_clauses, status = explore_map(status)

# vision_clauses.extend([[var] for var in add_vision_to_clause_base(status) if [var] not in vision_clauses])
# print(vision_clauses)
# guard_variables = [[- cell_to_variable(status["m"], status["n"], 0, 1, guard.value)] for guard in [HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]]
# print(guard_variables)

# print(variable_to_cell(94, status["m"], status["n"]))
# print(cell_to_variable(status["m"], status["n"], 0, 1, HC.GUARD_N.value))

clauses.extend(vision_clauses)
# clauses.extend(guard_variables)
write_dimacs_file(clauses, m*n*13, "ia02_p23/test.cnf")


final_map = {}
bo, result = exec_gophersat("ia02_p23/test.cnf")
print(bo, result)
for x in result:
    if x > 0:
        print(x, variable_to_cell(x, status["m"], status["n"]))
        final_map.update(variable_to_cell(x, status["m"], status["n"]))


#pprint(final_map)
pprint(hr.send_content(final_map))
print("pénalités :", status["penalties"])

print(hr.end_phase1())

status = hr.start_phase2()
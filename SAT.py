import itertools

from hitman import *
from itertools import *

#pour chaque case on a 4(garde)+4(civil)+1(mur)+1(corde de piano)+1(costume)+1(vide)+1(cible) = 13 variables
# donc N*M*13 variables au total
# 0 -> case (0,0) vide
# 1, 2, 3, 4 -> garde dans la case (0;0)
# 5, 6, 7, 8 -> garde dans la case (0;0)
#(N, E, S, W)
# 9 -> mur dans la case (0;0)
# 10 -> corde de piano dans la case (0;0)
# 11 -> costume dans la case (0;0)
# 12 -> cible dans la case (0;0)

def var_vide(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(13*i + 13*j)
    return res

def var_civilN(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(13*i + 13*j + 1)
    return res

def var_civilE(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(13*i + 13*j + 2)
    return res

def var_civilS(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(13*i + 13*j + 3)
    return res

def var_civilW(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 4)
    return res

def var_guardN(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 5)
    return res

def var_guardE(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 6)
    return res

def var_guardS(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 7)
    return res

def var_guardW(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 8)
    return res

def var_mur(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 19)
    return res
def var_corde(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 10)
    return res
def var_costume(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 11)
    return res

def var_cible(N, M) :
    res = []
    for i in range (N) :
        for j in range (M) :
            res.append(12*i + 12*j + 12)
    return res
def varToCell(M, N, var):
    ligne = var // N
    colonne = var % N
    return ligne, colonne


def cellToVar(M, N, ligne, colonne):
    var = ligne * N + colonne
    return var

def varGarde(M,N) :
    res = []
    est = var_guardE(N, M)
    nord = var_guardN(N,M)
    sud = var_guardS(N,M)
    ouest = var_guardW(N, M)
    for i in range (N*M) :
        res.append(nord[i])
        res.append(est[i])
        res.append(sud[i])
        res.append(ouest[i])
    return res

def varCivil(N, M) :
    res = []
    for i in var_civilN(N, M):
        res.append(i)
    for i in var_civilE(N, M):
        res.append(i)
    for i in var_civilS(N, M):
        res.append(i)
    for i in var_civilW(N, M):
        res.append(i)
    return res

#status = hr.start_phase1()
def nb_cases(status) :
    nb = status["n"]*status["m"]
    return nb

def nb_gardes(status) :
    return status["guard_count"]

def nb_civils(status) :
    return status["civil_count"]

def position(status) :
    return status["position"]

def at_least_one(var):
    return var

def position_to_num_case(x, y, N) :
    return N*y+x
def unique_element_par_case_i(x, y, N) :
    #retourne une liste de clauses il y a un unique element dans cette case
    res = []
    case = position_to_num_case(x, y, N)
    numVar = case*12
    for i in range (numVar, numVar+12) :
        list.append(i)
    res = unique(i)
    return res

def unique_element_par_case_plateau(N, M) :
    #retourne une liste de clauses : un seul élément oar case du plateau
    res = []
    for i in range (N) :
        for j in range (M) :
            for case in unique_element_par_case_i(i, j, N) :
                res.append(case)
    return res

"""
def garde_unique_direction(N, M) : # déja fait avec le unique élément par case
    var = varGarde(M, N)
    res = []
    for i in range (N*M) :
        list = var[i : i+3]
        for j in unique(list) :
            res.append(j)
    return res
"""

#def clauses_nb_gardes(N, M, nb) :

def unique(listVar) :
    res = []
    res.append(listVar)
    for i in range(len(listVar)):
        for j in range(i + 1, len(listVar)):
            res.append([-listVar[i], -listVar[j]])
    return res

def unique_corde(N, M) :
    return unique(var_corde(N,M))

def unique_costume(N, M) :
    return unique(var_costume(N,M))

def unique_cible(N, M) :
    return unique(var_cible(N,M))

def exactement_nb_vraies(liste, nb):
    num_variables = len(liste)
    res = []

    # Au moins cinq variables doivent être vraies
    res.append([liste[i] for i in range(num_variables)])

    # Au plus cinq variables peuvent être vraies
    for i in range(num_variables):
        for j in range(i + 1, num_variables):
            res.append([-liste[i], -liste[j]])

    # Exactement cinq variables doivent être vraies
    combinations = itertools.combinations(liste, nb)
    for combination in combinations:
        res.append(list(combination))

    return res

def exactement_nb_gardes(nb, N, M) :
    liste = varGarde(N, M)
    return exactement_nb_vraies(liste, nb)

def exactement_nb_civils(nb, N, M) :
    liste = varCivil(N, M)
    return exactement_nb_vraies(liste, nb)

def vision_to_dimacs(x, y, vue, N, M) :
    case = position_to_num_case(x, y, N)
    if vue == HC.EMPTY :
        return var_vide(N,M)[case]
    if vue == HC.CIVIL_E :
        return var_civilE(N, M)[case]
    if vue == HC.CIVIL_N :
        return var_civilN(N, M)[case]
    if vue == HC.CIVIL_S :
        return var_civilN(N, M)[case]
    if vue == HC.CIVIL_W:
        return var_civilN(N, M)[case]
    if vue == HC.GUARD_E :
        return var_guardE(N, M)[case]
    if vue == HC.GUARD_N :
        return var_guardN(N, M)[case]
    if vue == HC.GUARD_W :
        return var_guardW(N, M)[case]
    if vue == HC.GUARD_S :
        return var_guardS(N, M)[case]
    if vue == HC.PIANO_WIRE :
        return var_corde(N, M)[case]
    if vue == HC.SUIT :
        return var_costume(N, M)[case]
    if vue == HC.WALL :
        return var_mur(N, M)[case]
    if vue == HC.TARGET :
        return var_cible(N, M)[case]

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

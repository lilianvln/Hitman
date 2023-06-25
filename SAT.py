import itertools
import os
from hitman import *


# pour chaque case on a 4(garde)+4(civil)+1(mur)+1(corde de piano)+1(costume)+1(vide)+1(cible) = 13 variables
# donc N*M*13 variables au total
# 1 -> case (0,0) vide
# 2, 3, 4, 5 -> garde dans la case (0;0)
# 6, 7, 8, 9 -> garde dans la case (0;0)
# (N, E, S, W)
# 10 -> mur dans la case (0;0)
# 11 -> corde de piano dans la case (0;0)
# 12 -> costume dans la case (0;0)
# 13 -> cible dans la case (0;0)

def var_vide(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 1)
    return res


def var_civilN(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 2)
    return res


def var_civilE(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 3)
    return res


def var_civilS(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 4)
    return res


def var_civilW(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 5)
    return res


def var_guardN(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 6)
    return res


def var_guardE(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 7)
    return res


def var_guardS(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 8)
    return res


def var_guardW(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 9)
    return res


def var_mur(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 10)
    return res


def var_corde(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 11)
    return res


def var_costume(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 12)
    return res


def var_cible(N, M):
    res = []
    for i in range(N):
        for j in range(M):
            res.append(13 * (i * M + j) + 13)
    return res


def varToCell(M, N, var):
    ligne = var // N
    colonne = var % N
    return ligne, colonne


def cellToVar(M, N, ligne, colonne):
    var = ligne * N + colonne
    return var


def varGarde(N, M):
    res = []
    est = var_guardE(N, M)
    nord = var_guardN(N, M)
    sud = var_guardS(N, M)
    ouest = var_guardW(N, M)
    for i in range(N * M):
        res.append(nord[i])
        res.append(est[i])
        res.append(sud[i])
        res.append(ouest[i])
    return res


def varCivil(N, M):
    res = []
    est = var_civilE(N, M)
    nord = var_civilN(N, M)
    sud = var_civilS(N, M)
    ouest = var_civilW(N, M)
    for i in range(N * M):
        res.append(nord[i])
        res.append(est[i])
        res.append(sud[i])
        res.append(ouest[i])
    return res


# status = hr.start_phase1()
def nb_cases(status):
    nb = status["n"] * status["m"]
    return nb


def position_to_num_case(x, y, M):
    return M * y + x


def unique_element_par_case_i(x, y, M):
    # retourne une liste de clauses avec au moins un élément dans cette case
    case = position_to_num_case(x, y, M)
    res = []
    clause = [13 * case + var for var in range(1, 14)]
    res.append(clause)
    return res


def unique_element_par_case_plateau(N, M):
    # retourne une liste de clauses : au moins un élément par case du plateau
    res = []
    for i in range(N):
        for j in range(M):
            for case in unique_element_par_case_i(i, j, M):
                res.append(case)
    return res


def unique(listVar):
    res = []
    res.append(listVar)
    for i in range(len(listVar)):
        for j in range(i + 1, len(listVar)):
            res.append([-listVar[i], -listVar[j]])
    return res


def unique_corde(N, M):
    return unique(var_corde(N, M))


def unique_costume(N, M):
    return unique(var_costume(N, M))


def unique_cible(N, M):
    return unique(var_cible(N, M))


def exactement_nb_vraies(liste, nb):
    num_variables = len(liste)
    res = []

    # Au moins nb variables doivent être vraies
    res.append([liste[i] for i in range(num_variables)])

    # Au plus nb variables peuvent être vraies
    for i in range(num_variables):
        for j in range(i + 1, num_variables):
            res.append([-liste[i], -liste[j]])

    # Exactement nb variables doivent être vraies
    combinations = itertools.combinations(liste, nb)
    for comb in combinations:
        clause = [-var for var in liste if var not in comb]
        res.append(clause)

    return res


def exactement_nb_gardes(nb, N, M):
    liste = varGarde(N, M)
    return exactement_nb_vraies(liste, nb)


def exactement_nb_civils(nb, N, M):
    liste = varCivil(N, M)
    return exactement_nb_vraies(liste, nb)


def vision_to_dimacs(filename, x, y, vue, N, M):
    case = position_to_num_case(x, y, M)
    var = None
    if vue == HC.EMPTY:
        var = var_vide(N, M)[case]
        print("var vide : ", var)

    elif vue == HC.CIVIL_E:
        var = var_civilE(N, M)[case]
        print("var civilE : ", var)
    elif vue == HC.CIVIL_S:
        var = var_civilS(N, M)[case]
        print("var civilS : ", var)
    elif vue == HC.CIVIL_W:
        var = var_civilW(N, M)[case]
        print("var civilW : ", var)
    elif vue == HC.CIVIL_N:
        var = var_civilN(N, M)[case]
        print("var civilN : ", var)

    elif vue == HC.GUARD_E:
        var = var_guardE(N, M)[case]
        print("var guardE : ", var)
    elif vue == HC.GUARD_S:
        var = var_guardS(N, M)[case]
        print("var guardS : ", var)
    elif vue == HC.GUARD_W:
        var = var_guardW(N, M)[case]
        print("var guardW : ", var)
    elif vue == HC.GUARD_N:
        var = var_guardN(N, M)[case]
        print("var guardN : ", var)

    elif vue == HC.PIANO_WIRE:
        var = var_corde(N, M)[case]
        print("var corde : ", var)

    elif vue == HC.SUIT:
        var = var_costume(N, M)[case]
        print("var costume : ", var)

    elif vue == HC.WALL:
        var = var_mur(N, M)[case]
        print("var mur : ", var)

    elif vue == HC.TARGET:
        var = var_cible(N, M)[case]
        print("var cible : ", var)

    if var is not None:
        print(f"var = {var}")
        with open(filename, 'a') as file:
            file.write(str(var) + ' 0\n')


def dimacs(hr):
    status = hr.start_phase1()
    gardes = status["guard_count"]
    civils = status["civil_count"]
    N = status["n"]
    M = status["m"]
    tab = []
    c = 0
    for el in unique_element_par_case_plateau(N, M):
        tab.append(el)
        c += 1
    for el in unique_cible(N, M):
        tab.append(el)
        c += 1
    for el in unique_costume(N, M):
        tab.append(el)
        c += 1
    for el in unique_corde(N, M):
        tab.append(el)
        c += 1
    for el in exactement_nb_gardes(gardes, N, M):
        tab.append(el)
        c += 1
    for el in exactement_nb_civils(civils, N, M):
        tab.append(el)
        c += 1
    return tab, c, N, M


def write_dimacs_file(filename: str, hr):
    with open(filename, 'w') as file:
        tab, c, N, M = dimacs(hr)
        file.write('p cnf {} {}\n'.format(N * M * 13, c))
        # Écriture des clauses
        for clause in tab:
            file.write(' '.join(str(literal) for literal in clause) + ' 0\n')


"""hr = HitmanReferee()
tab, c, N, M = dimacs(hr)
#print (tab)
print (c)
print (N)
print (M)
print(var_vide(N,M))

write_dimacs_file('hitman.cnf', hr)"""
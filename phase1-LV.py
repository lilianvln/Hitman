import numpy as np
from hitman import *


def model_plateau(M, N):
    liste_plateau = [0] * M
    for m in range(M):
        ligne = [0] * N
        for n in range(N):
            ligne[n] = "non_etudie"
        liste_plateau[m] = ligne
    return liste_plateau


def print_plateau(plateau):
    colonnes = len(plateau[0])
    lignes = len(plateau)
    for i in range(lignes):
        if i == 0: # Première ligne
            print("┌" + "─" * (15 * colonnes + colonnes - 1) + "┐")
        else: # Autres lignes
            print("├" + "─" * (15 * colonnes + colonnes - 1) + "┤")
        for j in plateau[i]:
            print("│{:^14} ".format(j), end="")
        print("│")
    print("└" + "─" * (15 * colonnes + colonnes - 1) + "┘") # Dernière ligne


def call_arbitre(hr):
    status = hr.start_phase1()
    position = status["position"]
    orientation = status["orientation"]
    vision = status["vision"]
    hear = status["hear"]
    penalties = status["penalties"]
    guard_range = status["is_in_guard_range"]
    return vision, position, orientation, hear, penalties, guard_range


def voir(vision, plateau):  # remplit le tableau de ce qui est vu
    ligne = len(plateau) - 1
    for i in vision:
        x = ligne - i[0][1]
        y = i[0][0]
        plateau[x][y] = i[1]
    return plateau


def entendre(position, entend, tab):
    M = len(plateau) - 1
    N = len(plateau[0]) - 1
    y_pos, x_pos = position
    nb_personne_vue = 0

    x_min = x_pos - 2
    x_max = x_pos + 2
    y_min = y_pos - 2
    y_max = y_pos + 2

    if x_max > M:
        x_max = M
    if x_min < 0:
        x_min = 0
    if y_max > N:
        x_max = N
    if y_min < 0:
        y_min = 0

    if entend == 0:  # si on n'entend rien, il n'y a personne autour
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                if tab[i][j] in ["non_etudie", "qqn_pe"]:
                    tab[i][j] = "personne"
    else:  # on entend des gens
        nb_personne = 0
        non_connue = 0
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                if tab[i][j] in [HC.CIVIL_N, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W,
                                 HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]:
                    nb_personne += 1  # compte les personnes connues autour
                if tab[i][j] in ["non_etudie", "qqn_sur", "qqn_pe"]:
                    non_connue += 1  # compte les cases dont on ne connait pas le contenu et qui pourraient contenir qqn
        if nb_personne == entend:  # si on a déjà placé toutes les personnes qu'on entend
            for i in range(x_min, x_max + 1):
                for j in range(y_min, y_max + 1):
                    if tab[i][j] in ["non_etudie", "qqn_pe"]:
                        tab[i][j] = "personne"  # ni civil ni garde
        elif (non_connue + nb_personne) == entend:  # Le nombre de case inconnue correspond au nombre de personnes qu'il reste à placer
            for i in range(x_min, x_max + 1):
                for j in range(y_min, y_max + 1):
                    if tab[i][j] in ["non_etudie", "qqn_pe"]:
                        tab[i][j] = "qqn_sur"
        else:  # on sait qu'il y a du monde, mais pas où
            for i in range(x_min, x_max + 1):
                for j in range(y_min, y_max + 1):
                    if tab[i][j] in ["non_etudie"]:
                        tab[i][j] = "qqn_pe"  # il y a peut être qqn
    return tab



def anaylse(hr, position, orientation, plateau):
    y_pos, x_pos = position
    M = len(plateau) - 1
    N = len(plateau[0]) - 1
    if orientation == HC.N:
        if plateau[M-x_pos][y_pos+1] == "personne" or plateau[M-x_pos][y_pos+1] == "pe_qlqn" or plateau[M-x_pos][y_pos+1] == "non_etudie":
            hr.turn_clockwise()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            entendre(position, hear, plateau)
            voir(vision, plateau)
        elif plateau[M-x_pos][y_pos-1] == "personne" or plateau[M-x_pos][y_pos-1] == "pe_qlqn" or plateau[M-x_pos][y_pos-1] == "non_etudie":
            hr.turn_anti_clockwise()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            entendre(position, hear, plateau)
            voir(vision, plateau)


def deplacement(hr, vision, position, orientation, plateau):
    y_pos, x_pos = position
    M = len(plateau) - 1
    N = len(plateau[0]) - 1

    if vision[0] == HC.WALL:
        hr.turn_clockwise()
        (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
        entendre(position, hear, plateau)
        voir(vision, plateau)












plateau = model_plateau(3, 3)


hr = HitmanReferee()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(f"personne entendu : {hear}")
print(f"position : {position}")
entendre(position, hear, plateau)
voir(vision, plateau)
anaylse(hr, position, orientation, plateau)
print_plateau(plateau)

hr.turn_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(f"personne entendu : {hear}")
print(f"position : {position}")
entendre(position, hear, plateau)
voir(vision, plateau)
anaylse(hr, position, orientation, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(f"personne entendu : {hear}")
print(f"position : {position}")
entendre(position, hear, plateau)
voir(vision, plateau)
anaylse(hr, position, orientation, plateau)
print_plateau(plateau)

hr.turn_anti_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(f"personne entendu : {hear}")
print(f"position : {position}")
entendre(position, hear, plateau)
voir(vision, plateau)
anaylse(hr, position, orientation, plateau)
print_plateau(plateau)


"""
hr.turn_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.turn_anti_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.turn_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
entendre(position, hear, plateau)
print(position)
voir(vision, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
print(position)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.turn_anti_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
print(position)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
print(position)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)

hr.move()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(hear)
print(position)
entendre(position, hear, plateau)
voir(vision, plateau)
print_plateau(plateau)"""
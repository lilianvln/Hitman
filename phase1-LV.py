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
        if i == 0:  # Première ligne
            print("┌" + "─" * (15 * colonnes + colonnes - 1) + "┐")
        else:  # Autres lignes
            print("├" + "─" * (15 * colonnes + colonnes - 1) + "┤")
        for j in plateau[i]:
            print("│{:^14} ".format(j), end="")
        print("│")
    print("└" + "─" * (15 * colonnes + colonnes - 1) + "┘")  # Dernière ligne


def call_arbitre(hr):
    status = hr.start_phase1()
    position = status["position"]
    orientation = status["orientation"]
    vision = status["vision"]
    hear = status["hear"]
    penalties = status["penalties"]
    guard_range = status["is_in_guard_range"]
    return vision, position, orientation, hear, penalties, guard_range


def premier_appel(hr):
    status = hr.start_phase1()
    guard_count = status["guard_count"]
    civil_count = status["civil_count"]
    N = status["n"]
    M = status["m"]
    tab = model_plateau(M, N)
    return N, M, tab, guard_count, civil_count


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
        y_max = N
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
        elif (
                non_connue + nb_personne) == entend:  # Le nombre de case inconnue correspond au nombre de personnes qu'il reste à placer
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
        if plateau[M - x_pos][y_pos + 1] == "personne" or plateau[M - x_pos][y_pos + 1] == "pe_qlqn" or \
                plateau[M - x_pos][y_pos + 1] == "non_etudie":
            hr.turn_clockwise()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            entendre(position, hear, plateau)
            voir(vision, plateau)
        elif plateau[M - x_pos][y_pos - 1] == "personne" or plateau[M - x_pos][y_pos - 1] == "pe_qlqn" or \
                plateau[M - x_pos][y_pos - 1] == "non_etudie":
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


def heuristique(courante, destination):
    return abs(courante[0] - destination[0]) + abs(courante[1] - destination[1])


def remaining_empty_cases(tableau):
    for ligne in tableau:
        for case in ligne:
            if case == "non_etudie":
                return True
    return False

def count_qqn_pe_cases(tableau):
    count = 0
    for ligne in tableau:
        for case in ligne:
            if isinstance(case, str) and case == "qqn_pe" \
                    or case == HC.GUARD_N or case == HC.GUARD_S or case == HC.GUARD_E or case == HC.GUARD_W\
                    or case == HC.CIVIL_N or case == HC.CIVIL_S or case == HC.CIVIL_E or case == HC.CIVIL_W:
                count += 1
    return count


def parcours_plateau(hr):
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)

    voir(vision, plateau)
    entendre(position, hear, plateau)
    print_plateau(plateau)
    print(f"position de Hitman : {position}")
    print(f"orientation de Hitman : {orientation}")
    print(f"vision de Hitman : {vision}")

    y_pos, x_pos = position
    M = len(plateau) - 1
    N = len(plateau[0]) - 1

    case_devant = None
    case_droite = None
    case_gauche = None
    if orientation == HC.N:  # Hitman regarde au Nord
        if 0 <= y_pos <= N and 0 <= x_pos + 1<= M:
            case_devant = vision[0][1]
        if 0 <= y_pos + 1 <= N and 0 <= x_pos <= M:
            case_droite = plateau[x_pos][y_pos + 1]
        if 0 <= y_pos - 1 <= N and 0 <= x_pos <= M:
            case_gauche = plateau[x_pos][y_pos - 1]
    elif orientation == HC.S:  # Hitman regarde au Sud
        if 0 <= y_pos <= N and 0 <= x_pos - 1 <= M:
            case_devant = vision[0][1]
        if 0 <= y_pos - 1 <= N and 0 <= x_pos <= M:
            case_droite = plateau[x_pos][y_pos - 1]
        if 0 <= y_pos + 1<= N and 0 <= x_pos <= M:
            case_gauche = plateau[x_pos][y_pos + 1]
    elif orientation == HC.E:  # Hitman regarde à l'Est
        if 0 <= y_pos + 1 <= N and 0 <= x_pos <= M:
            case_devant = vision[0][1]
        if 0 <= y_pos <= N and 0 <= x_pos - 1 <= M:
            case_droite = plateau[x_pos - 1][y_pos]
        if 0 <= y_pos <= N and 0 <= x_pos + 1 <= M:
            case_gauche = plateau[x_pos + 1][y_pos]
    else:  # Hitman regarde à l'Ouest
        if 0 <= y_pos - 1<= N and 0 <= x_pos <= M:
            case_devant = vision[0][1]
        if 0 <= y_pos <= N and 0 <= x_pos + 1 <= M:
            case_droite = plateau[x_pos + 1][y_pos]
        if 0 <= y_pos <= N and 0 <= x_pos - 1 <= M:
            case_gauche = plateau[x_pos - 1][y_pos]

    print(f"case devant : {case_devant}")
    print(f"case droite : {case_droite}")
    print(f"case gauche : {case_gauche}")

    if (case_devant != None) and case_devant == HC.EMPTY:  # Si la case devant est vide avancer
        hr.move()
        (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
        voir(vision, plateau)
        print("Hitman avance")

    else:  # Si la case devant est plein
        if (case_droite != None) and (
                case_droite == HC.EMPTY or case_droite == "qqn_pe" or case_droite == "non_etudie" or case_droite == "personne"):
            hr.turn_clockwise()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            voir(vision, plateau)
            hr.move()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            voir(vision, plateau)
            print("Hitman tourne à droite et avance")
        elif (case_gauche != None) and (case_gauche == HC.EMPTY or case_gauche == "qqn_pe" or case_gauche == "non_etudie" or case_gauche == "personne"):
            hr.turn_anti_clockwise()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            voir(vision, plateau)
            hr.move()
            (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
            voir(vision, plateau)
            print("Hitman tourne à gauche et avance")
    print("---------------------------------------------------------------------------------------")

# --------------------------------------------------------------------------------------------------------------------------------#




hr = HitmanReferee()

(N, M, plateau, guard_count, civil_count) = premier_appel(hr)


while remaining_empty_cases(plateau):
    while count_qqn_pe_cases(plateau) != guard_count+civil_count:
        print(count_qqn_pe_cases(plateau))
        parcours_plateau(hr)

"""(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)

print(f"personne entendu : {hear}")
print(f"position : {position}")
print(vision[0][1])
print(orientation)
entendre(position, hear, plateau)
voir(vision, plateau)
anaylse(hr, position, orientation, plateau)
print_plateau(plateau)

hr.turn_clockwise()
(vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
print(f"personne entendu : {hear}")
print(f"position : {position}")
print(vision)
entendre(position, hear, plateau)
voir(vision, plateau)
anaylse(hr, position, orientation, plateau)
print_plateau(plateau)
"""

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

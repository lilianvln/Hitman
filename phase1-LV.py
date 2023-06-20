import random

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
    y_pos, x_pos = status["position"]
    guard_count = status["guard_count"]
    civil_count = status["civil_count"]
    N = status["n"]
    M = status["m"]
    plateau = model_plateau(M, N)
    ligne = len(plateau) - 1
    plateau[ligne - x_pos][y_pos] = "personne"
    return N, M, plateau, guard_count, civil_count


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



def turn_clockwise(hr):
    hr.turn_clockwise()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    hr.move()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


def turn_anti_clockwise(hr):
    hr.turn_anti_clockwise()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    hr.move()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


def move(hr):
    hr.move()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


def remaining_empty_cases(tableau):
    for ligne in tableau:
        for case in ligne:
            if case == "non_etudie" or case == "qqn_pe":
                return True
    return False


def remaining_target_cases(tableau):
    for ligne in tableau:
        for case in ligne:
            if case == HC.TARGET:
                return True
    return False


def count_qqn_pe_sur_cases(tableau):
    count_qqn_pe_sur = 0
    for ligne in tableau:
        for case in ligne:
            if isinstance(case, str) and (case == "qqn_pe" or case == "qqn_sur"):
                count_qqn_pe_sur += 1
            if isinstance(case, str) and (
                    case == HC.GUARD_N or case == HC.GUARD_S or case == HC.GUARD_E or case == HC.GUARD_W or
                    case == HC.CIVIL_N or case == HC.CIVIL_S or case == HC.CIVIL_E or case == HC.CIVIL_W):
                count_qqn_pe_sur -= 1
    return count_qqn_pe_sur


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
        if 0 <= y_pos <= N and 0 <= x_pos + 1 <= M:
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
        if 0 <= y_pos + 1 <= N and 0 <= x_pos <= M:
            case_gauche = plateau[x_pos][y_pos + 1]
    elif orientation == HC.E:  # Hitman regarde à l'Est
        if 0 <= y_pos + 1 <= N and 0 <= x_pos <= M:
            case_devant = vision[0][1]
        if 0 <= y_pos <= N and 0 <= x_pos - 1 <= M:
            case_droite = plateau[x_pos - 1][y_pos]
        if 0 <= y_pos <= N and 0 <= x_pos + 1 <= M:
            case_gauche = plateau[x_pos + 1][y_pos]
    else:  # Hitman regarde à l'Ouest
        if 0 <= y_pos - 1 <= N and 0 <= x_pos <= M:
            case_devant = vision[0][1]
        if 0 <= y_pos <= N and 0 <= x_pos + 1 <= M:
            case_droite = plateau[x_pos + 1][y_pos]
        if 0 <= y_pos <= N and 0 <= x_pos - 1 <= M:
            case_gauche = plateau[x_pos - 1][y_pos]

    print(f"case devant : {case_devant}")
    print(f"case droite : {case_droite}")
    print(f"case gauche : {case_gauche}")

    choix_tab = []

    if (case_devant != None) and (
            case_devant == HC.EMPTY or case_devant == "qqn_pe" or case_devant == "non_etudie" or case_devant == "personne"):  # Si la case devant est vide avancer
        choix_tab.append(0)

    if (case_droite != None) and (
            case_droite == HC.EMPTY or case_droite == "qqn_pe" or case_droite == "non_etudie" or case_droite == "personne"):
        choix_tab.append(1)

    if (case_gauche != None) and (
            case_gauche == HC.EMPTY or case_gauche == "qqn_pe" or case_gauche == "non_etudie" or case_gauche == "personne"):
        choix_tab.append(2)

    if choix_tab != []:
        choix = random.choice(choix_tab)
        print(choix_tab)
        if choix == 0:
            garde = move(hr)
            points = 1
            print("Hitman avance")
            return points, garde
        elif choix == 1:
            garde = turn_clockwise(hr)
            points = 2
            print("Hitman tourne à droite et avance")
            return points, garde
        else:
            garde = turn_anti_clockwise(hr)
            points = 2
            print("Hitman tourne à gauche et avance")
            return points, garde
    else:
        # Implémenter fonction demi-tour pour éviter que hitman soit bloqué.
        print("Hitman est bloqué")
        print("---------------------------------------------------------------------------------------")
        breakpoint()


# --------------------------------------------------------------------------------------------------------------------------------#


hr = HitmanReferee()

(N, M, plateau, guard_count, civil_count) = premier_appel(hr)

parcours_idx = 0
points = 0
garde_vue = 0
while (remaining_empty_cases(plateau) or count_qqn_pe_sur_cases(plateau) != guard_count + civil_count) or remaining_target_cases(plateau):
    points_parcours, garde = parcours_plateau(hr)
    points += points_parcours
    if garde:
        points += 5
        garde_vue += 1
        print(f"Hitmain a été vu : {garde_vue}")
    print(points)
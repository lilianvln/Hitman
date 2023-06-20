import random
from colorama import Fore, Style
from hitman import *
from SAT import *


# -----------------------------------------PLATEAU---------------------------------------------------------------------#

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


# -----------------------------------------ARBITRE---------------------------------------------------------------------#

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


# -----------------------------------------HITMAN----------------------------------------------------------------------#

def voir(vision, plateau):  # remplit le tableau de ce qui est vu
    ligne = len(plateau) - 1
    for i in vision:
        x = ligne - i[0][1]
        y = i[0][0]
        plateau[x][y] = i[1]
        vision_to_dimacs(x, y, i[1])
    pass


def entendre(position, entend, plateau):
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
                if plateau[i][j] in ["non_etudie", "qqn_pe"]:
                    plateau[i][j] = "personne"
    else:  # on entend des gens
        nb_personne = 0
        non_connue = 0
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                if plateau[i][j] in [HC.CIVIL_N, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W,
                                 HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]:
                    nb_personne += 1  # compte les personnes connues autour
                if plateau[i][j] in ["non_etudie", "qqn_sur", "qqn_pe"]:
                    non_connue += 1  # compte les cases dont on ne connait pas le contenu et qui pourraient contenir qqn
        if nb_personne == entend:  # si on a déjà placé toutes les personnes qu'on entend
            for i in range(x_min, x_max + 1):
                for j in range(y_min, y_max + 1):
                    if plateau[i][j] in ["non_etudie", "qqn_pe"]:
                        plateau[i][j] = "personne"  # ni civil ni garde
        elif (
                non_connue + nb_personne) == entend:  # Le nombre de case inconnue correspond au nombre de personnes qu'il reste à placer
            for i in range(x_min, x_max + 1):
                for j in range(y_min, y_max + 1):
                    if plateau[i][j] in ["non_etudie", "qqn_pe"]:
                        plateau[i][j] = "qqn_sur"
        else:  # on sait qu'il y a du monde, mais pas où
            for i in range(x_min, x_max + 1):
                for j in range(y_min, y_max + 1):
                    if plateau[i][j] in ["non_etudie"]:
                        plateau[i][j] = "qqn_pe"  # il y a peut être qqn
    pass


# -----------------------------------------MOUVEMENT HITMAN------------------------------------------------------------#
def turn_clockwise(hr, plateau):
    hr.turn_clockwise()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    hr.move()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


def turn_anti_clockwise(hr, plateau):
    hr.turn_anti_clockwise()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    hr.move()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


def move(hr, plateau):
    hr.move()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


def U_turn(hr, plateau):
    hr.turn_clockwise()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    hr.turn_clockwise()
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)
    voir(vision, plateau)
    if guard_range:
        return True
    return False


# -----------------------------------------ANALYSE PLATEAU-------------------------------------------------------------#

def cases_non_etudie(tableau):
    for ligne in tableau:
        for case in ligne:
            if case == "non_etudie" or case == "qqn_pe":
                return True
    return False


def cases_target(tableau):
    for ligne in tableau:
        for case in ligne:
            if case == HC.TARGET:
                return True
    return False


def count_personne_decouverte(tableau):
    nb_personne_decouverte = 0
    nb_qqn_pe = 0
    nb_qqn_sur = 0
    for ligne in tableau:
        for case in ligne:
            if case == HC.GUARD_N or case == HC.GUARD_S or case == HC.GUARD_E or case == HC.GUARD_W or case == HC.CIVIL_N or case == HC.CIVIL_S or case == HC.CIVIL_E or case == HC.CIVIL_W :
                nb_personne_decouverte += 1
            if case == "qqn_pe":
                nb_qqn_pe += 1
            if case == "qqn_sur":
                nb_qqn_sur += 1
    return nb_qqn_sur


# -----------------------------------------PARCOURS PLATEAU------------------------------------------------------------#

def parcours_plateau(hr, plateau):
    (vision, position, orientation, hear, penalties, guard_range) = call_arbitre(hr)

    M = len(plateau) - 1
    N = len(plateau[0]) - 1

    y_pos, x_pos = position
    tmp = plateau[M - x_pos][y_pos]
    plateau[M - x_pos][y_pos] = f"{Fore.RED}    HITMAN    {Style.RESET_ALL}"

    voir(vision, plateau)
    entendre(position, hear, plateau)
    print_plateau(plateau)
    print(f"Position de Hitman : {position}")
    print(f"Orientation de Hitman : {orientation}")
    print(f"Vision de Hitman : {vision}")

    plateau[M - x_pos][y_pos] = tmp

    case_droite = None
    case_gauche = None

    if orientation == HC.N:  # Hitman regarde au Nord
        if 0 <= y_pos + 1 <= N and 0 <= x_pos <= M:
            case_droite = plateau[M - x_pos][y_pos + 1]

        if 0 <= y_pos - 1 <= N and 0 <= x_pos <= M:
            case_gauche = plateau[M - x_pos][y_pos - 1]
    elif orientation == HC.S:  # Hitman regarde au Sud
        if 0 <= y_pos - 1 <= N and 0 <= x_pos <= M:
            case_droite = plateau[M - x_pos][y_pos - 1]

        if 0 <= y_pos + 1 <= N and 0 <= M - x_pos <= M:
            case_gauche = plateau[M - x_pos][y_pos + 1]
    elif orientation == HC.E:  # Hitman regarde à l'Est
        if 0 <= y_pos <= N and 0 <= M - x_pos + 1 <= M:
            case_droite = plateau[(M - x_pos) + 1][y_pos]

        if 0 <= y_pos <= N and 0 <= M - x_pos - 1 <= M:
            case_gauche = plateau[(M - x_pos) - 1][y_pos]
    else:  # Hitman regarde à l'Ouest
        if 0 <= y_pos <= N and 0 <= M - x_pos - 1 <= M:
            case_droite = plateau[(M - x_pos) - 1][y_pos]

        if 0 <= y_pos <= N and 0 <= M - x_pos + 1 <= M:
            case_gauche = plateau[(M - x_pos) + 1][y_pos]

    choix_tab = []

    for i in range(len(vision)):
        if vision[i][1] == HC.EMPTY or vision[i][1] == "personne" or vision[i][1] == "non_etudie" or vision[i][1] == HC.CIVIL_N or vision[i][1] == HC.CIVIL_S or vision[i][1] == HC.CIVIL_E or vision[i][1] == HC.CIVIL_W:
                choix_tab.append(0)

    if (case_droite != None) and (case_droite == HC.EMPTY or case_droite == "qqn_pe" or case_droite == "non_etudie" or case_droite == "personne" or case_droite == HC.CIVIL_N or case_droite == HC.CIVIL_S or case_droite == HC.CIVIL_E or case_droite == HC.CIVIL_W):
        choix_tab.append(1)

    if (case_gauche != None) and (case_gauche == HC.EMPTY or case_gauche == "qqn_pe" or case_gauche == "non_etudie" or case_gauche == "personne" or case_gauche == HC.CIVIL_N or case_gauche == HC.CIVIL_S or case_gauche == HC.CIVIL_E or case_gauche == HC.CIVIL_W):
        choix_tab.append(2)

    if choix_tab:
        choix = random.choice(choix_tab)
        if choix == 0:
            print("Hitman avance")
            garde_range = move(hr, plateau)
            points = 1
            return points, garde_range
        elif choix == 1:
            print("Hitman tourne à droite et avance")
            garde_range = turn_clockwise(hr, plateau)
            points = 2
            return points, garde_range
        else:
            print("Hitman tourne à gauche et avance")
            garde_range = turn_anti_clockwise(hr, plateau)
            points = 2
            return points, garde_range
    else:
        # Implémenter fonction demi-tour pour éviter que hitman soit bloqué.
        print("Hitman fait demi-tour")
        garde_range = U_turn(hr, plateau)
        points = 2
        return points, garde_range


# -----------------------------------------RUN------------------------------------------------------------------------#


def main():
    hr = HitmanReferee()

    (N, M, plateau, guard_count, civil_count) = premier_appel(hr)

    points_parcours = 0
    point_garde_range = 0
    while (cases_non_etudie(plateau) or not cases_target(plateau)) and count_personne_decouverte(plateau) != guard_count + civil_count:  # Teste s'il reste des cases vides et si on a trouvé la cible.
        points_action, garde_range = parcours_plateau(hr, plateau)
        points_parcours += points_action
        if garde_range:
            points_action += 5
            point_garde_range += 1
            print(f"Hitman a été vu !!")
        print(f"Point d'action : {points_parcours}")
        print("----------------------------------------------------------------------------------------------------------------")
    return plateau, points_parcours, point_garde_range

# -----------------------------------------MAIN------------------------------------------------------------------------#

plateau, points_parcours, point_garde_range = main()

print("--------------------------------------------------PLATEAU FINAL-------------------------------------------------")
print_plateau(plateau)
print(f"Point d'action : {points_parcours}")
print(f"Nombre de fois ou Hitman a été vue : {point_garde_range}")
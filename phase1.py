import numpy as np
from hitman import *


def varToCell(M, N, var):
    ligne = var // N
    colonne = var % N
    return ligne, colonne


def cellToVar(M, N, ligne, colonne):
    var = ligne * N + colonne
    return var


def model_plateau(M, N):
    liste_plateau = [0] * M
    for m in range(M):
        ligne = [0] * N
        for n in range(N):
            ligne[n] = "non_etudie"
        liste_plateau[m] = ligne
    return liste_plateau


def premier_appel(hr):
    status = hr.start_phase1()
    guard_count = status["guard_count"]
    civil_count = status["civil_count"]
    n = status["n"]
    m = status["m"]
    tab = model_plateau(m, n)
    return m, m, tab, guard_count, civil_count


def appel_arbitre(hr):
    status = hr.start_phase1()
    position = status["position"]
    orientation = status["orientation"]
    vision = status["vision"]
    hear = status["hear"]
    penalties = status["penalties"]
    guard_range = status["is_in_guard_range"]
    return vision, position, orientation, hear, penalties, guard_range


def voir(vision, tab):  # rempli le tableau de ce qui est vu
    for i in vision:
        y, x = i[0]
        tab[x][y] = i[1]
    return tab


# def tourner(position, orientation) :


def entendre(m, n, entend, position, tab):
    y, x = position
    xmin = x - 2
    xmax = x + 2
    ymin = y - 2
    ymax = y + 2
    if xmax > (m - 1):
        xmax = m - 1
    if xmin < 0:
        xmin = 0
    if ymax > (n - 1):
        xmax = n - 1
    if ymin < 0:
        ymin = 0
    if entend == 0:  # si on n'entend rien, il n'y a personne autour
        for i in range(xmin, xmax + 1):
            for j in range(ymin, ymax + 1):
                if tab[i][j] in ["non_etudie", "qqn_pe"]:
                    tab[i][j] = "personne"
    else:  # on entend des gens
        nb_personne = 0
        non_connue = 0
        for i in range(xmin, xmax + 1):
            for j in range(ymin, ymax + 1):
                if tab[i][j] in [HC.CIVIL_N, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W,
                                 HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]:
                    nb_personne += 1  # compte les personnes connues autour
                if tab[i][j] in ["non_etudie", "qqn_sur", "qqn_pe"]:
                    non_connue += 1  # compte les cases dont on ne connait pas le contenu et qui pourraient contenir qqn
        if nb_personne == entend:  # si on à déjà placé toutes les personnes qu'on entend
            for i in range(xmin, xmax + 1):
                for j in range(ymin, ymax + 1):
                    if tab[i][j] in ["non_etudie", "qqn_pe"]:
                        tab[i][j] = "personne"  # ni civil ni garde
        elif (
                non_connue + nb_personne) == entend:  # le nombre de case inconnue correspond au nombre de personnes qu'il reste à placer
            for i in range(xmin, xmax + 1):
                for j in range(ymin, ymax + 1):
                    if tab[i][j] in ["non_etudie", "qqn_pe"]:
                        tab[i][j] = "qqn_sur"
        else:  # on sait qu'il y a du monde mais pas où
            for i in range(xmin, xmax + 1):
                for j in range(ymin, ymax + 1):
                    if tab[i][j] in ["non_etudie"]:
                        tab[i][j] = "qqn_pe"  # il y a peut être qqn
    return tab


def etape(hr, m, n, tab):
    print("étape suivante :")
    vision, position, orientation, entend, penalite, vu_garde = appel_arbitre(hr)
    print(position)
    print(orientation)
    tab = voir(vision, tab)
    tab = entendre(m, n, entend, position, tab)
    for element in tab:
        print(element)


def phase1(hr):
    m, n, tab, nb_guard, nb_civil = premier_appel(hr)
    pas_fini = True
    # while pas_fini :
    etape(hr, m, n, tab)

    # test:
    hr.turn_clockwise()
    etape(hr, m, n, tab)
    hr.move()
    etape(hr, m, n, tab)
    hr.turn_anti_clockwise()
    etape(hr, m, n, tab)
    hr.move()
    etape(hr, m, n, tab)
    hr.turn_clockwise()
    etape(hr, m, n, tab)
    hr.move()
    etape(hr, m, n, tab)
    hr.turn_anti_clockwise()
    etape(hr, m, n, tab)

    # tab_possibilite = possible(m, n, tab,tab_possibilite, entend, vu_garde)
    # tourner intelligement

    # condition d'arret de la boucle
    """trouve = False
        for i in tab :
            if "non_etudie" in i :
                trouve = True
        if (trouve==False) :
            pas_fini=False
        """
    # else : #on avance

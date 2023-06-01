from hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint
import numpy as np


def model_plateau(M, N):
    liste_plateau = [0]*M
    for m in range(M):
        ligne = [0]*N
        for n in range(N):
            ligne[n] = HC.EMPTY
        liste_plateau[m] = ligne
    return liste_plateau


empty_map = model_plateau(6, 7)



def varToCell(M, N, var):
    ligne = var // N
    colonne = var % N
    return ligne, colonne


def cellToVar(M, N, ligne, colonne):
    var = ligne * N + colonne
    return var


liste = model_plateau(6, 7)


def main():
    hr = HitmanReferee()
    status = hr.start_phase1()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    pprint(hr.send_content({(0, 0): HC.EMPTY}))
    pprint(hr.send_content(complete_map_example))
    complete_map_example[(7, 0)] = HC.EMPTY
    pprint(hr.send_content(complete_map_example))



if __name__ == "__main__":
    main()

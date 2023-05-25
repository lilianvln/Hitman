from hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint
import numpy as np


def model_plateau(M, N):
    liste_plateau = [0]*
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


if __name__ == "__main__":
    main()

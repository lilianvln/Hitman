 ## Exercice n°3 : Prise en main d'un solveur SAT ##

# _______________________________________________________________________________ #

# FONCTION #
def nb_sommet():
    return int(input("Entrer un nombre le nombre de sommets du graph : "))


def parameter(nb_sommet, nb_parametre):
    files.write(f"p cnf {3 * nb_sommet} {nb_parametre}\n")


def noeud(nb_sommet):
    noeuds = []
    for i in range(1, nb_sommet + 1):
        noeuds.append(i)
    return noeuds


def links(nb_sommet):
    link = []
    for i in range(1, nb_sommet):
        for j in range(1, nb_sommet):
            link.append((i, j))
    print(link)


def variable(noeuds, colors):
    variables = []
    for i in noeuds:
        for j in colors:
            variables.append(f"S{i}{j}")
    return variables


def couple_sommet(id_prem_sommet):
    tab_couple_sommet = []
    deb = id_prem_sommet + 1
    for i in range(id_prem_sommet, id_prem_sommet + 2):
        for j in range(id_prem_sommet + 1, id_prem_sommet + 3):
            if i !=  j:
                tab_couple_sommet.append([i, j])
    return tab_couple_sommet

def sommet_adj(id_gauche, decallage):
    tab_sommet_adj = []
    for i in range(id_gauche, id_gauche + 3):
        tab_sommet_adj.append([i, i + decallage])
    return tab_sommet_adj


# _______________________________________________________________________________ #

# VARIABLE #
nb_sommets = nb_sommet()
noeuds = noeud(nb_sommets)
color = ['R', 'G', 'B']
variables = variable(noeuds, color)
#print(variables)

# dico avec toute les variables
dico_var = {}
for i in range(len(variables)):
    dico_var[i + 1] = f'{variables[i]}'
#print(dico_var)

# arc entre les noeuds
links(nb_sommets)

# _______________________________________________________________________________ #

# MODELISATION #
# Chaque sommet ne peut être colorié qu'avec une seule couleur
res_couple_sommet = []
for i in range(1, nb_sommets*3, 3):
    res_couple_sommet += (couple_sommet(i))


# Chaque sommet a une couleur différente des sommets adjacents
res_sommet_adj = []
deb = 1
fin = nb_sommets*3
for i in range(deb, nb_sommets*3, 3):
    #print(i)
    for j in range(3, fin, 3):
        res_sommet_adj += sommet_adj(i, j)
    fin -= 3


# _______________________________________________________________________________ #
files = open("Exercices/Exercice_3.cnf", "w")
# _______________________________________________________________________________ #
# Ecriture fichier
# ENTETE #
files.write(f"""c FILE: Exercice_3.cnf
c
c SOURCE: Lilian Valin
c
c DESCRIPTION: Exercice 3 - CNF coloration d'un graph 
c NOTATION : {dico_var}\n""")


nb_parametre = nb_sommets + len(res_couple_sommet) + len(res_sommet_adj)

parameter(nb_sommets, nb_parametre)

# Chaque sommet doit être colorié par une couleur
for i in range(1, len(dico_var) + 1, 3):
    files.write(f'{i} {i + 1} {i + 2} 0 \n')

for i in res_couple_sommet:
    files.write(f"-{i[0]} -{i[1]} 0\n")

for i in res_sommet_adj:
    files.write(f"-{i[0]} -{i[1]} 0\n")

files.close()

Rapport 



Phase 1 :

Pour la phase 1, nous effectuons tout d'abord un premier appel à l'arbitre qui nous renvoie les informations importantes qui ne changeront pas lors de notre parcours (nombre de gardes et de civils, taille du plateau (N, M), etc). Nous créons ensuite, grâce à ces information, un tableau de taille N*M représentant le plateau en cours d'exploration. Nous initialisons chacunes de ses cases à "non-étudié".

Ensuite, nous nous déplaçons dans le plateau en récupérant, après chaque action, les informations données par l'arbitre sur ce qui nous entoure :
 - la vue : nous ajoutons dans notre tableau les informations renvoyées par la vue.
 - l'ouie : nous interprétons ce que nous entendons : 
    - rien : cela signifie qu'il n'y a personne autour donc on met les cases non-étudiés (ou contenant peut être quelqu'un) qui entourent Hitman à "personne".
    - autant de personnes que le nombre de personnes que nous connaissons dans notre périmètre : on passe toutes les cases inconues à "personne"
    - le nombre de personnes entendues moins le nombre de personnes dont on connait l'emplacement est égal au nombres de cases dont on ne connait pas le contenu : on ajoute au tableau, dans les cases inconues du périmètre "qqn_sur" car les personnes entendues sont forcément sur ces cases là.
    - sinon, on entend des gens mais on ne peut pas savoir où ils sont : on ajoute "qqn_pe" dans les cases non_étudiées du périmètre.

Pour nous déplacer, nous mettons dans un tableau toutes les actions possibles pour Hitman puis nous choisissons aléatoirement l'action qu'il va effectuer. Si il est bloqué de tous les cotés, il va faire demi-tour. Petit à petit, notre tableau va se remplir, en grande partie grâce à la vision pour finalement être completement découvert.



Modélisation SAT :

Pour faire la modélisation SAT, nous avons choisi, pour chaque case, d'associer un nombre à un objet possiblement présent sur celle-ci. Il y a donc 13 raviables par cases, par exemple, pour la case (0,0), on a :
 - 1 : case vide 
 - 2 : civil orienté au nord
 - 3 : civil orienté à l'est 
 - 4 : civil orienté au sud
 - 5 : civil orienté à l'ouest
 - 6 : garde orienté au nord
 - 7 : garde orienté à l'est 
 - 8 : garde orienté au sud
 - 9 : garde orienté à l'ouest
 - 10 : mur
 - 11 : corde de piano
 - 12 : costume 
 - 13 : cible

Et ainsi de suite pour les autres cases.

Ensuite, nous avons repris les contraintes du sujets et les avons mis sous forme de CNF pour ensuite pouvoir les importer dans le DIMACS :
 - un unique élément pas case
 - une unique corde de piano sur tout le plateau 
 - un unique costume sur tout le plateau 
 - une unique cible sur tout le plateau 
 - exactement nb gardes (nombre renvoyé par l'arbitre) 
- exactement nb civils (nombre renvoyé par l'arbitre) 

Nous avons ensuite fait une fonction qui permet de mettre toutes les clauses générées sous format DIMACS pour pouvoir fournir le fichier à Gophersat.

Une fonction permettant d'ajouter les fait dont on est sur lors du parcours du plateau (grâce à la vue en général) à aussi été implémentée. Mais cette fonction sensée ajouter des clauses au fichier DIMACS rend le finchier insatisfiable donc elle n'a pu être utilisé. Et, malgrès de longues heures passées à essayer de trouver la source du problème, nous n'avons pas réussi.



Les faiblesses de notre phase 1 sont que nous avons eu du mal à connecter SAT avec notre algorithme python et nous ne comprenions pas comment l'utiliser intelligement. De plus, nous n'évitons pas les cases qui sont regardées par des gardes ce qui nous donne parfois beaucoup de pénalité. De plus, l'utilisation du random donne des scores très variés selon les exécutions.

Le point fort de la phase 1 est qu'elle arrive toujours à trouver la carte complete (et correcte), probablement grâce au random qui permet qu'Hitman se débloque et ne tourne pas en rond sans fin. De plus, les scores sont parfois très bons, mais cela relève de l'aléatoire.


Phase 2 :

Pour la phase 2, nous avons tout d'abord commencé par la modélisation en STRIPS que vous trouverez ci-joint. Nous avons ensuite converti cette modélisation de python afin de pouvoir effectuer la phase 2 et chercher le meilleur chemin pour Hitman grâce à un algorithme A*. 

Pour cela, nous créons un état initial qui reprend toutes les informations de la map obtenue à la fin de la phase 1. Ces informations sont stockées dans un dictionaire état qui correspond à tous les fluents de notre STRIPS. Nous créons aussi une fonction goal qui renvoie True si l'état qu'on lui fournis correspond à Hitman en (0,0) et cible tuée.
Nous créons ensuite une classe Noeud ayant pour méthodes toutes les actions possibles. Ces méthodes ont étes implémentées suivant notre modélisation STRIPS. Chaque action crée un nouvel état et retourne le nombre de pénalités associées à cette action. 

Nous implémentons ensuite un algorithme A* qui part de l'état initial et essaye d'aller à l'état final. Pour cela, nous avons implémenté une fonction qui calcule les heuristiques pour chaque état.

L'algorithme A* est sensé nous retourner une suite d'états correspondant au chemin que doit emprunter Hitman pour aller tuer la cible. Nous avons ensuite une fonction qui converti cette suite d'états en suite d'action que doit réaliser hitman.
Mais malheuresement, malgrès de nombreux efforts de notre part, notre algorithme A* ne fonctionne pas et n'arrive pas à renvoyer de chemin donc notre phase 2 n'abouti pas.

Le gros point faible de la phase 2 est qu'elle ne fonctionne pas. 


Globalement, les points faibles de notre programmes sont que nous n'avons pas réussi à faire fonctionner beaucoup de chose et tout n'est donc pas fonctionnels.
Le point fort de ce projet est que nous avons beaucoup appris.

Pour conclure, ce projet nous a demandé beaucoup d'investissement mais nous n'avons pas réussi à tout rendre fonctionnel par manque de temps. Mais il nous à beaucoup appris et nous a réellement fait découvrir la programation d'intelligences artificielles.



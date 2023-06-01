# Tâches à faire :

## Phase n°1 :
- [ ] Cartographier le la plateau de taille (M,N)
  - [ ] Faire une fonction qui appelle l'arbitre et récupère ce que le joueur voit
  - [ ] Placer ce que le joueur voit dans un tableau, et le faire tourner pour capter tout ce qu'il peut voire
  - [ ] Le faire se déplacer de manière logique
  - [ ] Répéter tout cela jusqu'à que le tableau soit plein


- [ ] Modélisation SAT
  - [ ] Convertir le plateau de jeu en SAT
  - [ ] Convertir les règle du jeu en SAT
  - [ ] Placer le tout dans un fichier SAT pour une résolution avec gopherSAT
  -[ ] Faire le décompte des points :
    - "Décompte des points : deux points par case correctement classée, un point de malus par action, 5 points de malus supplémentaire par nombre de fois où vous êtes passé dans le champ de vision d’un garde."

## Phase n°2 :
- [ ] Faire modélisation en STRIPS 
- [ ] Recherche du meilleur parcours pour tuer la cible
- [ ] Décompte des points
  - "Décompte des points (de furtivité) : nb d’actions effectuées + nb de fois vu par un garde * 5 + nb de personnes neutralisées * 20 + nb de fois vu en train de passer le costume * 100 + nb de fois vu en train de neutraliser quelqu’un * 100 + nb de fois vu en train de tuer la cible * 100"
- [ ] Programme python exploitent la modélisation STRIPS

## Phase n°3 :
- [ ] Faire un compte rendu avec : 
  - Un rapport incluant vos modélisations et résumant les forces et faiblesses de vos programmes.
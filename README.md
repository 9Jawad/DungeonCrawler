# Dungeon Crawler
![image](https://github.com/user-attachments/assets/ff96020e-72fd-486b-8f45-26c17fc71122)

## Auteur
  - ### Prénom : Jawad Cherkaoui
  - ### Date : 2023-04-02
  - ### Matricule : 576517

   
## But
Le but de ce projet est de créer un jeu de type Dungeon Crawler où le joueur doit naviguer à travers un donjon, collecter des bonus, éviter des fantômes et atteindre la sortie.

## Structure du Projet

### Fichiers Principaux

- `renderer.py` : Se charge de l'affichage du donjon.
- `pos2d.py` : Représente un point avec des coordonnées entières.
- `player.py` : Représentation de la personne tentant de sortir du donjon.
- `grid.py` : Représente le donjon à travers une matrice de nodes.
- `generation.py` : Permet de générer un donjon en fonction des paramètres passés en argument.
- `box.py` : Représentation d'un rectangle défini par deux points.

### Classes Principales

- `GridRenderer` : Classe pour afficher la grille du donjon.
- `Renderer` : Hérite de `GridRenderer` et ajoute des fonctionnalités spécifiques au jeu.
- `Pos2D` : Classe pour représenter une position en 2D.
- `Player` : Classe pour gérer les actions du joueur.
- `Node` : Classe pour représenter une case du donjon.
- `Grid` : Classe pour gérer la grille du donjon.
- `DungeonGenerator` : Classe pour générer le donjon.
- `Box` : Classe pour représenter une pièce du donjon.

## Instructions d'Utilisation

1. Cloner le dépôt.
2. Installer les dépendances nécessaires.
3. Exécuter le script principal pour lancer le jeu.

## Exécution

Pour exécuter le jeu, utilisez la commande suivante :

```bash
python3 main.py
```

## Paramètres

Le jeu peut être configuré à l'aide de différents paramètres passés en argument. Voici quelques exemples :

- `--width` : Largeur du donjon.
- `--height` : Hauteur du donjon.
- `--rooms` : Nombre de pièces.
- `--bonuses` : Nombre de bonus.
- `--ghosts` : Nombre de fantômes.
- `--seed` : Graine pour le générateur aléatoire.

## Exemple

```bash
python3 main.py --width 10 --height 10 --rooms 5 --bonuses 3 --ghosts 2 --seed 42
``

"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
Entrées : Les dimensions du donjon (widht, height), le reste est optionnel ! 
Sorties : Affichage du donjon sur le terminal
But : Votre objectif est, sur le long terme, de réussir à trouver la sortie depuis n'importe
    quelle position et peu importe la dificulté du donjon, votre seule consolation étant une torche vous permettant de vous éclairer. 
    Il vous faut cependant faire attention : votre torche fonctionne à l'huile, et cette dernière se consomme à chacun de vos pas. 
    Heureusement pour vous, de petites réserves de carburant à brûler se situent de manière cachée dans les donjons.
"""

# importation des modules :
import os
import argparse
from player import Player
from renderer import Renderer
from generation import DungeonGenerator
#########################################


def main() -> None:
    ##############  CONFIGURATION  ##############
    parse = argparse.ArgumentParser()
    parse.add_argument('width', help="Width of the dungeon", type=int)
    parse.add_argument('height', help="Height of the dungeon", type=int)
    parse.add_argument('--rooms', help="Number of rooms to generate (default: 5)", required=False, default=5, type=int)
    parse.add_argument('--bonuses', help="Number of bonuses to generate (default: 2)", required=False, default=2, type=int)
    parse.add_argument('--seed', help="Seed for the RNG (default: None)", required=False, default=None, type=int)
    parse.add_argument('--view-radius', help="Rendering distance around the player (default: 6)", required=False, default=6, type=int)
    parse.add_argument('--torch-delay', help="Number of moves between 2 torch decays (default: 7)", required=False, default=7, type=int)
    parse.add_argument('--bonus-radius', help="Visibility radius augmentation by bonus (default: 3)", required=False, default=3, type=int)
    parse.add_argument('--minwidth', help="Min width of a room (default: 4)", required=False, default=4, type=int)
    parse.add_argument('--maxwidth', help="Max width of a room (default: 8)", required=False, default=8, type=int)
    parse.add_argument('--minheight', help="Min height of a room (default: 4)", required=False, default=4, type=int)
    parse.add_argument('--maxheight', help="Max height of a room (default: 8)", required=False, default=8, type=int)
    parse.add_argument('--openings', help="Number of openings per room (default: 2)", required=False, default=2, type=int)
    parse.add_argument('--hard', help="Turn the dungeon into a maze (default: False)", required=False, action='store_true')
    parse.add_argument('--ghosts', help="Number of ghosts to spawn (default: 0)", required=False, default=0, type=int)
    parse.add_argument('--ghosts-delay', help="Ghosts will wonder around once every (default: 2)", required=False, default=2, type=int)
    parse.add_argument('--ghosts-walls', help="Ghosts cannot go through walls (default: False)", required=False, action='store_true')
    params = parse.parse_args()
    
    
    ##############  PLAY GAME  ##############
    
    # ---  Initialisation ---
    
    game = None
    dungeon = DungeonGenerator(params)
    dictionary = dungeon.generate()
    user = Player(dungeon.board, dictionary, params)
    
    # ---  Boucle de jeu ---
    
    while game == None:
        os.system('cls' if os.name == 'nt' else 'clear')
        Renderer(dungeon.board, user.pos, user.view).show()
        direction = input("Enter a direction (Z, Q, S, D): ").lower()
        while direction not in ('z', 'q', 's', 'd'):
            direction = input('\033[37m' + "Enter a direction (Z, Q, S, D): " + '\033[0m').lower()
        # deplacement avec direction 
        game = user.deplacement(direction)
    
    # ---  Fin de partie ---
    
    os.system('cls' if os.name == 'nt' else 'clear')
    Renderer(dungeon.board, user.pos, user.view).show()
    print('\n'+'\033[92m'+ "   You managed to escape !" +'\033[0m'+'\n') if game == True \
    else print('\n'+'\033[1;91m'+ f"   {game}" +'\033[0m'+'\n')
        

if __name__ == '__main__':
    main()
"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
But : Se charge de l'affichage du donjon.
"""

# importation des modules :
from pos2d import Pos2D
from grid import Grid
###########################


class GridRenderer:
    
    def __init__(self, grid: Grid) -> None:
        """
        Construit un renderer d'une grille.
        """
        self.grid = grid.grid
        self.width, self.height = grid.width, grid.height
        self.full_lines, self.line1, self.line2 = '', '', ''


    def central_filling(self) -> None:
        """
        Remplissage central de la grille.
        """
        for y in range(1, self.height):
            for x in range(self.width):
                node = self.grid[x][y]
                if not self.visibility(x, y):
                    self.line1 += f"    {' ' if x == self.width - 1 else ''}"
                    self.line2 += f"    {' ' if x == self.width - 1 else ''}"
                else:
                    if not x:   # bord de gauche
                        self.line1 += f"{'├───' if not node.up else '│   '}"
                    else:   # caractères du milieu + bord de droite
                        char = self.detect_character(Pos2D(x, y))
                        if char[1]:
                            self.line1 += (char[0] + f"{'┤' if x == self.width - 1 else ''}")
                        else:
                            self.line1 += (char[0] + f"{'│' if x == self.width - 1 else ''}")
                    if 2:   # entre case
                        self.line2 += self.between_case(node, x)
            self.sum_full_lines()


    def draw_border(self, cas: int = 0) -> None:
        """
        Dessine les bords de la grille (supérieur ou inférieur).
        """
        item = ('┌', '┬', '┐') if not cas else ('└', '┴', '┘')  # selection des caractères 
        height = 0 if not cas else self.height - 1  # selection d'une ligne (debut ou fin)
        for i in range(self.width):
            node = self.grid[i][height]
            if not self.visibility(i, height):
                    self.line1 += f"    {' ' if i == self.width - 1 else ''}"
                    self.line2 += f"    {' ' if i == self.width - 1 else ''}"
            else:
                if i == 0:  # coin gauche
                    self.line1 += (item[0] + '───')
                else:   # caractères du milieu + coin droit
                    self.line1 += (f"{item[1] if not node.left else '─'}" + "───" + f"{item[2] if i == self.width - 1 else ''}")
                if not cas:  # entre case
                    self.line2 += self.between_case(node, i)
        self.sum_full_lines()


    def show(self) -> None:
        """
        Affiche le donjon sur l'écran.
        """
        i = 0
        self.assembler()
        char_x, char_y = ((self.width * 5) - (self.width - 1)), ((self.height * 3) - (self.height - 1))
        print()
        for _ in range(char_y):
            for _ in range(char_x):
                print(self.full_lines[i], end='')
                i += 1
            print()


    # ----- FONCTIONS HELPER ----- 

    
    def visibility(self, x: int, y: int) -> bool:
        """
        Renvoie la visibilité d'une case.
        """
        return True 
    
    
    def assembler(self) -> None:
        """
        Assemble le bord supérieur, le remplissage central et le bord inférieur.
        """
        self.draw_border()
        self.central_filling()
        self.draw_border(1)
    
    
    def sum_full_lines(self) -> None:
        """
        Ajoute les lignes 1 et 2 à la ligne complète, puis les vides.
        """
        self.full_lines += (self.line1 + self.line2)
        self.line1, self.line2 = '', ''


    def between_case(self, node, i: int) -> str:
        """
        Renvoie le caractère entre-case.
        """
        return f"{'│' if not node.left else ' '}" + "   " + f"{'│' if i == self.width - 1 else ''}"


    def detect_character(self, pos: Pos2D) -> tuple[str, bool]:
        """
        Renvoie le caractère à afficher en fonction des nodes autour de la position.
        """
        x, y = pos.x, pos.y
        node, node_ul = self.grid[x][y], self.grid[x - 1][y - 1]
        # (caractères + boolean) -> True = présence de tirets -> False = vide
        if not node.up and not node.left and node_ul.down and node_ul.right:
            return '┌───', True
        elif node.up and not node.left and not node_ul.down and node_ul.right:
            return '┐   ', False
        elif not node.up and node.left and node_ul.down and not node_ul.right:
            return '└───', True
        elif node.up and node.left and not node_ul.down and not node_ul.right:
            return '┘   ', False
        elif not node.up and not node.left and not node_ul.down and node_ul.right:
            return '┬───', True
        elif not node.up and node.left and not node_ul.down and not node_ul.right:
            return '┴───', True
        elif not node.up and not node.left and node_ul.down and not node_ul.right:
            return '├───', True
        elif node.up and not node.left and not node_ul.down and not node_ul.right:
            return '┤   ', False
        elif not node.up and not node.left and not node_ul.down and not node_ul.right:
            return '┼───', True
        elif node.up and node.left and node_ul.down and not node_ul.right:
            return '│   ', False
        elif node.up and not node.left and node_ul.down and node_ul.right:
            return '│   ', False
        elif node.up and not node.left and node_ul.down and not node_ul.right:
            return '│   ', False
        elif not node.up and node.left and not node_ul.down and node_ul.right:
            return '────', True
        elif not node.up and node.left and node_ul.down and node_ul.right:
            return '────', True
        else:
            return '    ', False


# ----------

class Renderer(GridRenderer):
    
    def __init__(self, grid: Grid, pos: Pos2D, radius: int) -> None:
        """
        Récupère les méthodes de la classe parente.
        """
        super().__init__(grid)
        self.visible = self._visible(pos, radius//2)
    
    
    def between_case(self, node, i: int) -> str:
        """
        Renvoie le caractère entre-case n°2.
        """
        return f"{'│' if not node.left else ' '}" + f" {self.detect_items(node)} " + f"{'│' if i == self.width - 1 else ''}"


    def detect_items(self, node) -> str:
        """
        Renvoie l'item à afficher en fonction du node.
        """
        dict = {'player': 'X', 'bonus': '@', 'end': '#', 'ghost': 'G'}
        for key, value in dict.items():
            if getattr(node, key):
                return value
        return ' '
    

    def _visible(self, pos: Pos2D, radius: int) -> list[Pos2D]: 
        """
        Rend visible les cases autour du joueur selon le rayon euclidien.
        """
        visible = []
        for x in range(pos.x - radius, pos.x + radius + 1):
            for y in range(pos.y - radius, pos.y + radius + 1):
                # filtre (de manière abstraite le carré se transforme en cercle)
                if (x - pos.x) ** 2 + (y - pos.y) ** 2 <= radius ** 2:
                    visible.append(Pos2D(x, y))
        return visible
    
    
    def visibility(self, x: int, y: int) -> bool:
        """
        Renvoie True si la case est visible, False sinon.
        """
        if Pos2D(x, y) in self.visible:
            return True
        return False